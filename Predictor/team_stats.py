from game_stats import GameStats
class TeamStats(object):
    """ Class to store info about a team"""
    def __init__(self,name):
        self.name = name 
        self.stats = {
        'home':GameStats(),
        'away':GameStats(),
        'total':GameStats()
        }

    def add_game_to_stats(self,game,box_score,is_home_game):
        self.stats['total'].add_game_to_stats(game,box_score, is_home_game)
        if is_home_game:
          self.stats['home'].add_game_to_stats(game,box_score, is_home_game)
        else:
          self.stats['away'].add_game_to_stats(game,box_score, is_home_game)



    def get_features(self, moving_averages, current_date, is_home_game, transform_params=None):
        features = []
        court_stats = self.stats['home'] if is_home_game else self.stats['away']
        for num_games in moving_averages:
          for stats in (self.stats['total'], court_stats):
            features.extend(stats.get_average_stats_from_last_games(num_games, current_date, transform_params))
        return features
