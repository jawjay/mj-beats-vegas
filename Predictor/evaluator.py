import numpy 
from model import get_features
import datetime

from constant import SEASON_1516_SPLIT,SEASON_1516_END


WIN_MONEY = 100
LOSS_MONEY = 110
def get_historical_games_by_tuple(historical_games):
  historical_games_by_tuple = {}
  for game in historical_games:
    historical_games_by_tuple[tuple((game['date'], game['home'], game['away']))] = game['total_score']
  return historical_games_by_tuple

def evaluate_model(the_model, all_stats, bet_info, historical_games_by_tuple, moving_averages, transform_params, bet_threshold, cv_percent=0.8, cv_runs=100, start_date=SEASON_1516_SPLIT, end_date=SEASON_1516_END):
  prediction_by_game_tuple = {}
  overunder_by_game_tuple = {}
  for game in bet_info:
    if not start_date <= game['date'] <= end_date:
      continue
    features = get_features(all_stats, game['home'], game['away'], game['date'], moving_averages, transform_params=transform_params)
    if features is not None:
      prediction = the_model.predict(numpy.array([features]))
      game_tuple = tuple((game['date'], game['home'], game['away']))
      prediction_by_game_tuple[game_tuple] = prediction
      overunder_by_game_tuple[game_tuple] = game['overunder']

  winnings_list = []
  for _ in range(cv_runs):
    win = 0
    loss = 0
    for game_tuple in prediction_by_game_tuple:
      if game_tuple not in historical_games_by_tuple:
        continue
      prediction = prediction_by_game_tuple[game_tuple][0]
      actual_score = historical_games_by_tuple[game_tuple]
      overunder = float(overunder_by_game_tuple[game_tuple])
      if numpy.random.uniform(0,1) > cv_percent:
        continue
      if abs(prediction - overunder) < bet_threshold:
        continue
      if prediction < overunder and actual_score < overunder:
        win += 1
      elif prediction > overunder and actual_score > overunder:
        win += 1
      else:
        loss += 1


        
    winnings = win*WIN_MONEY - loss*LOSS_MONEY
    winnings_list.append(winnings)

  winnings_avg = numpy.mean(numpy.array(winnings_list))
  winnings_std = numpy.std(numpy.array(winnings_list))

  print("Avg winnings = {0} +/- {1}".format(
      winnings_avg,
      winnings_std,
      ))
  return winnings_avg, winnings_std