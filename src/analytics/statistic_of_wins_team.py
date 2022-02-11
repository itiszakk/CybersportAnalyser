import webbrowser
import plotly.express as px

from src import database_handler as db
import config as cfg
import re

def get_static_of_team(connection, name):
    query_text =  'SELECT id FROM teams WHERE name=\'' + name + '\''
    team_id = db.select(connection, query_text, 0)

    query_text =  'SELECT tournament_id, place FROM teams_results WHERE team_id=' + str(team_id[0][0])
    results = db.select(connection, query_text, 0)

    statistics_of_team = {}
    for result in results:
        query_text =  'SELECT name FROM tournaments WHERE id=' + str(result[0])
        tournament_name = db.select(connection, query_text, 0)
        place = re.sub('\D','',result[1].split()[0])
        statistics_of_team[tournament_name[0][0]] = place
    
    
    return statistics_of_team

def create_plot(statistic, name):
    x = []
    y = []

    for tournaments, place in statistic.items():
        x.append(tournaments)
        y.append(place)

    fig = px.bar(x=x, y=y, labels={'x': 'Название турнира', 'y': 'Место'}, title='Динамика выигрышей киберспортсмена')
    file_path = '{}/statistic_of_wins_team_{}.html'.format(cfg.outputPath, name)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):

    try:
        name = input('Введите название команды:')
    except:
        print('Некорректный ввод!')
    
    static_team = get_static_of_team(connection, name)
    create_plot(static_team, name)

