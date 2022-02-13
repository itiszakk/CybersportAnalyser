from src import database_handler as db
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.graph_objects as go
import matplotlib.dates as mdates
import datetime as dt
import csv

def averAge(connection):
    test1 = db.select(connection, "SELECT born, year_active_end FROM players", 0)
    result = 0.0
    k = 0
    for t in test1:
        if t[0] != '-':
            year = re.search(r'\d\d\d\d', str(t[0]))
            if year != None:
                if t[1] != '-':
                    year1 = re.search(r'\d\d\d\d', str(t[1]))
                    if year1 != None:
                        result = result + float(str(year1.group(0))) - float(str(year.group(0)))
                        k = k+1
                    else:
                        result = result + 2022 - float(str(year.group(0)))
                        k = k + 1
                else:
                    result = result + 2022 - float(str(year.group(0)))
                    k = k + 1
    result = result / k
    return result

def nationDiag(connection):
    test1 = db.select(connection, "SELECT country FROM players", 0)
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

    fig = dict({
        "data": [{"type": "bar",
                  "x": keys,
                  "y": values }],
        "layout": {"title": {"text": "Распределение игроков по их родным странам"}}
    })
    pio.show(fig)
    
   # plt.bar(keys, values)
    #plt.title('Распределение игроков по их родным странам (%)')
    #plt.xlabel('Страны', fontsize=15)
    #plt.ylabel('Игроки', fontsize=15)
    #plt.show()



def teamContrDiag(connection):#траблы с сортировкой, значений получается больше чем ключей
    test1 = db.select(connection, "SELECT country FROM teams", 0)
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

    fig = dict({
        "data": [{"type": "bar",
                  "x": keys,
                  "y": values}],
        "layout": {"title": {"text": "Распределение игроков по их родным странам"}}
    })
    pio.show(fig)

def tornMoneyAnal(connection):
    test1 = db.select(connection, "SELECT date, winnings FROM tournaments", 0)
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
                if str(year1.group(0)) == y:
                    win += int(t[1])
        winnings.append(win)
    print(len(years))
    print(years)
    print(len(winnings))
    print(winnings)
    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=winnings))
        fig.show()

    except Exception:
        print('Херня, по новой!')
