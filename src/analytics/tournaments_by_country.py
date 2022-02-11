import webbrowser
import plotly.express as px

from src import database_handler as db
import config as cfg

def get_tournaments_by_country(connection):
    tournaments_countries = db.select(connection, 'SELECT name, country FROM tournaments', 0)

    tournaments_by_country = {}

    for tournament in tournaments_countries:
        for country in tournament[1]:
            if 'NULL' in country or 'TBA' in country:
                continue
            tournaments_by_country[country] = []

    for tournament in tournaments_countries:
        for country in tournament[1]:
            if 'NULL' in country or 'TBA' in country:
                continue
            tournaments_by_country[country].append(tournament[0])
    
    return tournaments_by_country

def create_plot(tournaments_by_country):
    x = []
    y = []

    for country, tournaments in tournaments_by_country.items():
        x.append(country)
        y.append(len(tournaments))
    
    fig = px.bar(x=x, y=y, labels={'x': 'Место проведения турнира', 'y': 'Количество турниров'}, title='Количество турниров по местам проведения')
    file_path = '{}/tournaments_by_country.html'.format(cfg.outputPath)
    fig.write_html(file_path)
    webbrowser.open('file://{}'.format(file_path))
    
def run(connection):
    tournaments_by_country = get_tournaments_by_country(connection)
    create_plot(tournaments_by_country)

