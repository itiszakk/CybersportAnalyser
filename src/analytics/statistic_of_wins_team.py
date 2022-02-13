import webbrowser
import plotly.express as px

from src import database_handler as db
from src import environment_handler as env
import config as cfg
import re

def get_static_of_team(connection, name, game):
    query_text =  'SELECT tournaments.name, teams_results.place FROM teams, teams_results, tournaments WHERE teams.id = teams_results.team_id AND tournaments.id = teams_results.tournament_id AND teams.name=\'{}\' AND teams.game_id = {}'.format(name, game)
    results = db.select(connection, query_text, 0)

    statistics_of_team = {}
    for result in results:

        place_t = result[1].lstrip().split()[0]
        if place_t == 'W':
            place = 1
        else:
            try:
                place = int(re.sub('\D', '', place_t))
            except:
                continue

        statistics_of_team[result[0]] = place
    
    
    return statistics_of_team

def create_plot(statistic, name, game):
    x = []
    y = []

    for tournaments, place in statistic.items():
        x.append(tournaments)
        y.append(place)

    fig = px.line(x=x, y=y, labels={'x': 'Название турнира', 'y': 'Место'}, title='Динамика выигрышей команды', markers=True)
    file_path = '{}/statistic_of_wins_teams/{}_{}.html'.format(cfg.outputPath, name, game)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):
    running = True
    while running:
        name = input('Введите название команды: ')
        query_text =  'SELECT games.id, games.name FROM teams, games WHERE teams.game_id=games.id AND teams.name=\'' + name + '\''
        games = db.select(connection, query_text, 0)
        if len(games) == 0:
            print('Некорректный ввод!')
        else:
            running = False
    
    env.createDirectory('{}/statistic_of_wins_teams/'.format(cfg.outputPath))
    
    for game in games:
        static_team = get_static_of_team(connection, name, game[0])
        create_plot(static_team, name, game[1])

