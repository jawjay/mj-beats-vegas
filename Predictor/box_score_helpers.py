import datetime

def get_datetime_from_id(name):
    # year month day
    return datetime.date(int(name[:4]),int(name[4:6]),int(name[6:8]))
def get_points_from_boxscore(boxscore):
    return int(boxscore['home_basic'][-1]),int(boxscore['away_basic'][-1])

teamNames = [x.upper() for x in ['atl', 'bos', 'brk', 'chi', 'cho', 'cle', 'dal', 'den', 'det',
             'gsw', 'hou', 'ind', 'lac', 'lal', 'mem', 'mia', 'mil', 'min', 
             'nop', 'nyk', 'okc', 'orl', 'phi', 'pho', 'por', 'sac', 'sas', 
             'tor', 'uta', 'was'] ]
