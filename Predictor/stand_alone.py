import datetime, os
import pickle
from game_stats import EXP_TRANSFORM

from run_model import runner
import read_data
import evaluator
from constant import SEASON_1516_SPLIT
import bet_reader
import model

def get_historical_games(box_scores,max_date=None):
    all_stats = read_data.generate_all_stats(box_scores)
    historical_games = read_data.generate_historical_games(box_scores,max_date=max_date)
    return historical_games



def run_beatVegas(box_scores,historical_games,historical_games_training_set, bet_info):

    historical_games_by_tuple = evaluator.get_historical_games_by_tuple(historical_games)
    
    all_stats = read_data.generate_all_stats(box_scores)
    moving_averages = [5,15]
    X,y = model.build_model_inputs(historical_games_training_set,all_stats,moving_averages)
    
    the_model = model.build_model(X,y)
    winnings = evaluator.evaluate_model(the_model,all_stats,bet_info,historical_games_by_tuple,moving_averages,None,2.5)
    pass



bpath = '/Users/MarkJaj/Documents/github/bbrefpy/Scripts/Cleaning/betting_2015_cleaned.pkl'
boxpath = '/Users/MarkJaj/Documents/github/bbrefpy/Scripts/Cleaning/results_2015.pkl'

def run_example(boxscorepath,max_date = SEASON_1516_SPLIT) :
    box_scores = read_data.pickle2box_scores(boxscorepath)
    historical_games = get_historical_games(box_scores)
    historical_games_training_set = get_historical_games(box_scores, max_date=max_date)
    historical_games_by_tuple = evaluator.get_historical_games_by_tuple(historical_games)

    bet_info = bet_reader.transform_old_format(bet_reader.readCleanBets(bet_reader.bpath),box_scores)


    run_beatVegas(box_scores,historical_games,historical_games_training_set,bet_info)

run_example(boxpath)