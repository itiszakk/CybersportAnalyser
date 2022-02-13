import webbrowser
import plotly.express as px

from src import database_handler as db
from src import environment_handler as env
import config as cfg
import re

def get_static_of_player(connection, nick, game):
    query_text =  'SELECT tournaments.name, players_results.place FROM players, players_results, tournaments WHERE players.id = players_results.player_id AND tournaments.id = players_results.tournament_id AND players.nick=\'{}\' AND players.game_id = {}'.format(nick, game)
    results = db.select(connection, query_text, 0)

    statistics_of_player = {}
    for result in results:

        place_t = result[1].lstrip().split()[0]
        if place_t == 'W':
            place = 1
        else:
            try:
                place =int(re.sub('\D', '', place_t))
            except:
                continue

        statistics_of_player[result[0]] = place
    
    
    return statistics_of_player

def create_plot(statistic, nick, game):
    x = []
    y = []

    for tournaments, place in statistic.items():
        x.append(tournaments)
        y.append(place)

    fig = px.line(x=x, y=y, labels={'x': 'Название турнира', 'y': 'Место'}, title='Динамика выигрышей киберспортсмена', markers=True)
    file_path = '{}/statistic_of_wins_players/{}_{}.html'.format(cfg.outputPath, nick, game)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):
    running = True
    while running:
        nick = input('Введите nickname игрока: ')
        query_text =  'SELECT games.id, games.name FROM players, games WHERE players.game_id=games.id AND players.nick=\'' + nick + '\''
        games = db.select(connection, query_text, 0)
        if len(games) == 0:
            print('Некорректный ввод!')
        else:
            running = False
    
    env.createDirectory('{}/statistic_of_wins_players/'.format(cfg.outputPath))
    
    for game in games:
        static_player = get_static_of_player(connection, nick, game[0])
        create_plot(static_player, nick, game[1])

