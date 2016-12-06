from bs4 import BeautifulSoup
import urllib
import csv
import re
import json
import os
time_match = lambda x: re.search(r'[0-9]{1,3}\:[0-9]{2}\.[0-9]',x)
def id_match(x):
    m = re.search(r'\/[a-z]\/.*\.html',x)
    if m:
        return m.group(0)
    return x

team_name2abv = {'New Jersey Nets':'NJN','Vancouver Grizzlies':'VAN','Seattle SuperSonics':'SEA','Los Angeles Lakers': 'LAL', 'Chicago Bulls': 'CHI', 'San Antonio Spurs': 'SAS', 'New Orleans Pelicans': 'NOP', 'Houston Rockets': 'HOU', 'Detroit Pistons': 'DET', 'Boston Celtics': 'BOS', 'Miami Heat': 'MIA', 'Orlando Magic': 'ORL', 'Golden State Warriors': 'GSW', 'New York Knicks': 'NYK', 'Washington Wizards': 'WAS', 'Dallas Mavericks': 'DAL', 'Sacramento Kings': 'SAC', 'Los Angeles Clippers': 'LAC', 'Oklahoma City Thunder': 'OKC', 'Charlotte Hornets': 'CHO', 'Milwaukee Bucks': 'MIL', 'Portland Trail Blazers': 'POR', 'Memphis Grizzlies': 'MEM', 'Toronto Raptors': 'TOR', 'Utah Jazz': 'UTA', 'Phoenix Suns': 'PHO', 'Minnesota Timberwolves': 'MIN', 'Philadelphia 76ers': 'PHI', 'Cleveland Cavaliers': 'CLE', 'Atlanta Hawks': 'ATL', 'Brooklyn Nets': 'BRK', 'Indiana Pacers': 'IND', 'Denver Nuggets': 'DEN'}
monthDic = {'october':'10','november':'11','december':'12','january':'01','february':'02','march':'03','april':'04','may':'05','june':'06'}


def getHomeAwayPlay(base_url,name):
    r = urllib.urlopen(base_url).read()
    bs = BeautifulSoup(r,'html.parser')
    table = bs.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="pbp") 
    # rows = table.findAll(lambda tag: tag.name=='tr')
    rows =  []
    ts = bs.find(lambda tag: tag.name =='div' and tag.has_attr('id') and tag['id'] == "div_pbp")

    rows = []
    for c in bs.find_all('tr'):
        if c.find_all('td'):
            rows.append(c.find_all('td'))
    away = []
    for y in  [row for row in rows if time_match(row[0].text) ]:
        if y[1].a:
            s = y[1].text # this is what we need to search for
            away.append([y[0].text.encode('utf8'),re.sub(r''.join(y[1].a.text),id_match(str(y[1].a.get('href'))),y[1].text).encode('utf8')]) 
    # print away
    home = []
    for y in  [row for row in rows if time_match(row[0].text) ]:
        if y[-1].a:
            s = y[-1].text # this is what we need to search for
            home.append([y[0].text.encode('utf8'),re.sub(r''.join(y[-1].a.text),id_match(str(y[-1].a.get('href'))),y[-1].text).encode('utf8')]) 
    # print home
    return ({name:{"away":away, "home":home}})


def writeJSON(s): 
    with open('dataTry.txt','w') as outfile:
        json.dump(getHomeAwayPlay(s),outfile)
def readBox(year,month,day,team):
    mainpath = '/Users/MarkJaj/Documents/github/bbrefpy/schedules'
    base_url = 'http://www.basketball-reference.com/boxscores/pbp/'
    name = year+month+day+'0'+team
    url = base_url+name+'.html'
    return getHomeAwayPlay(url,name)
def getALLgames():
    pass
    mainpath = '/Users/MarkJaj/Documents/github/bbrefpy/schedules'
    scores = []
    for sched in os.listdir(mainpath)[1:]:
        # print sched
        year = sched[:4]
        # print year
        month = sched[4:-4]
        if year!='2016':
            continue
        if int(monthDic[month])>9:
            year= str(int(year)-1)
        if year!='2015':
            continue
        
        current_file = '/'+sched

        print month
        with open(mainpath+current_file,'rb') as csvfile:
            sreader = csv.reader(csvfile,delimiter = ',')
            for row in sreader:
                day = re.search(r'[0-9]{1,2}\,',row[0]).group(0)[:-1]
                if len(day)<2:
                    day = '0'+day
                # print team_name2abv[row[4]], day
                # print(readBox(year,monthDic[month],day,team_name2abv[row[4]]))
                scores.append(readBox(year,monthDic[month],day,team_name2abv[row[4]]))
    with open('2016_box_scores2.txt','w') as outfile:
        json.dump(scores,outfile)


# s = 'http://www.basketball-reference.com/boxscores/pbp/201604010ATL.html'
# scores = [] 
# scores.append(readBox('2016','03','01','CHO'))
# with open('2016_box_scores.txt','w') as outfile:
#     json.dump(scores,outfile)

getALLgames()
# for t in team_name2abv:
#     print t,team_name2abv[t]







