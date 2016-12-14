import scrapy
import datetime
import pickle
from scrapy_splash import SplashRequest
import re

class BettingSpider(scrapy.Spider):
    name = "bettingSpider"



    def start_requests(self):
        # base_url = 'http://data.nowgoal.com/nba/oddsHistory.aspx?Selday='
        
        # urls = ['mark.']
        def nowGoalURL(y,m):
        # getNowGoal = lambda y,m: ('http://nba.nowgoal.com/cn/Normal.html?y='+str(y)+'&m='+str(m)+'&matchSeason=2015-2016&SclassID=1')
            y1,y2 = y,y+1
            yn = y if m>6 else y+1
            return 'http://nba.nowgoal.com/cn/Normal.html?y='+str(yn)+'&m='+str(m)+'&matchSeason='+str(y1)+'-'+str(y2)+'&SclassID=1'

        get_url = lambda y,m: ('http://www.basketball-reference.com/leagues/NBA_'+str(y)+'_games-'+m+'.html')
        s,e = 2004,2016
        urls = [nowGoalURL(y,m) for y in range(s,e+1) for m in [10,11,12,1,2,3,4,5,6] ]
        ou_url = lambda t,y: 'http://nba.nowgoal.com/cn/Team/OuHandicapDetail.html?sclassid=1&teamid={0}&matchseason={1}-{2}&halfOrAll=1'.format(t,y,y+1)


        urls = [ou_url(t,y) for t in range(1,31) for y in range(2004,2016)]
        urls = urls[::-1]# go in decreasing order
        # urls = ['http://nba.nowgoal.com/cn/Normal.html?y=2015&m=10&matchSeason=2015-2016&SclassID=1']
        # urls = ['http://nba.nowgoal.com/cn/Normal.html?y=2015&m=11&matchSeason=2015-2016&SclassID=1']
        # urls = ['http://www.basketball-reference.com/leagues/NBA_2016_games-june.html']
        # urls = ['http://nba.nowgoal.com/cn/Team/OuHandicapDetail.html?sclassid=1&teamid=16&matchseason=2012-2013&halfOrAll=1']
        for url in urls:
            # yield scrapy.Request(url=url,callback = self.parseNowGoal)
            yield scrapy.Request(url,self.parseNowGoalOU,meta = {
                'splash': {
                'endpoint':'render.html',
                'args':{'wait':0.5}
                }
                })
            continue

            yield scrapy.Request(url,self.parseNowGoal,meta = {
                'splash': {
                'endpoint': 'render.html',
                    'args':{'wait':0.5}
                }
                })
   

    def parseNowGoalOU(self,response):
        print("response: ",response,'\n')

        table = response.xpath('//table')
        output = []
        # print("url: ",response.url)
        regexSeas = r"matchseason=(\d{4}\-\d{4})"
        years = re.search(regexSeas, response.url)
        years = years.group(1)
        regexTeam = r"teamid=(\d+)"
        teamid = re.search(regexTeam,response.url)
        teamid = teamid.group(1)
        
        for row in table.xpath('./tbody/tr'):
            vals = [x for x in row.xpath('./td')]
            if not vals[0]:
                continue
            kind = vals[0].xpath('./font/b/text()').extract()
            if kind==['NBAPreseason']:continue
            date = vals[1].xpath('./text()').extract()
            score  = vals[-3].xpath('./font/b/text()').extract()
            ou = vals[-4].xpath('./text()').extract()
            opponent = vals[-2].xpath('./a/font/text()').extract()
            ht = vals[-1].xpath('./font/b/text()').extract()
            if score:

                output.append([x[0] for x in [date,opponent,score,ou,ht]])

        # print(output)
        home = vals[3].xpath('./a/font/text()').extract()
        pname = 'ou_pickles/line{0}_{1}.pkl'.format(years,home[0].replace(" ", ""))
        pickle.dump(output,open(pname,'wb'))
        print('\n'*3)

    def parseNowGoal(self,response):
        # looking for rows with id=Sclass_1
        print("response: ",response)
        # games = response.xpath('//div[@id="info"]/div[@id="i_main"]/div/div[@style="padding-top:2px"]/div')

        divs = response.xpath('//div[@id="scheDiv"]/table')
        utl = response.url.split("=")
        print(utl)
        year = utl[-2][:4]
        month = utl[2][:2]
        if month[1] =='&': month = month[0]

        pname = 'line_pickles2/line'+year+month+'.pkl'
        res = []
        correct = 0
        day = '00'
        for row in divs.xpath('./tbody/tr'):
            try:
                row = [r for r in row.xpath('./td')]
                # print(row.xpath('./td/@text')
                if len(row)<3:
                    # print('CHANGE DAY: ')
                    # print(row[0].xpath('./strong/text()').extract())
                    # print()
                    sp = row[0].xpath('./strong/text()').extract()[0].split("-")
                    d = sp[-1][:2]
                    day = d
                    continue

                # day = row[1].xpath('./text()').extract()[0]
                correct += 1
                
                home = row[2].xpath('./a/text()').extract()
                away = row[4].xpath('./a/text()').extract()
                score = row[3].xpath('./a/span/text()').extract()
                handicap = row[5].xpath('./text()').extract()
                ou = row[6].xpath('./text()').extract()
                ht = row[8].xpath('./text()').extract()

                # print(day,home,away)
                res.append([day,home,away,score,handicap,ou,ht])
                # print(row)
            except:
                continue
            # score = row[3]
        print("Correct: ",correct)
        pickle.dump(res,open(pname,'wb'))
            
            
        # print("TABLE: ",games)
        # # rows = games.xpath('./tbody')
        # for g in games:
        #     print("Table: ",g)
        #     print("TBODY: ",g.xpath('./tbody'))




