from collections import namedtuple


FeatureSet = namedtuple(
    "FeatureSet",
    [
    'MP','FG','FGA',
    'TP','TPA',
    'FT','FTA',
    'ORB','DRB','TRB',
    'AST','STL','BLK','TOV','PF','PTS',
    'TSP','eFGP','TPAr',
    'FTr','ORBP','DRBP','TRBP','ASTP','STLP',
    'BLKP','TOVP','USGP','ORtg','DRtg'
        ] )
        # l40 items

# test = {'away_basic': ['sac', '240', '52', '101', '.515', '6', '22', '.273', '22', '30', '.733', '16', '40', '56', '26', '6', '7', '14', '23', '132'], 'home': 'lal', 
# 'home_advanced': ['lal', '240', '.565', '.522', '.382', '.303', '16.7', '64.4', '39.8', '48.8', '6.4', '11.4', '15.8', '100.0', '104.3', '120.8'], 
# 'away_advanced': ['sac', '240', '.578', '.545', '.218', '.297', '35.6', '83.3', '60.2', '50.0', '5.5', '12.7', '10.9', '100.0', '120.8', '104.3'], 
# 'home_basic': ['lal', '240', '41', '89', '.461', '11', '34', '.324', '21', '27', '.778', '8', '29', '37', '20', '7', '9', '19', '24', '114'], 'away': 'sac'}


def calculate_featues_from_boxscore(boxscore,home=False):
    team = 'home' if home else 'away'
    not_team= 'away' if home else 'home'
    win = int(boxscore[team+'_basic'][-1])>int(boxscore[not_team+'_basic'][-1])
    basic = boxscore[team+'_basic']
    advanced = boxscore[team+'_advanced']
    stats = basic[1:4]+basic[5:7]+basic[8:10]+basic[11:]+advanced[2:]
    return FeatureSet( *[float(x) for x in stats])

def check_win_from_boxscore(boxscore,home=False):
    if home:
        return int(boxscore['home_basic'][-1])>int(boxscore['away_basic'][-1])
    return int(boxscore['home_basic'][-1])<int(boxscore['away_basic'][-1])

