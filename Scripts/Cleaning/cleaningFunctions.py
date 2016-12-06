
from collections import defaultdict
from team_features import GivenFeatureSetAdvanced,GivenFeatureSetBasic
import pickle
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
full2abv = {
'Atlanta Hawks':'ATL',
'Boston Celtics':'BOS',
'Brooklyn Nets':'BRK',
'Charlotte Bobcats':'CHO',
'Charlotte Hornets': 'CHO',
'Chicago Bulls':'CHI',
'Cleveland Cavaliers':'CLE',
'Dallas Mavericks':'DAL',
'Denver Nuggets':'DEN',
'Detroit Pistons':'DET',
'Golden State Warriors':'GSW',
'Houston Rockets':'HOU',
'Indiana Pacers':'IND',
'Los Angeles Clippers':'LAC',
'Los Angeles Lakers':'LAL',
'Memphis Grizzlies':'MEM',
'Miami Heat':'MIA',
'Milwaukee Bucks':'MIL',
'Minnesota Timberwolves':'MIN',
'New Orleans Pelicans':'NOP',
'New York Knicks':'NYK',
'Oklahoma City Thunder':'OKC',
'Orlando Magic':'ORL',
'Philadelphia 76ers':'PHI',
'Phoenix Suns':'PHO',
'Portland Trail Blazers':'POR',
'Sacramento Kings':'SAC',
'San Antonio Spurs':'SAS',
'Toronto Raptors':'TOR',
'Utah Jazz':'UTA',
'Washington Wizards':'WAS',
}


class Team():
    def __init__(self,name="none"):
        self.record = [(0,0)]
        self.gamestats = []
        self.opponents = []
        self.games = []
    def addGame(self,win):
        if win:
            self.record.append((self.record[-1][0]+1,self.record[-1][1]))
        else:
            self.record.append((self.record[-1][0],self.record[-1][1]+1))



def organizeTeam(results):

    # results = sorted(res) # now in increasing order
    i = 0
    # del res
    get_score = lambda x: int(x[1])*2+int(x[4])*3+int(x[7])

    teams={x:Team(x) for x in team_names}
    for game in sorted(results):
        if (game[:4]=='2015'and game[4:6]in['10','11','12']) or (game[:4]=='2016' and game[4:6] in ['01','02','03','04']):
            i+=1
            home,away = results[game]['home'],results[game]['away']
            
            hb_stats = results[game]['home_basic']
            home_stats,away_stats = results[game]['home_basic'][1:]+results[game]['home_advanced'][1:],results[game]['away_basic'][1:]+results[game]['away_advanced'][1:]

            hscore,ascore = int(results[game]['home_basic'][-1]),int(results[game]['away_basic'][-1])
            
            if results[game]['home']=='gsw':print(results[game]['home_basic'],'\n',results[game]['away_basic'])
            # print(results[game])
            # if home=='gsw':print(home_stats)
            teams[home].addGame(hscore>ascore)
            teams[home].games.append(game)

            teams[away].addGame(ascore>hscore)
            teams[away].games.append(game)

            # teams[away].record.append(ascore>hscore)
        # if i>4:break
    print(i)
    for i,j in zip(teams['gsw'].record[1:],teams['gsw'].games):
        print(i,j)
    # print(teams['gsw'].record)
            
def seperateByYear(results):
    out = {}
    for game in results:
        if (game[:4]=='2015'and game[4:6]in['10','11','12']) or (game[:4]=='2016' and game[4:6] in ['01','02','03','04']):
            out[game] = results[game]
    print(out)
    with open('results_2015.pkl','wb') as handle:
        pickle.dump(out,handle)


# getTeamStats(big_file,'testTeam.pkl')
# with open('box_team_results_cleaned.pkl','rb') as handle:
#     full_results  = pickle.load(handle)
with open('results_2015.pkl','rb') as handle:
    res_2015  = pickle.load(handle)

for r in res_2015:
    print(r,res_2015[r])
# organizeTeam(full_results)
# seperateByYear(full_results)

