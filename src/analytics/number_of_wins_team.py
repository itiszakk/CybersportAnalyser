import webbrowser
import plotly.express as px

from src import database_handler as db
from src import environment_handler as env
import config as cfg
import re

def get_games(connection):
    data = db.select(connection, 'SELECT name FROM games', 0)
    games = []

    for line in data:
        games.append(line[0])
    
    return games

def get_number_of_wins_team(connection, game):
    wins_of_team = {}

    query_text = 'SELECT teams.name  FROM teams, games WHERE teams.game_id = games.id AND games.name = \'{}\''.format(game)
    teams = db.select(connection, query_text, 0)

    for team in teams:
        wins_of_team[team[0]] = 0

    query_text = 'SELECT teams.name, teams_results.place FROM teams, games, teams_results WHERE teams.game_id = games.id AND teams.id = teams_results.team_id AND games.name = \'{}\''.format(game)
    results = db.select(connection, query_text, 0)

    for result in results:
        place_t = result[1].lstrip().split()[0]
        if place_t == 'W':
            place = 1
        else:
            try:
                place = int(re.sub('\D', '', place_t))
            except:
                continue
        if place == 1:
            wins_of_team[result[0]] += 1
    
    return wins_of_team

def create_plot(wins, game):
    x = []
    y = []

    for team, count_wins in wins.items():
        x.append(team)
        y.append(count_wins)
    fig = px.bar(x=x, y=y, labels={'x': 'Команда', 'y': 'Количество побед'}, title='Победы Команд ({})'.format(game))
    file_path = '{}/number_of_wins_team/{}.html'.format(cfg.outputPath, game)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):
    env.createDirectory('{}/number_of_wins_team/'.format(cfg.outputPath))
    games = get_games(connection)
    for game in games:
        number_of_wins = get_number_of_wins_team(connection, game)
        create_plot(number_of_wins, game)

