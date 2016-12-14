import pickle
import os
import glob
import sys
from cleaningFunctions import full2abv
# with open('box_team_results_cleaned.pkl','rb') as handle:
#     full_results  = pickle.load(handle)
from collections import defaultdict

main_path = '/Users/MarkJaj/Documents/github/bbrefpy/BoxScores/BoxScores/spiders/line_pickles'
def getYear(s):
    year = s[:4]
    month = s[4:6]
    day = s[-2:]
    if int(month)<6:
        return str(int(year)-1)
    return year


# results = defaultdict(dic2

# for f in full_results:
#     results[getYear(f)][f] = full_results[f]
def organizeAllBets(linepath):
    lines = {}
    matchups = {}
    game_ids = defaultdict(list)
    get_year = lambda year,month: year if month in ['08','09','10','11','12'] else str(int(year)-1)
    for p in glob.glob(linepath+'/*.pkl'):
        with open(p,'rb') as handle:
            full = pickle.load(handle)
        year = p.split('/')[-1]
        year,month = year[4:8],year[8:-4]
        m =  month if len(month)==2 else '0'+month
        bb_year = get_year(year,m)
        for f in full:
            if not all(f):continue
            h,a = f[1][0],f[2][0]
            d = f[0]
            gid = year+m+d+'0'+full2abv[h]
            gid = gid if gid[-3:]!='CHO' else gid[:-3]+'CHA'
            lines[gid] = f
            matchups[gid] = (h,a)
            game_ids[bb_year].append(gid)

    return game_ids,lines,matchups


def cleanBetsForYear(cYear):

    game_ids = {str(cYear):[],str(cYear+1):[]} 
    lines = {}
    for p in glob.glob(main_path+'/*.pkl'):
        with open(p,'rb') as handle:
            full = pickle.load(handle)
        year = p.split('/')[-1]
        year,month = year[4:8],year[8:-4]
        m = month
        if (year ==str(cYear)):
            for f in full:
                # print(f)
                if not all(f):
                    continue
                h,a = f[1][0],f[2][0]
                d = f[0]
                if int(m)<7:
                    year = str(cYear+1)
                gid = year+m+d+'0'+full2abv[h]
                gid = gid if gid[-3:]!='CHO' else gid[:-3]+'CHA'
                addD = lambda x: x if len(x) == 12 else x[:4] + '0' + x[4:]

                lines[addD(gid)] = f
                game_ids[year].append(gid)
    return game_ids,lines



def combineData(bbdata,game_ids,lines,goal_year):
    '''
    bettings lines have incorrect dates, but correct order
     use the structure of bbreff data to organize nowgoal data
    '''
    bet_lines = {}
    current = '00'
    prev_games = []
    i = 0
    err = []
    for g in zip(sorted(bbdata),(game_ids[str(goal_year)]+game_ids[str(goal_year+1)])):
        # print(g)
        # print(i, g)
        i+=1
        if g[0][-6:-4] != current: # if bb day different than current day (chould change 1st)
            current = g[0][-6:-4]
            # try:
            tofix = {x[1][-3:]:x[1] for x in prev_games}
            fixed = {x[0]:tofix[x[0][-3:]] for x in prev_games}
            for c in fixed:
                bet_lines[c] = lines[fixed[c]]

            prev_games = [g]
            continue
        prev_games.append(g)
    return bet_lines


def clean2015(res_2015,bet_lines):
    '''
    hardcode in last set of games for 2015:2016 season
    NEED TO FIX SO IT DOESNT NEED THIS
    '''
    for g in sorted(bet_lines):
        bet_lines[g] = bet_lines[g][-4:]
    notworking = [x.upper() for x in 'dal hou cho mil min was bos brk cle chi lal pho por gsw'.split(' ')]
    ans = ['5 187.5 52-34','15 220 64-44','7.5 211 66-50','4.5 201.5 46-62',
        '10 212.5 72-50','-9 210 57-59','4.5 206 38-62','-5.5 206.5 47-49','4 194 44-58',
            '9.5 210 51-60','-3.5 196 42-57','5 205.5 62-55','10 217 58-56','17.5 212.5 70-50']
    scores = '91-96 116-81 117-103 92-97 144-109 109-98 98-88 96-103 110-112 115-105 101-96 114-105 107-99 125-104'.split(' ')
    fix = dict(zip(notworking,zip(scores,[x.split(' ') for x in ans])))

    for g in sorted(res_2015)[1216:1230]:
        a = fix[g[-3:]]
        bet_lines[g] = [a[0].split('-')] + [[x] for x in a[1] ]


    for b in sorted(bet_lines):
        bet_lines[b] = [x[0] for x in bet_lines[b][1:]]
    return bet_lines


def clean2014(res_2014,bet_lines):
    '''
    hardcode in last set of games for 2014:2015 season
    '''

    for g in sorted(bet_lines):
        bet_lines[g] = bet_lines[g][-4:]
    notworking = [x.upper() for x in 'tor nyk chi brk cle hou nop dal min mil phi mem lal gsw'.split(' ')]
    ans = ['92-87 10.5 194','90-112 -9 193','91-85 5 197.5','101-88 9 203.5','113-108 8 192',
            '117-91 11.5 193.5','108-103 -5.5 193','114-98 6 208.5','113-138 -14 211',
            '100-105 6 198','101-105 2 192','95-83 -2 184.5','99-122 3 206.5','133-126 11.5 215.5']
    fix = dict(zip(notworking,ans))
    for g in sorted(res_2014)[1216:1230]:
        a = fix[g[-3:]].split(" ")
        bet_lines[g] = [a[0].split('-'),[a[1]],[a[2]]]
    for b in sorted(bet_lines):
        bet_lines[b] = [bet_lines[b][0][0],bet_lines[b][0][1],bet_lines[b][1][0],bet_lines[b][2][0]]
            # print(b)
    return bet_lines
