import pickle
import os
import glob
from collections import defaultdict
import boxScoreHelper
full2abv = {
'Atlanta Hawks':'ATL',
'Boston Celtics':'BOS',
'Brooklyn Nets':'BRK',
'Charlotte Bobcats':'CHO',
'Charlotte Hornets': 'CHA',
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
'Seattle SuperSonics':'SEA'
}
spacelessTeams = {x.replace(" ",""):x for x in full2abv}

def readOUyear(year='2012'):
    allgames = {}
    for p in glob.glob('../Data/ou_pickles/line{0}*.pkl'.format(year)):
            with open(p,'rb') as handle:
                full = pickle.load(handle)
            team = spacelessTeams[p.split("_")[-1][:-4]]
            abv = full2abv[team]
            for f in full:
                if f[0]:
                    date = f[0].split(" ")[0]
                    y,m,d = date.split("/")
                    gid = '20'+y+m+d+'0'+abv.upper()
                    allgames[gid] = f[1:]
    return allgames


def organizeOU():
    '''
    Update scrapy output with BBref id's and more organization
    '''
    all_results = {str(year):readOUyear(year) for year in range(2005,2016)}
    # for year in range(2005,2016):
    #     year_results = readOUyear(year)
    with open('../Data/ou/allOU2U.pkl','wb') as handle:
            pickle.dump(all_results,handle)

# organizeOU()
def compareBB(year='2006'):
    with open('../Data/Clean/allOU.pkl','rb') as handle:
        res = pickle.load(handle)

    results = res[year]
    with open('../Data/Clean/TeamBoxByYear/results_{0}.pkl'.format(year),'rb') as handle:
        bbres = pickle.load(handle)
    for z in zip(sorted(results),sorted(bbres)):
        pass
def updateOU():
    allresults = {}
    with open('../Data/Clean/allOU.pkl','rb') as handle:
        res = pickle.load(handle)
    for year in res:
        allresults[year] = {}
        with open('../Data/Clean/TeamBoxByYear/results_{0}.pkl'.format(year),'rb') as handle:
            bbres = pickle.load(handle)
        for b,n in zip(sorted(bbres),sorted(res[year])):
            if year=='2015':
                if b[-3:]!=n[-3:]:
                    print("ERROR: ",b)
            allresults[year][b] = res[year][n]

def checkYear(year = '2014'):
    with open('../Data/Clean/allOU.pkl','rb') as handle:
        res = pickle.load(handle)
    res14 = res[year]

    with open('../Data/Clean/TeamBoxByYear/results_{0}.pkl'.format(year),'rb') as handle:
        bbres = pickle.load(handle)


    res,b,g = combineBBlines(bbres,res14)
    for r in res:
        print(r)
    print("B",b)
    print("G",g)
    print(len(res14),len(bbres))
    for g,b in zip(sorted(bbres),sorted(res14)):
        print(g,b)


def checkOUtoBB():
    with open('../Data/Clean/OUbyID.pkl','rb') as handle:
        res = pickle.load(handle)
    i = 0
    working = True
    notworking = {}
    for year in res:
        notworking[year] = []
        with open('../Data/Clean/TeamBoxByYear/results_{0}.pkl'.format(year),'rb') as handle:
            bbres = pickle.load(handle)
        for b,r in zip(sorted(bbres),sorted(res[year])):
            # print(b,r)
            if not (bbres[b]['home'].upper() == full2abv[res[year][r][0]]):
                notworking[year].append((b,bbres[b]['home'],full2abv[res[year][r][0]]))
                # print(b,bbres[b]['home'],full2abv[res[year][r][0]])
    
    for n in sorted(notworking):
        print(n)
        for z in notworking[n]:
            print(z)
        # for pn in notworking[n]:
        #     print(pn)
def readGames(year = '2014'):
    # need to convert CHA to CHO
    with open('../Data/ou/allOU2U.pkl','rb') as handle:
        ouResults = pickle.load(handle)
    glres = ouResults[year]
    with open('../Data/Clean/TeamBoxByYear/results_{0}.pkl'.format(year),'rb') as handle:
            bbres = pickle.load(handle)
    
    return glres,bbres


def line2tuple(res):
    out = {}
    for game in res:
        h,a = game[-3:],full2abv[res[game][0]]
        out[game] = (h,a,res[game][1])
    return out
def box2tuple(res):
    out = {}
    fixCHO = lambda x:'CHA' if x=='CHO' else x
    for game in sorted(res):
        cgame = res[game]
        fscore = boxScoreHelper.getFinalScore(cgame)
        h,a = fixCHO(cgame["away"].upper()),fixCHO(cgame["home"].upper())
        out[game] = (h,a,fscore)
    return out
def bb2teamList(bb):
    games_ordered = []
    games_byteam = defaultdict(list)
    fixCHO = lambda x:'CHA' if x=='CHO' else x
    for game in sorted(bb):
        cgame = bb[game]
        fscore = boxScoreHelper.getFinalScore(cgame)
        h,a = fixCHO(cgame["away"].upper()),fixCHO(cgame["home"].upper())
        team = fixCHO(game[-3:])
        games_byteam[team].append((h,a,fscore,game))
    return games_byteam


def connectGames(year='2014',need_check = False,fixdict = {'BRK':'NJN','OKC':'SEA','NOP':'NOH','CHA':'CHO'}):
    ''' Return betting id to bbref id
    '''
    if year == '2006':
        fixdict = {'BRK':'NJN','OKC':'SEA','NOP':'NOK'}
    gl,bb = readGames(year)
    bbteams = bb2teamList(bb)
    '''
    - Read through sorted games
        -keep sorted list of home team
        - keep sorted list of teams games in dict
    - loop through sorted list of home teams
        - get games from sorted home list
    '''
    teamCounter = defaultdict(int)
    outdict = {}
    
    for game in sorted(gl):
        team = game[-3:]
        i = teamCounter[team]
        teamCounter[team] += 1
        try:
            bbid = bbteams[team][i]
        except IndexError:
            try:
                
                if team in fixdict:
                    team = fixdict[team]
                bbid = bbteams[team][i]
            except IndexError:
                print("Index Error:  ",team,year)
        outdict[game] = bbid 

    new_gl = {}
    for game in outdict:
        new_gl[outdict[game][-1]] = gl[game]
    return new_gl
    # return {game:outdict[game][-1] for game in outdict}
    

def checkConnection(outdict,year):
    gl,bb = readGames(year)
    gans = line2tuple(gl)
    bans = box2tuple(bb)    
    fixdict = {'BRK':'NJN','NOP':'NOH'}
    if year =='2006': fixdict = {'BRK':'NJN','NOP':'NOK'}
    working = True
    for i in outdict:
        bi = outdict[i][-1]

        gteam = gans[i][0]
        bteam = bans[outdict[i]][0]

        if gteam!=bteam:
            if gteam in fixdict:
                if fixdict[gteam]!=bteam:
                    return False
        # print(i,gans[i],bans[bi])    
    print("Games appear to be matched up: ",True)

    #dictionary of betting games to bbgames
    return -1







    # print(od)
    # checkConnection(od,year)



# finalOUtoBB()
# checkYear('2013')
# updateOU()
# checkOUtoBB()