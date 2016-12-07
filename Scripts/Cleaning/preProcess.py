import pickle
import os
import glob

from cleaningFunctions import full2abv
# with open('box_team_results_cleaned.pkl','rb') as handle:
#     full_results  = pickle.load(handle)

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

def cleanBetsForYear(cYear):
    teams = set()
    years = set()
    correct,incorrect = 0,0
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
                        # continue    
                    gid = year+m+d+'0'+full2abv[h]
                    lines[gid] = f
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

    
    for g in zip(sorted(bbdata),(game_ids[str(goal_year)]+game_ids[str(goal_year+1)])):
        print(g)
        # continue
        if g[0][-6:-4] != current: # if bb day different than current day (chould change 1st)
            current = g[0][-6:-4]

            tofix = {x[1][-3:]:x[1] for x in prev_games}
            fixed = {x[0]:tofix[x[0][-3:]] for x in prev_games}
            print(fixed)
            for c in fixed:
                bet_lines[c] = lines[fixed[c]]
            bbset = set([x[0][-3:] for x in prev_games])
            prev_games = [g]
            continue
        prev_games.append(g)
    return bet_lines


def clean2015(res_2015,betlines):
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
    return betlines


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

def run2014(year = 2014):
    with open('results_by_year.pkl','rb') as handle:
        res_f  = pickle.load(handle)
    res_20x = res_f[str(year)]
    goal_year = year
    game_ids,lines = cleanBetsForYear(goal_year)
    res_20x = [x for x in res_20x if (x[:4]==str(year) and int(x[4:6])>7) or (x[:4]==str(year+1)and int(x[4:5]) <7)]

    addD = lambda x: x if len(x)==12 else x[:4]+'0'+x[4:]
    res_20x = [addD(x) for x in res_20x]
    game_ids[str(year)] = [addD(x) for x in game_ids[str(year)]]
    game_ids[str(year+1)] = [addD(x) for x in game_ids[str(year+1)]]

    game_ids[str(year)] = [x  if x[-3:]!='CHA' else x[:-3]+'CHO' for x in game_ids[str(year)]  ]
    game_ids[str(year+1)] = [x  if x[-3:]!='CHA' else x[:-3]+'CHO' for x in game_ids[str(year+1)] ]



    bb_set = set( (x[-3:] for x in res_20x))
    bet_set = set( ( x[-3:] for x in game_ids[str(year)]))
    for x in game_ids[str(year)]:
        print(x)
    print(bb_set-bet_set)
    # bet_lines = combineData(res_20x,game_ids,lines,goal_year)
    # ans2014 = clean2014(res_2014,bet_lines)

run2014(2013)