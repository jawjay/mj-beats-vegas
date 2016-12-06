from bs4 import BeautifulSoup
import urllib.request
import csv
import pickle
from urllib.error import HTTPError
from collections import defaultdict
import html5lib

import pandas as pd
import grequests

def htmlTable2Pandas(game):
    address = 'http://www.basketball-reference.com/boxscores/'+game+'.html'
    try:
        with urllib.request.urlopen(address) as url:
            s = url.read()
            bs = BeautifulSoup(s,"lxml")
            #return bs
    except HTTPError:
        return None
    frames = []
    for t in bs.findAll('table'):
        data = []
        for row in t.findAll('tr'):
            player = ''
            try:
                player = row.findAll('th')[0]['data-append-csv'] #should be id of player
            except: 
                player = None
            if not player:
                continue
            vals = [player]+[r.text for r in row.findAll('td')]
            data.append(vals)
        df = pd.DataFrame(data)#columns = ['NAME','MP','FG','FGA','FGP','3P','3PA','3PP','FT','FTA','FTP','ORB','DRB','TRB','AST,STL'])
        h,w = df.shape
        if h<6 or w<6:
            continue
        frames.append(df)
    # should go away basic, away advanced,home basic, home advanced
    if len(frames)!=4:return
    frames[0].columns = ['NAME','MP','FG','FGA','FGP','3P','3PA','3PP','FT','FTA','FTP','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','PM']
    frames[2].columns = ['NAME','MP','FG','FGA','FGP','3P','3PA','3PP','FT','FTA','FTP','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','PM']
    
    frames[1].columns = ['NAME','MP','TSP','eFGP','3PAr','FTr','ORBP','DRBP','TRBP','ASTP','STLP','BLKP','TOVP','USGP','ORtg','DRtg']
    frames[3].columns = ['NAME','MP','TSP','eFGP','3PAr','FTr','ORBP','DRBP','TRBP','ASTP','STLP','BLKP','TOVP','USGP','ORtg','DRtg']
    return frames

seasons = pickle.load(open('SeasonGames_1985-2017.pkl','rb'))

def trySeas(seasons):
    results = {s:dict() for s in seasons}
    errors = []

    for season in seasons:
        print(season)
        i=0
        for game in seasons[season]:
            i+=1 
            print(i)
            try:
                results[season][game] = htmlTable2Pandas(game)
            except:
                print(game)
                errors.append(game)
                
    out = open("boxScores_1985-2017","wb")
    pickle.dump(results, out)
seasons = pickle.load(open('SeasonGames_1985-2017.pkl','rb'))
t_urls = ['http://www.basketball-reference.com/boxscores/'+game+'.html' for game in seasons['2015']]

rs = (grequests.get(u) for u in t_urls)
grequests.map(rs)
# trySeas(seasons)


