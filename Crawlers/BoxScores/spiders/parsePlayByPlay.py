# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
import re

class pBpItem(scrapy.Item):
    game = scrapy.Field() 
    pbp = scrapy.Field() 


class BbrefboxSpider(scrapy.Spider):
    name = "pbpBox"
    allowed_domains = ["basketball-reference.com"]
    start_urls = ['http://basketball-reference.com/']


    def start_requests(self):
        # have these for unit testing
        # urls = ["http://www.basketball-reference.com/boxscores/198811040BOS.html", 'http://www.basketball-reference.com/boxscores/198811040CHH.html', 'http://www.basketball-reference.com/boxscores/198811040CHI.html', 'http://www.basketball-reference.com/boxscores/198811040DAL.html', 'http://www.basketball-reference.com/boxscores/198811040DEN.html', 'http://www.basketball-reference.com/boxscores/198811040IND.html', 'http://www.basketball-reference.com/boxscores/198811040NJN.html', 'http://www.basketball-reference.com/boxscores/198811040PHI.html', 'http://www.basketball-reference.com/boxscores/198811040POR.html', 'http://www.basketball-reference.com/boxscores/198811040UTA.html', 'http://www.basketball-reference.com/boxscores/198811050DET.html', 'http://www.basketball-reference.com/boxscores/198811050GSW.html', 'http://www.basketball-reference.com/boxscores/198811050HOU.html', 'http://www.basketball-reference.com/boxscores/198811050IND.html', 'http://www.basketball-reference.com/boxscores/198811050MIA.html']
        # urls = urls[:7]
        urls = ['http://www.basketball-reference.com/boxscores/pbp/201610250GSW.html']
        for url in urls:
            yield scrapy.Request(url=url,callback = self.parsePBP)

    def parsePBP(self,response):
        PBP = pBpItem()

        page = response.url.split('.')[-2][-12:]
        table = response.xpath('.//table')
        PBP['game'] = page # set game id
        plays = {'home':[],'away':[]}   # store results of pbp

        for row in table.xpath('./tr'):
            try:
                time = row.xpath('./td/text()').extract()[0]
                print(time)
            except IndexError:
                pass
            if len(row.xpath('./td'))<4:
                continue

            cols = row.xpath('./td/a/..')
            at = len(cols.xpath('./preceding-sibling::*'))
            # print('at: ',len(at))
            cols = cols.xpath('./a | ./text()')
            play = cols.extract()
            for i in range(len(play)):
                p = play[i]
                if p[:2]=='<a':#href tag
                    play[i] = (p.split('>')[0].split('.')[0].split('/')[-1])
            if at==1:#away team
                # print("away: ",play)
                plays['away'].append((time,''.join(play)))
            elif at==5:#home team
                # print("home: ",play)
                plays['home'].append((time,''.join(play)))

        PBP['pbp'] = plays

        # print(tables)