def clean2013(res_2013,bet_lines):

    for g in sorted(bet_lines):
        bet_lines[g] = bet_lines[g][-4:]
    teamnames = 'brk lac bos cha cle den mem mia mil min nop nyk okc orl por sac sas'
    teamnames = 'dal hou cha mil min was bos brk cle chi lal pho por gsw'
    teamnames = 'bos cha cle den mem mia mil min nop nyk okc orl por sac sas'
    teamnames = 'orl cha min nop nyk sas cle okc mia bos mil mem por den sac'
    notworking = [x.upper() for x in teamnames.split(' ')]
    ans = ['86-101 3.5 187','91-86 1.5 180.5','130-136 11.5 210.5','105-100 3 208.5','95-92 -6 198.5',
            '100-113 9 217','114-85 8 198','112-111 14.5 212.5','87-100 5.5 208','102-118 -8 197.5','103-111 3 205',
            '106-105 3 190.5','110-104 3 207','112-116 8 209.5','99-104 -2.5 208']
    fix = dict(zip(notworking,ans))
    for g in sorted(res_2013)[1215:1230]: 
        a = fix[g[-3:]].split(" ")
        bet_lines[g] = [a[0].split('-'),[a[1]],[a[2]]]
    for b in sorted(bet_lines):
        bet_lines[b] = [bet_lines[b][0][0],bet_lines[b][0][1],bet_lines[b][1][0],bet_lines[b][2][0]]
            
    return bet_lines
def run2013(year = 2013):
    with open('results_by_year.pkl','rb') as handle:
        res_f  = pickle.load(handle)
    res_20x = res_f[str(year)]
    goal_year = year
    game_ids,lines = cleanBetsForYear(goal_year)
    res_20x = [x for x in res_20x if (x[:4]==str(year) and int(x[4:6])>7) or (x[:4]==str(year+1)and int(x[4:5]) <7)]

    addD = lambda x: x if len(x)==12 else x[:4]+'0'+x[4:]
    res_20x = [addD(x) for x in res_20x]


    # res_20x = [  x if x[-3:]!='CHA' else x[:-3]+'CHO']
    game_ids[str(year)] = [addD(x) for x in game_ids[str(year)]]
    game_ids[str(year+1)] = [addD(x) for x in game_ids[str(year+1)]]

    game_ids[str(year)] = [x  if x[-3:]!='CHO' else x[:-3]+'CHA' for x in game_ids[str(year)]  ]
    game_ids[str(year+1)] = [x  if x[-3:]!='CHO' else x[:-3]+'CHA' for x in game_ids[str(year+1)] ]
    bet_lines = combineData(res_20x,game_ids,lines,goal_year)
    print(len(bet_lines))
    sol2013 = clean2013(res_20x,bet_lines)
    # print( sorted(res_20x)[1215:1230])

def combineData2(bbdata,game_ids,lines):
    '''
    bettings lines have incorrect dates, but correct order
     use the structure of bbreff data to organize nowgoal data
    '''
    bet_lines = {}
    current = '00'
    prev_games = []
    i = 0
    err = []
    for g in zip(sorted(bbdata),game_ids):

        i+=1
        if g[0][-6:-4] != current: # if bb day different than current day (chould change 1st)
            current = g[0][-6:-4]
            # try:
            tofix = {x[1][-3:]:x[1] for x in prev_games}
            print("TOFIX: ",tofix)
            print("PREV: ",prev_games)
            print(i)
            fixed = {x[0]:tofix[x[0][-3:]] for x in prev_games}
            print("FIXED: {0}".format(fixed),i)
            for c in fixed:
                if c[-3:]=='NOH':
                    bet_lines[c] = lines[fixed[c][:-3]+'NOP']
                else:
                    bet_lines[c] = lines[fixed[c]]

            prev_games = [g]
            continue
        prev_games.append(g)
    return bet_lines

def groupBy3(lst):
    out = defaultdict(list)
    for game in lst:
        out[game[-3:]].append(game)
    return out
def connectList(ls1,ls2):
    """
    Assuming games by each team,last 3 chars of list, appear in order.
    give dicts to go from one list to another
    """
    s1,s2 = groupBy3(ls1),groupBy3(ls2)
    bb2line = {}
    line2bb = {}
    for a in set([a for a in s1]+[b for b in s2]):
        # print(a)
        for i,j in zip(s1[a],s2[a]):
            # print('\t',i,j)
            bb2line[i] = j
            line2bb[j] = i
    return bb2line,line2bb

    
games,lines,matchups = organizeAllBets('../Data/line_pickles2')

with open('../Data/Clean/TeamBoxByYear/results_2012.pkl','rb') as handle:
    res12 = pickle.load(handle)


for i in range(len(games['2012'])):
    team = games['2012'][i]
    if team[-3:]=='NOP':
        games['2012'][i] = team[:-3]+'NOH'

def removeDuplicatePreserveOrder(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

bbD,lineD = connectList(sorted(res12),removeDuplicatePreserveOrder(games['2012']))


# for g in zip(sorted(set(games['2012'])),sorted(lineD),sorted(res12)):
#     # print(game,lineD[game])
#     print(g)
z = groupBy3(games['2012'])
for g in z:
    print(g,len(z[g]))
    i=0
    for game in sorted(z[g]):
        i+=1
        print('\t',game,matchups[game])




