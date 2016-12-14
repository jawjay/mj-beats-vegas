
import ijson
import json
import ast
from pprint import pprint
import pickle
from cleaningFunctions import organizeTeam
small_path = '/Users/MarkJaj/Documents/github/bbrefpy/data/example_box_small.json'
large_path = '/Users/MarkJaj/Documents/github/bbrefpy/data/example_box_full.json'
big_file = '/Users/MarkJaj/Documents/github/bbrefpy/data/box_scores-80-16.json'

small_keys = ['game','home','away','home_basic','away_basic']
large_keys = small_keys + ['home_advanced','away_advanced']


def cleanTable(table):
    pass


def readBoxScoreResults(filepath,outputPath='output.pkl'):
    ''' 
    Function to read json output off bbref scraper
    '''
    current_path = filepath
    misclassified = []
    errors = []
    results = {str(year):dict() for year in range(1980,2018)}


    def fix_name(x):
        l = ast.literal_eval(x)
        if l:
            return l[0].split('/')[-1][:-5]
        return 'NONE'
    def fix_table(table,team):
        for t in table[:-1]:
            t[0] = fix_name(t[0])
        table[-1][0] = team
        return table
    def get4tables(game):
        out = dict()
        out['home'] = game['home']
        out['away']  = game['away']
        out['home_advanced'] = fix_table(game['home_advanced'],game['home'])
        out['home_basic'] = fix_table(game['home_basic'],game['home'])
        out['away_advanced'] = fix_table(game['away_advanced'],game['away'])
        out['away_basic'] = fix_table(game['away_basic'],game['away'])
        return out

    with open(current_path,'r') as f:
        i = 0
        for game in ijson.items(f,"item"):
            i+=1
            if i%1000==0:print(i)
            if 'mislabeled' in game:
                misclassified.append(game['game'])
            elif all(key in game for key in large_keys):
                g = game['game']
                year = g[:4]
                results[year][g] =  get4tables(game)
            else:
                 errors.append(game['game'])
                    
    with open(outputPath, 'wb') as handle:
        pickle.dump(results, handle)
    with open('errors.pickle','wb') as handle:
        pickle.dump(errors,handle)
    with open('missclassified.pickle','wb') as handle:
        pickle.dump(misclassified,handle)

    return


def getPlayingTeams(current_path,outfile = 'teamNames.pkl'):

    i=0
    teams = {}
    with open(current_path,'r') as f:
        for game in ijson.items(f,"item"):
            
            if i%1000==0:print(i)
            # if i>10:break
            if 'mislabeled' in game:
                continue

            elif all(key in game for key in large_keys):
                i+=1
                teams[game['game']] ={'home':game['home'],'away':game['away']}


    with open(outfile,'wb') as handle:
        pickle.dump(teams,handle)

def getTeamStats(current_path,outfile = 'teamStats.pkl'):

    def fix_table_team(table,team):
        table[-1][0] = team
        return table[-1]
    def get4tablesTeam(game):
        out = dict()
        out['home'] = game['home']
        out['away']  = game['away']
        out['home_advanced'] = fix_table_team(game['home_advanced'],game['home'])
        out['home_basic'] = fix_table_team(game['home_basic'],game['home'])
        out['away_advanced'] = fix_table_team(game['away_advanced'],game['away'])
        out['away_basic'] = fix_table_team(game['away_basic'],game['away'])
        return out

    with open(current_path,'r') as f:
        results = {}
        i = 0
        for game in ijson.items(f,"item"):
            
            
            if i%1000==0 and i>0:print(i)
            if 'mislabeled' in game:
                continue
            elif all(key in game for key in large_keys):
                i+=1
                g = game['game']
                year = g[:4]
                results[g] =  get4tablesTeam(game)
            else:
                 errors.append(game['game'])
        # print(results)
    with open(outfile,'wb') as handle:
        pickle.dump(results,handle)

# getTeams(big_file,'test_big.pkl')


# getTeamStats(big_file,'testTeam.pkl')
with open('box_team_results_cleaned.pkl','rb') as handle:
    full_results  = pickle.load(handle)

# a = 1
# for i in full_results:
#     a+=1
#     print(full_results[i])
#     if a>3:break

organizeTeam(full_results)
  
# print(full_results)
# errors by year
# {'1979': 427, '1981': 878, '1980': 974, '1982': 1004, '1985': 583, '1983': 989, '1984': 1032}


# with open('missclassified.pickle','rb') as handle:
#     ers = pickle.load(handle)
#     years = ['1982', '1981', '1979', '1983', '1984', '1980', '1985']
#     year_count = {y:0 for y in years}
#     c=0
#     for g in ers:
#         year_count[g[:4]]+=1

#         if g[:4]=='1985' and c <2:
#             c+=1
#             print(g)

    #