import datetime, os
import pickle
from game_stats import EXP_TRANSFORM
from run_model import runner
import read_data
import evaluator
from constant import SEASON_1516_SPLIT
import bet_reader
import model

import sys

def get_historical_games(box_scores,max_date=None):
    historical_games = read_data.generate_historical_games(box_scores,max_date=max_date)
    return historical_games



def run_beatVegas(box_scores,historical_games,historical_games_training_set, bet_info):

    historical_games_by_tuple = evaluator.get_historical_games_by_tuple(historical_games)
    all_stats = read_data.generate_all_stats(box_scores)
    



    # all stats is organized by team which is organized by game
    
    moving_averages = [2,5]


    X,y = model.build_model_inputs(historical_games_training_set,all_stats,moving_averages)

    print(X.shape,y.shape)

    transforms = {'type':'linear_transform'}
    the_model = model.build_model(X,y)
    winnings = evaluator.evaluate_model(the_model,all_stats,bet_info,historical_games_by_tuple,moving_averages,transforms,1)
    




boxpath = '../Data/Clean/TeamBoxByYear/results_2015.pkl'
bpath = '../Data/Clean/BettingLinesByYear/betting_2015_cleaned.pkl'
def run_example(boxscorepath,bpath,max_date = SEASON_1516_SPLIT) :
    box_scores = read_data.pickle2box_scores(boxscorepath) # create box scores
    historical_games = get_historical_games(box_scores)
    historical_games_training_set = get_historical_games(box_scores, max_date=max_date) # need a training set
    # historical_games_by_tuple = evaluator.get_historical_games_by_tuple(historical_games)  

   
    bet_info = bet_reader.transform_old_format(bet_reader.readCleanBets(bpath),box_scores)
    run_beatVegas(box_scores,historical_games,historical_games_training_set,bet_info)

if __name__ == '__main__':
    run_example(boxpath,bpath)
    # print(os.listdir('..'))
    # os.getcwdb()



