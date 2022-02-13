import webbrowser
import plotly.express as px
import pandas as pd

from src import database_handler as db
import config as cfg

def get_place_by_country_query(country, place):
    return '''SELECT COUNT(players_results.place) 
    FROM players, players_results 
    WHERE players.id = players_results.player_id AND players.country = '{}' AND players_results.place = '{}'
    GROUP BY players.country, players_results.place
    '''.format(country, place)

def get_players_performance_by_country(connection):
    query = 'SELECT DISTINCT country FROM players'
    countries = db.select(connection, query, 0)

    places = ['1st', '2nd', '3rd']
    players_performance_by_country = pd.DataFrame()

    for country in countries:
        dict = {}
        dict['Country'] = country[0]
        for place in places:
            data = db.select(connection, get_place_by_country_query(country[0], place), 0)
            dict[place] = data[0][0] if len(data) != 0 else 0
            print(dict)
        players_performance_by_country = players_performance_by_country.append(dict, ignore_index=True)

    return players_performance_by_country

def create_plot(data_frame):
    fig = px.bar(
        data_frame, 
        x='Country', y=['1st', '2nd', '3rd'],
        labels={'Country': 'Страна'},
        title='Результативность игроков по странам',
    )
    file_path = '{}/players_performance_by_country.html'.format(cfg.outputPath)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):
    data_frame = get_players_performance_by_country(connection)
    create_plot(data_frame)

