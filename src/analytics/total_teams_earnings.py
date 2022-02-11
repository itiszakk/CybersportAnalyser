import webbrowser
import plotly.express as px

from src import database_handler as db
from src import environment_handler as env
import config as cfg

def get_games(connection):
    data = db.select(connection, 'SELECT name FROM games', 0)
    games = []

    for line in data:
        games.append(line[0])
    
    return games

def get_total_teams_earnings(connection, game):
    query = 'SELECT teams.name, teams.winnings FROM teams, games WHERE teams.game_id = games.id AND games.name = \'{}\''.format(game)
    data = db.select(connection, query, 0)
    
    total_teams_earnings = {}
    
    for line in data:
        total_teams_earnings[line[0]] = 0
    
    for line in data:
        total_teams_earnings[line[0]] = line[1]
    
    return total_teams_earnings

def create_plot(total_teams_earnings, game):
    x = []
    y = []

    for nick, earnings in total_teams_earnings.items():
        x.append(nick)
        y.append(earnings)
    
    fig = px.bar(x=x, y=y, labels={'x': 'Киберспортивный клуб', 'y': 'Заработок (в долларах США)'}, title='Заработок киберспортивных клубов ({})'.format(game))
    file_path = '{}/total_teams_earnings/{}.html'.format(cfg.outputPath, game)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):
    env.createDirectory('{}/total_teams_earnings/'.format(cfg.outputPath))
    games = get_games(connection)
    for game in games:
        total_teams_earnings = get_total_teams_earnings(connection, game)
        create_plot(total_teams_earnings, game)

