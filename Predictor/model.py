from sklearn import ensemble
import numpy
from team_stats import TeamStats
from box_score_helpers import get_datetime_from_id





def get_features(all_stats, home, away, date, moving_averages, transform_params):
  # try:
  #   x = 1
  features = []
  if home not in all_stats:
    all_stats[home] = TeamStats(home)


  features.extend(all_stats[home].get_features(
      moving_averages,
      date,
      True,
      transform_params=transform_params,
      ))

  if away not in all_stats:
    all_stats[away] = TeamStats(away)
  features.extend(all_stats[away].get_features(
      moving_averages,
      date,
      False,
      transform_params=transform_params,
      ))
  return numpy.array(features)
  # except ValueError as e:
  #   return None


def build_model_inputs(historical_games, all_stats, moving_averages, transform_params=None):
  X = []
  y = []
  cnt = 0
  for game in historical_games:
    features = get_features(all_stats, game['home'], game['away'],game['date'], moving_averages, transform_params)
    if features is not None:
      y.append(game['total_score'])
      X.append(numpy.array(features))
    if features is None:
      cnt+=1
  print(" Errors in build model inputs: ",cnt)
  return numpy.array(X), numpy.array(y)

def build_model(X, y, n_estimators=10, min_samples_split=2, min_samples_leaf=5):
  rf = ensemble.RandomForestRegressor(n_estimators=n_estimators, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
  model = rf.fit(X, y)
  return model
