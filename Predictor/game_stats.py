import datetime
import numpy

import team_features
from team_features import FeatureSet
import box_score_helpers

MAX_LOOKBACK_DAYS = 90
LINEAR_TRANSFORM = 'linear_transform'
EXP_TRANSFORM = 'exp_transform'
possible_transforms = {LINEAR_TRANSFORM,EXP_TRANSFORM}
def checkIfBasicTransform(transform_params):
  if transform_params==None:
    return True
  if 'type' in transform_params:
    if transform_params['type'] in possible_transforms:
      return False
  return False
class GameStats(object):
    """ Class to store stats about specific games"""
    def __init__(self):
        self.stats_by_date = {}
        self.ordered_stats = []
        self.record_by_date = {}
        self.wins_by_date = {}

    def add_game_to_stats(self,game,box_score,is_home):
        day_of_game = box_score_helpers.get_datetime_from_id(game)
        stats = team_features.calculate_featues_from_boxscore(box_score,is_home)
        win = team_features.check_win_from_boxscore(box_score,is_home)
        if stats:
            self.stats_by_date[day_of_game] = stats
            self.wins_by_date[day_of_game] = win

    def orderStats(self):
      self.ordered_stats = sorted(self.stats_by_date)

    def get_record_in_range(self,num_games,current_date):
        wins = (sum([ k for i,k in self.wins_by_date.items()][-num_games:]))
        return wins/float(num_games)

    def get_average_stats_from_last_games(self, num_games, current_date, transform_params):
        stat_date = current_date - datetime.timedelta(days=1)
        sum_of_stats = numpy.zeros(len(FeatureSet._fields))      
        # should include get game_weight
        prev_games = numpy.array([self.stats_by_date[x] for x in self.ordered_stats if x<=current_date])[-num_games:]

        if checkIfBasicTransform(transform_params):# no external transform properties
          return numpy.mean(prev_games,axis = 0)
        # we have some type of weighting method
        if transform_params['type']==LINEAR_TRANSFORM:
          weights = [[(num_games-i)/float(num_games)] for i in range(1,num_games+1)]
          return numpy.mean(prev_games*weights,axis = 0)

        if transform_params['type']==EXP_TRANSFORM:
          ep = transform_params['exp_param']
          weights = [[numpy.exp(-1.0*game_num*ep)] for i in range(1,num_games+1)]
          return numpy.mean(prev_games*weights,axis = 0)

