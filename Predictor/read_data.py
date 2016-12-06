import pickle
from box_score_helpers import get_datetime_from_id,get_points_from_boxscore,teamNames
from team_stats import TeamStats
def pickle2box_scores(filepath):
    with open(filepath,'rb') as handle:
        boxScores  = pickle.load(handle)
    return boxScores

def get_teams(box_score):
    return box_score['home'],box_score['away']

def generate_historical_games(box_scores,max_date = None):
    historical_games = []

    for game in box_scores:
        box_score = box_scores[game]
        date = get_datetime_from_id(game)
        if max_date and date>max_date:
            continue
        home_team,away_team = get_teams(box_score)
        hp,ap = get_points_from_boxscore(box_score)
        historical_games.append({
            'home': home_team.upper(),
        'away': away_team.upper(),
        'total_score': hp+ap,
        'h_score':hp,
        'a_score':ap,
        'date': date,
            })
    return historical_games
def generate_all_stats(box_scores,all_stats = None):
    if not all_stats:
        all_stats = {x:TeamStats(x) for x in teamNames}
    for game in box_scores:
        box_score = box_scores[game]
        home = box_score['home'].upper()
        away = box_score['away'].upper()
        all_stats[home].add_game_to_stats(game,box_score,True)
        all_stats[away].add_game_to_stats(game,box_score,False)

    return all_stats
    

