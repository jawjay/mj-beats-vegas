import pickle
import os
import glob

from cleaningFunctions import full2abv,res_2015
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
    

teams = set()
years = set()
correct,incorrect = 0,0
game_ids = {'2015':[],'2016':[]} 

lines = {}
for p in glob.glob(main_path+'/*.pkl'):

    with open(p,'rb') as handle:
        full = pickle.load(handle)
        year = p.split('/')[-1]
        year,month = year[4:8],year[8:-4]
        m = month
        if (year =='2015'):
            for f in full:
                # print(f)
                if not all(f):
                    continue
                h,a = f[1][0],f[2][0]
                d = f[0]
                if int(m)<7:
                    year = '2016'
                    # continue    
                gid = year+m+d+'0'+full2abv[h]
                lines[gid] = f
                game_ids[year].append(gid)
                if gid in res_2015:
                    correct += 1
                else:
                    incorrect += 1
                    # print(gid)
        # print(h,a)
        # m,d = full[0].split('-')
        # print(m,d)
        # print(full)
            # print(h,a)
    # print(h,a)
# for r in res_2015:print(r)
i = 0


# for g in game_ids:
#     print(g)
current = '00'
prev_games = []

bet_lines = {}

for g in zip(sorted(res_2015),(game_ids['2015']+game_ids['2016'])):
    if g[0][-6:-4] != current:
        current = g[0][-6:-4]

        tofix = {x[1][-3:]:x[1] for x in prev_games}
        fixed = {x[0]:tofix[x[0][-3:]] for x in prev_games}

        for c in fixed:
            bet_lines[c] = lines[fixed[c]]
        bbset = set([x[0][-3:] for x in prev_games])
        # nowset = set([x[1][-3:] for x in prev_games])
        
        # print(bbset==nowset)
        prev_games = [g]

        continue
    prev_games.append(g)
#     if g[1] not in res_2015:
#         print(g[1])# print(sorted(game_ids))
for g in sorted(bet_lines):
    bet_lines[g] = bet_lines[g][-4:]

s1 = set()
s2 = set()
i = 0
notworking = [x.upper() for x in 'dal hou cho mil min was bos brk cle chi lal pho por gsw'.split(' ')]
ans = ['5 187.5 52-34','15 220 64-44','7.5 211 66-50','4.5 201.5 46-62',
    '10 212.5 72-50','-9 210 57-59','4.5 206 38-62','-5.5 206.5 47-49','4 194 44-58',
        '9.5 210 51-60','-3.5 196 42-57','5 205.5 62-55','10 217 58-56','17.5 212.5 70-50']
scores = '91-96 116-81 117-103 92-97 144-109 109-98 98-88 96-103 110-112 115-105 101-96 114-105 107-99 125-104'.split(' ')
fix = dict(zip(notworking,zip(scores,[x.split(' ') for x in ans])))
print(fix)
# print(fix)
for g in sorted(res_2015)[1216:1230]:
    a = fix[g[-3:]]
    bet_lines[g] = [a[0].split('-')] + [[x] for x in a[1] ]

# print(len(bet_lines))
for b in sorted(bet_lines):
    bet_lines[b] = [x[0] for x in bet_lines[b][1:]]



# with open('betting_2015_cleaned.pkl','wb') as handle:
#         pickle.dump(bet_lines,handle)

