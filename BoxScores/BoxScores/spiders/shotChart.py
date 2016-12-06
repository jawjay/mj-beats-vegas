import scrapy

class GameShotChartItem(scrapy.Item):
    game = scrapy.Field()

    home = scrapy.Field()
    away = scrapy.Field()
    shotchart = scrapy.Field()
  
class nowGoalSpider(scrapy.Spider):
    name = "shotChartSpider"
    allowed_domains = ['http://www.basketball-reference.com/']
    start_urls = ['http://www.basketball-reference.com/']

    def start_requests(self):

        # get_url = lambda y,m: 'http://nba.nowgoal.com/cn/Normal.aspx?y='+y+'&m='+m+'&matchSeason=2015-2016&SclassID=1'
        urls = ['http://www.basketball-reference.com/boxscores/shot-chart/201610250GSW.html']
        for url in urls:
            yield scrapy.Request(url=url,callback = self.parseChart)
    def parseChart(self,response):
        page = response.url.split('.')[-2][-12:]

        key = (180,165)
        ShotChart = GameShotChartItem()
        ShotChart['game'] = page
        print("TEST")
        tdiv = response.xpath('//div[@id="content"]/div[@class="scorebox"]/div/div/strong/a/@href').extract()
        home = tdiv[0][7:10]
        away = tdiv[1][7:10]

        print(home,away)

#        tdiv = response.xpath('//div[@id="content"]/div[@id="all_line_score"]/div')
        print(tdiv)



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
                print(q,t)
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




