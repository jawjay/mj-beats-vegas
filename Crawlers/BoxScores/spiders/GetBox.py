import scrapy
import pickle

class BoxSpider(scrapy.Spider):
    name = "getBox"
    # seasons = pickle.load(open('/Users/MarkJaj/Documents/github/bbrefpy/SeasonGames_1985-2017.pkl','rb'))
    

    def start_requests(self):
        pass

    # def start_requests(self):
    #     seasons = pickle.load(open('/Users/MarkJaj/Documents/github/bbrefpy/SeasonGames_1985-2017.pkl','rb'))
    #     urls = ['http://www.basketball-reference.com/boxscores/'+item+'.html' for sublist in seasons for item in seasons[sublist]]
    #     # with  open('/Users/MarkJaj/Desktop/bbref_gamelinks.csv', 'rb') as f:
    #     #     urls = f.read().strip().split(",")
            
    #     for url in urls:
    #         yield scrapy.Request(url=url,callback = self.parse)

    #     def parse(self,response):
    #         page = response.url.split('.')[-2][-12:]
    #         out = open(page+'_response.pkl','wb')
    #         pickle.dump(response.body, out)
    #         self.log('Saved file %s'%page)




