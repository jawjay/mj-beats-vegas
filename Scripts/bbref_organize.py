import json
import re
from collections import defaultdict
from suffixTree import SuffixTree#,PermTree
mainpath = '/Users/MarkJaj/Documents/github/bbrefpy/'
def readYearResults(name):
    with open(mainpath+name) as data_file:
        data = json.load(data_file)
        
    return data
    

def checkMake(s):
    nameReg = '[a-z]*[0-9]{1,3}(?=\.html)'
    missReg = '[a-z]*[0-9]{1,3}\.html\smisses*s\s[2-3]'
    makeReg = '[a-z]*[0-9]{1,3}\.html\smakes*s\s[2-3]'

    makeMatch = re.match(r''+makeReg,s)
    makeSearch = re.search(makeReg,s)
    nameSearch = re.search(nameReg,s)
    if makeSearch:
        return (str(s[nameSearch.start():nameSearch.end()]),str(s[makeSearch.end()-1]),str(s[makeSearch.end()-1]))
    missSearch = re.search(missReg,s)
    if missSearch:
         return (str(s[nameSearch.start():nameSearch.end()]),'0',str(s[missSearch.end()-1]))
    return None

def updatePlayers(players,shots):
    for s in shots:
        players[s[0]].append( (s[1],s[2]))

def savePlayerData(p):
    with open('playerShots2016.txt','w') as data_file:
        json.dump(p,data_file)


data = [readYearResults('2016_box_scores.txt'),readYearResults('2016_box_scores2.txt')]



def getPlayerData(datas):
    players = defaultdict(lambda: [])
    for data in datas:
        print("Number of games: ",len(data))
        # for a in data[1]['201604010CHO']['home']:
        for i in range(len(data)):
            a = data[i]
            game_name = str(a.keys()[0])
            # updatePlayers = lambda x,y,z:players[x].append((y,z)) if x else None
            for h in data[i][game_name]:
                shots = [ s for s in map(lambda x:checkMake(x[1]),data[i][game_name][h]) if s]
                updatePlayers(players,shots)

    return players

def updatePlayerData(players):

    shotdict = {('0','2'):'0',('2','2'):'2',('0','3'):'1',('3','3'):'3'}
    fix_shot = lambda x: shotdict[str(x[0]),str(x[1])]
    string_dict = {}
    # with open(mainpath + name) as data_file:
    #     players = json.load(data_file)
    for p in players:
        string_dict[p] =  ''.join(map(fix_shot,players[p]))
    return string_dict
        # for shot in players[p]:
        #     print fix_shot(shot)

player2 = updatePlayerData(data)

for p in player2:
    print p


