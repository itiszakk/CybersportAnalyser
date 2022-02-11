import webbrowser
import plotly.express as px

from src import database_handler as db
import config as cfg
import re

def get_static_of_player(connection, nick):
    query_text =  'SELECT id FROM players WHERE nick=\'' + nick + '\''
    player_id = db.select(connection, query_text, 0)

    query_text =  'SELECT tournament_id, place FROM players_results WHERE player_id=' + str(player_id[0][0])
    results = db.select(connection, query_text, 0)

    statistics_of_player = {}
    for result in results:
        query_text =  'SELECT name FROM tournaments WHERE id=' + str(result[0])
        tournament_name = db.select(connection, query_text, 0)
        place = re.sub('\D','',result[1].split()[0])
        statistics_of_player[tournament_name[0][0]] = place
    
    
    return statistics_of_player

def create_plot(statistic, nick):
    x = []
    y = []

    for tournaments, place in statistic.items():
        x.append(tournaments)
        y.append(place)

    fig = px.bar(x=x, y=y, labels={'x': 'Название турнира', 'y': 'Место'}, title='Динамика выигрышей киберспортсмена')
    file_path = '{}/statistic_of_wins_players_{}.html'.format(cfg.outputPath, nick)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):

    try:
        nick = input('Введите nickname игрока:')
    except:
        print('Некорректный ввод!')
    
    static_player = get_static_of_player(connection, nick)
    create_plot(static_player, nick)

