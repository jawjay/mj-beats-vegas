
import pickle
import numpy as np
from box_score_helpers import get_datetime_from_id
from read_data import pickle2box_scores
from collections import defaultdict
def readCleanBets(filepath):
    '''
    Get bet data from pickle file
    Data should be cleaned 
    '''
    with open(filepath,'rb') as handle:
        bets  = pickle.load(handle)
    return bets



def transform_old_format(old_bet_info,boxscores):
    '''
    Convert bets into friendly format
    '''
    bet_info = []
    for game in old_bet_info:
        day = get_datetime_from_id(game)
        home = boxscores[game]['home'].upper()
        away = boxscores[game]['away'].upper()
        bet_info.append({
        'gid':game,
        'spread':old_bet_info[game][0],
        'home':home,'away':away,
        'overunder':old_bet_info[game][1],
        'ht':old_bet_info[game][2],
        'date':day
            })
    return bet_info

