import webbrowser
import plotly.express as px
import pandas as pd

from src import database_handler as db
import config as cfg

def get_tournaments_by_country(connection):
    query = '''SELECT tournaments.country, COUNT(tournaments.name), games.name 
    FROM tournaments, games 
    WHERE tournaments.game_id = games.id 
    GROUP BY tournaments.country, games.name'''
    
    data = db.select(connection, query, 0)

    tournaments_by_country = pd.DataFrame()

    for line in data:
        dict = {}
        for country in line[0]:
            if 'NULL' in country or 'TBA' in country:
                continue
            dict['Country'] = country
            dict['Tournaments'] = line[1]
            dict['Game'] = line[2]
            tournaments_by_country = tournaments_by_country.append(dict, ignore_index=True)

    tournaments_by_country = tournaments_by_country.sort_values(by=['Game'])
    return tournaments_by_country

def create_plot(data_frame):
    fig = px.bar(
        data_frame, 
        x='Country', y='Tournaments', 
        color='Game', 
        labels={'Country': 'Место проведения турнира', 'Tournaments': 'Количество турниров', 'Game': 'Игра'}, 
        title='Количество турниров по местам проведения',
    )
    file_path = '{}/tournaments_by_country.html'.format(cfg.outputPath)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):
    data_frame = get_tournaments_by_country(connection)
    create_plot(data_frame)

