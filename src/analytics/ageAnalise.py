import imp
from src import database_handler as db
from src import environment_handler as env
import re
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
import webbrowser
import config as cfg

def averAge(connection):
    path = '{}/nation_diag/'.format(cfg.outputPath)
    env.createDirectory(path)
    test1 = db.select(connection, "SELECT born, year_active_end, country FROM players", 0)
    test2 = db.select(connection, "SELECT DISTINCT country FROM players", 0)
    countr = {}
    for tt in test2:
        result = 0.0
        k = 0
        for t in test1:
            if t[0] != '-':
                year = re.search(r'\d\d\d\d', str(t[0]))
                if year != None and t[2] == tt[0] :
                    if t[1] != '-':
                        year1 = re.search(r'\d\d\d\d', str(t[1]))
                        if year1 != None:
                            result = result + float(str(year1.group(0))) - float(str(year.group(0)))
                            k = k + 1
                        else:
                            result = result + 2022 - float(str(year.group(0)))
                            k = k + 1
                    else:
                        result = result + 2022 - float(str(year.group(0)))
                        k = k + 1
        try:
            countr[tt[0]] = result / k
        except Exception:
            countr[tt[0]] = 0

    keys = []
    values = []

    for k, v in countr.items():
        keys.append(k)
        values.append(v)

    fig = px.bar(x=keys, y=values, labels={'x': 'Страна', 'y': 'Киберспортсмен'},
                 title='Средний возраст киберспортсменов по странам')

    fig.write_html(path)

    webbrowser.open('file://{}'.format(path))

def nationDiag(connection):
    path = '{}/nation_diag/'.format(cfg.outputPath)
    env.createDirectory(path)

    games = db.select(connection, "SELECT name FROM games", 0)

    for game in games:
        test1 = db.select(connection, "SELECT country FROM players, games WHERE games.id = players.game_id AND games.name = " + "'{}'".format(game[0]), 0)
        test2 = db.select(connection, "SELECT DISTINCT country FROM players", 0)

        countr = {}

        for t in test2:
            countr[t[0]] = 0

        for t in test1:
            countr[t[0]] += 1

        keys = []
        values = []

        for k, v in countr.items():
            keys.append(k)
            values.append(v)

        fig = px.bar(x=keys, y=values, labels={'x': 'Страна', 'y': 'Киберспортсмен'}, title='Распределение киберспортсменов по странам')
    
        fig.write_html('{}{}.html'.format(path, game[0]))

    webbrowser.open('file://{}counterstrike.html'.format(path))
    webbrowser.open('file://{}leagueoflegends.html'.format(path))
    webbrowser.open('file://{}dota2.html'.format(path))
    webbrowser.open('file://{}valorant.html'.format(path))

def teamContrDiag(connection):
    path = '{}/team_diag/'.format(cfg.outputPath)
    env.createDirectory(path)

    games = db.select(connection, "SELECT name FROM games", 0)

    for game in games:
        test1 = db.select(connection, "SELECT country FROM teams, games WHERE games.id = teams.game_id AND games.name = " + "'{}'".format(game[0]), 0)
        test2 = db.select(connection, "SELECT DISTINCT country FROM teams", 0)

        countr = {}

        for t in test2:
            countr[t[0]] = 0

        for t in test1:
            countr[t[0]] += 1

        keys = []
        values = []

        for k, v in countr.items():
            keys.append(k)
            values.append(v)

        fig = px.bar(x=keys, y=values, labels={'x': 'Страна', 'y': 'Киберспортивный клуб'}, title='Распределение киберспортивных клубов по странам')
    
        fig.write_html('{}{}.html'.format(path, game[0]))
        
    webbrowser.open('file://{}counterstrike.html'.format(path))
    webbrowser.open('file://{}leagueoflegends.html'.format(path))
    webbrowser.open('file://{}dota2.html'.format(path))
    webbrowser.open('file://{}valorant.html'.format(path))

def tornMoneyAnal(connection):
    test2 = db.select(connection, "SELECT date, winnings FROM tournaments", 0)
    countr = {}

    years = []
    winnings = []
    for t in test2:
        year = re.search(r'\d\d\d\d', str(t[0]))
        if year != None:
            if str(year.group(0)) not in years:
                years.append(str(year.group(0)))

    years.sort()

    for y in years:
        win = 0
        for w in test2:
            year1 = re.search(r'\d\d\d\d', str(w[0]))
            if year1 != None:
                if str(year1.group(0)) == y and w[1] != None:
                    win += float(w[1])
        winnings.append(win)
    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=winnings))
        file_path = '{}/money_per_year.html'.format(cfg.outputPath)
        fig.write_html(file_path)
        webbrowser.open('file://{}'.format(file_path))

    except Exception:
        print('Херня, по новой!')
