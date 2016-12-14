import datetime
import numpy

import team_features
from team_features import FeatureSet
import box_score_helpers

MAX_LOOKBACK_DAYS = 90
LINEAR_TRANSFORM = 'linear_transform'
EXP_TRANSFORM = 'exp_transform'


class GameStats(object):
    """ Class to store stats about specific games"""
    def __init__(self):
        self.stats_by_date = {}
        self.ordered_stats = []
        self.record_by_date = {}

    def add_game_to_stats(self,game,box_score,is_home):
        day_of_game = box_score_helpers.get_datetime_from_id(game)
        stats = team_features.calculate_featues_from_boxscore(box_score,is_home)
        if stats:
            self.stats_by_date[day_of_game] = stats

    def orderStats(self):
      self.ordered_stats = sorted(self.stats_by_date)

    def get_average_stats_from_last_games(self, num_games, current_date, transform_params):
        stat_date = current_date - datetime.timedelta(days=1)
        sum_of_stats = numpy.zeros(len(FeatureSet._fields))      

        # should include get game_weight
        prev_games = numpy.array([self.stats_by_date[x] for x in self.ordered_stats if x<=current_date])[-num_games:]
        if transform_params==None or (transform_params['type']!=LINEAR_TRANSFORM and transform_params['type']!= EXP_TRANSFORM):
          return numpy.mean(prev_games,axis = 0)

        # we have some type of weighting method
        if transform_params['type']==LINEAR_TRANSFORM:
          weights = [[(num_games-i)/float(num_games)] for i in range(1,num_games+1)]
          return numpy.mean(prev_games*weights,axis = 0)

        if transform_params['type']==EXP_TRANSFORM:
          ep = transform_params['exp_param']
          weights = [[numpy.exp(-1.0*game_num*ep)] for i in range(1,num_games+1)]
          return numpy.mean(prev_games*weights,axis = 0)




# OUTDATED
# updated to simply weighting/averaging with numpy built ins
class GameStats2(object):
    """ Class to store stats about specific games"""
    def __init__(self):
        self.stats_by_date = {}
        self.ordered_stats = []
        self.record_by_date = {}

    def add_game_to_stats(self,game,box_score,is_home):
        day_of_game = box_score_helpers.get_datetime_from_id(game)
        stats = team_features.calculate_featues_from_boxscore(box_score,is_home)
        if stats:
            self.stats_by_date[day_of_game] = stats

    def orderStats(self):
      self.ordered_stats = sorted(self.stats_by_date)

    @staticmethod
    def get_game_weight(game_num, total_num_games, transform_params):
        if transform_params == None:
          return 1.0
        elif transform_params['type'] == LINEAR_TRANSFORM:
          return (total_num_games - game_num) / float(total_num_games)
        elif transform_params['type'] == EXP_TRANSFORM:
          return numpy.exp(-1.0 * game_num * transform_params['exp_param'])
        else:
          raise NotImplementedError("Transform type {0} not implemented.".format(transform_params['type']))


    def get_average_stats_from_last_games(self, num_games, current_date, transform_params):
        ''' want to get averages for some num_games'''
        stat_date = current_date - datetime.timedelta(days=1)
        sum_of_stats = numpy.zeros(len(FeatureSet._fields))
        num_games_averaged = 0
        while num_games_averaged < num_games:
          if stat_date in self.stats_by_date:
            weight = self.get_game_weight(num_games_averaged, num_games, transform_params)
            sum_of_stats += weight * numpy.array(self.stats_by_date[stat_date])
            num_games_averaged += 1
          stat_date -= datetime.timedelta(days=1)
          if stat_date < current_date - datetime.timedelta(days=MAX_LOOKBACK_DAYS):
            break

        # if num_games_averaged < num_games:
        #   raise ValueError("Not enough previous games to average within MAX_LOOKBACK_DAYS ({0}).".format(MAX_LOOKBACK_DAYS))
        return sum_of_stats / float(num_games)


