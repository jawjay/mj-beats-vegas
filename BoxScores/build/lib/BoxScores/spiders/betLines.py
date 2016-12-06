import scrapy

class GameBettingLinesItem(scrapy.Item):
    date = scrapy.Field()

    year = scrapy.Field()
    month = scrapy.Field()
    results = scrapy.Field()

    home = scrapy.Field()
    away = scrapy.Field()
    ou = scrapy.Field()

class nowGoalSpider(scrapy.Spider):
    name = "nowgoalSpider"
    allowed_domains = ['nowgoal.com','nba.nowgoal.com']
    start_urls = ['nowgoal.com']

    def start_requests(self):

        # get_url = lambda y,m: 'http://nba.nowgoal.com/cn/Normal.aspx?y='+y+'&m='+m+'&matchSeason=2015-2016&SclassID=1'
        urls = ['http://nba.nowgoal.com/cn/Normal.aspx?y=2015&m=12&matchSeason=2015-2016&SclassID=1']
        for url in urls:
            yield scrapy.Request(url=url,callback = self.parseMonth)

    def parseMonth(self,response):
        table = response.xpath('//div')
        print('\n'*2)
        for d in table:
            print(d)
        print('\n'*2)