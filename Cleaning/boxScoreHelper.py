



def getFinalScore(box):
    '''Return final score in format
    home-away
    '''
    return box['away_basic'][-1]+'-'+box['home_basic'][-1]

