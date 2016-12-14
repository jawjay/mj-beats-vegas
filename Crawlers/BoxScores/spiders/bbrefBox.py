# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader

class GameBoxScoreItem(scrapy.Item):
    game = scrapy.Field() 

    home = scrapy.Field() # hold team name
    home_basic = scrapy.Field()
    home_advanced = scrapy.Field()

    away = scrapy.Field()   # hold team name
    away_basic = scrapy.Field()
    away_advanced = scrapy.Field()

    mislabeled = scrapy.Field()


class GamePlayByPlayItem(scrapy.Item):
    game = scrapy.Field()
    home_plays = scrapy.Field()
    away_plays = scrapy.Field()

class GameShotChartItem(scrapy.Item):
    game = scrapy.Field()
    home = scrapy.Field()
    away = scrapy.Field()
    shotchart = scrapy.Field()
class pBpItem(scrapy.Item):
    game = scrapy.Field() 
    pbp = scrapy.Field() 

  

class BbrefboxSpider(scrapy.Spider):
    name = "bbrefBox"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ['http://basketball-reference.com/']


    def start_requests(self):
        # have these for unit testing
        # urls = ["http://www.basketball-reference.com/boxscores/198811040BOS.html", 'http://www.basketball-reference.com/boxscores/198811040CHH.html', 'http://www.basketball-reference.com/boxscores/198811040CHI.html', 'http://www.basketball-reference.com/boxscores/198811040DAL.html', 'http://www.basketball-reference.com/boxscores/198811040DEN.html', 'http://www.basketball-reference.com/boxscores/198811040IND.html', 'http://www.basketball-reference.com/boxscores/198811040NJN.html', 'http://www.basketball-reference.com/boxscores/198811040PHI.html', 'http://www.basketball-reference.com/boxscores/198811040POR.html', 'http://www.basketball-reference.com/boxscores/198811040UTA.html', 'http://www.basketball-reference.com/boxscores/198811050DET.html', 'http://www.basketball-reference.com/boxscores/198811050GSW.html', 'http://www.basketball-reference.com/boxscores/198811050HOU.html', 'http://www.basketball-reference.com/boxscores/198811050IND.html', 'http://www.basketball-reference.com/boxscores/198811050MIA.html']
        # urls = urls[:7]


        get_url = lambda y,m: ('http://www.basketball-reference.com/leagues/NBA_'+str(y)+'_games-'+m+'.html')
        s,e = 1996,2016
        urls = [get_url(y,m) for y in range(s,e+1) for m in ['october','november','december','january','february','march','april','may','june'] ]
        
        urls = urls[::-1]# go in decreasing order
        
        # urls = ['http://www.basketball-reference.com/leagues/NBA_2016_games-june.html']
        for url in urls:
            yield scrapy.Request(url=url,callback = self.parseMonth)

    def parseMonth(self,response):
        '''
        Function to parse html at basketball reference for a given month of some season
        '''
        tables = response.xpath('//table')
        table = tables[0]

        if len(tables)>1: # more than one table, we want the big one
            temp_table = table
            sz = len(temp_table.xpath('./tbody/tr'))
            for t in tables[1:]:
                if len(temp_table.xpath('./tbody/tr'))>sz:
                    temp_table = t
                    sz = len(temp_table.xpath('./tbody/tr'))
            table = temp_table

        for tr in table.xpath('./tbody/tr'):

            link = tr.xpath('./td[@data-stat="box_score_text"]/a/@href').extract()
            try:
                game = link[0].split('/')[-1]
                link = 'http://www.basketball-reference.com/boxscores/'+game
                linkpbp = 'http://www.basketball-reference.com/boxscores/pbp/'+game
                linkshot = 'http://www.basketball-reference.com/boxscores/shot-chart/'+game
                #yield scrapy.Request(url=link,callback=self.parse)
                yield scrapy.Request(url=linkpbp,callback = self.parsePBP)
                yield scrapy.Request(url=linkshot,callback = self.parseChart)
            except:
                pass        



    def parse(self,response):
        page = response.url.split('.')[-2][-12:]
        scores = GameBoxScoreItem()
        scores['game']=page  #unique game id
        def clean_table(test_table):
            #function to return data from box score html table
            rows = test_table.xpath('./tbody/tr').extract()
            temp = []
            for row in test_table.xpath('./tbody/tr'):
                name = str(row.xpath('./th/a/@href').extract()) # want unique url , use as player id
                temp.append([name] + [str(c) for c in row.xpath('./td/text()').extract()])

            row = test_table.xpath('./tfoot/tr')
            try:
                temp.append(['Team Totals']+ [str(c) for c in row.xpath('./td/text()').extract()])
            except:
                return temp
            return temp

        tables = response.xpath('//table')# get all tables
        table_labels = response.xpath('//table/@id').extract() #get id's of all tables



        if len(tables)==4: # should be regular boxscores box scores
                scores['home'] = table_labels[0].split("_")[1] #home team name
                scores['away'] = table_labels[3].split("_")[1]  # away team name
                scores['home_basic'] = clean_table(tables[0])
                scores['home_advanced'] = clean_table(tables[1])
                scores['away_basic'] = clean_table(tables[2])
                scores['away_advanced'] = clean_table(tables[3])
        elif len(tables)==2:
                scores['home'] = table_labels[0].split("_")[1] #home team name
                scores['away'] = table_labels[1].split("_")[1]  # away team name
                scores['home_basic'] = clean_table(tables[0])
                scores['away_basic'] = clean_table(tables[2])

        else:
            # if we have the wrong number of tables return everything for analysis later
            scores['mislabeled'] = {l:t for l,t in zip(table_labels,tables.extract())}
     

        yield(scores)

    def parseChart(self,response):
        page = response.url.split('.')[-2][-12:]
    
        ShotChart = GameShotChartItem()
        ShotChart['game'] = page
        tdiv = response.xpath('//div[@id="content"]/div[@class="scorebox"]/div/div/strong/a/@href').extract()
        home = tdiv[0][7:10]
        away = tdiv[1][7:10]
        mdivs = [response.xpath('//div[@id="wrapper-'+h+'"]/div') for h in [home,away]]
        fshots = [[],[]]
        i=0
        for mdiv in mdivs:
            shots = fshots[i]
            i+=1
            for shot in mdiv.xpath('./div'):
                # at holds x,y representation of shot in shot chart
                at = shot.xpath('./@style').extract()[0]
                time = shot.xpath('./@tip').extract()[0]
                q,t = time[0],time.split(" ")[2]
                top = at[4:7]
                if top[-1]=='x':
                    top=top[0]
                    # 1 digit first num
                    left = at[13:16]
                    if left[-1]==['x']:left=left[0]
                    elif left[-1]==['p']:left = left[:1]
                elif top[-1]=='p':
                    top=top[:-1]
                    left = at[14:17]
                    if left[-1]==['x']:left=left[0]
                    elif left[-1]==['p']:left = left[:1]
                else:left = at[15:18]
                shots.append((top,left,q,t))

        ShotChart['shotchart'] = fshots
        yield ShotChart

    def parsePBP(self,response):
        PBP = pBpItem()
        page = response.url.split('.')[-2][-12:]
        table = response.xpath('.//table')
        PBP['game'] = page # set game id
        plays = {'home':[],'away':[]}   # store results of pbp
        for row in table.xpath('./tr'):
            try:
                time = row.xpath('./td/text()').extract()[0]
            except IndexError:
                pass
            if len(row.xpath('./td'))<4:
                continue
            cols = row.xpath('./td/a/..')
            at = len(cols.xpath('./preceding-sibling::*'))
            cols = cols.xpath('./a | ./text()')
            play = cols.extract()
            for i in range(len(play)):
                p = play[i]
                if p[:2]=='<a':#href tag
                    play[i] = (p.split('>')[0].split('.')[0].split('/')[-1])
            if at==1:#away team
                plays['away'].append((time,''.join(play)))
            elif at==5:#home team
                plays['home'].append((time,''.join(play)))
        PBP['pbp'] = plays
        yield PBP

