import scrapy
import datetime
import pickle
from scrapy_splash import SplashRequest

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
        
        urls = urls[::-1]# go in decreasing order
        urls = ['http://nba.nowgoal.com/cn/Normal.html?y=2015&m=10&matchSeason=2015-2016&SclassID=1']
        # urls = ['http://nba.nowgoal.com/cn/Normal.html?y=2015&m=11&matchSeason=2015-2016&SclassID=1']
        # urls = ['http://www.basketball-reference.com/leagues/NBA_2016_games-june.html']
        for url in urls:
            # yield scrapy.Request(url=url,callback = self.parseNowGoal)
            yield scrapy.Request(url,self.parseNowGoal,meta = {
                'splash': {
                'endpoint': 'render.html',
                    'args':{'wait':0.5}
                }
                })
   

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

        print("MAIN: ",divs)
        pname = 'line_pickles/line'+year+month+'.pkl'
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
                    print('DAY: ',day)
                    continue

                # day = row[1].xpath('./text()').extract()[0]
                correct += 1
                
                home = row[2].xpath('./a/text()').extract()
                away = row[4].xpath('./a/text()').extract()
                print(day,home,away)
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




