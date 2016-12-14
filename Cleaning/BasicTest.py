
import pickle
import numpy as np
import pandas as pd

basic = ['NAME','MP','FG','FGA','FGP','TP','TPA',
                    'TPP','FT','FTA','FTP','ORB','DRB','TRB',
                    'AST','STL','BLK','TOV','PF','PTS','PM']

advanced = ['NAME','MP','TSP','eFGP','TPAr',
                            'FTr','ORBP','DRBP','TRBP','ASTP','STLP',
                            'BLKP','TOVP','USGP','ORtg','DRtg']

                            
team_names = ['atl', 'bos', 'brk', 'chi', 'cho', 'cle', 'dal', 'den', 'det',
             'gsw', 'hou', 'ind', 'lac', 'lal', 'mem', 'mia', 'mil', 'min', 
             'nop', 'nyk', 'okc', 'orl', 'phi', 'pho', 'por', 'sac', 'sas', 
             'tor', 'uta', 'was']




class Team():
    def __init__(self,name="none"):
        self.record = [(0,0)]
        self.gamestats = []
        self.opponents = []
        self.games = []
        self.name = name
    def addWin(self,win):
        if win:
            self.record.append((self.record[-1][0]+1,self.record[-1][1]))
        else:
            self.record.append((self.record[-1][0],self.record[-1][1]+1))
    def addGame(self,name,stats):
        self.gamestats.append(stats)
        self.games.append(name)
    def __str__(self):
        return str(self.name)+":"+str(self.record[-1])




testing_games = ['201603180DAL','201603280POR','201511170NYK']

teams={x:Team(x) for x in team_names}

records = {x:[0,0] for x in teams}
for game in results:
    home = results[game]['home']
    away = results[game]['away']
    hscore,ascore = int(results[game]['home_basic'][-1]),int(results[game]['away_basic'][-1])
            
    home_stats = results[game]['home_advanced'][2:]
    away_stats = results[game]['away_advanced'][2:]
    
    teams[home].addWin(hscore>ascore)
    teams[away].addWin(ascore>hscore)
    teams[home].addGame(game,home_stats)
    teams[away].addGame(game,away_stats)

