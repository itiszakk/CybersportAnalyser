from src import database_handler as db
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
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
def nationDiag(connection):#траблы с сортировкой, значений получается больше чем ключей
    test1 = db.select(connection, "SELECT country FROM players", 0)
    test2 = db.select(connection, "SELECT DISTINCT country FROM players", 0)
    countr = []
    values = []
    #k = 0
    tr = 0
    for t in test2:
        if t not in countr and t != None:
            countr.extend(t)
            tr = tr + 1
            #strContr = str(t)
            #strContr = strContr.lstrip[1:]
            #strContr = strContr.lstrip[1:]
            #lg = len(strContr)
            #strContr = strContr[:lg-1]
            #k = db.select(connection, "SELECT COUNT ({}) FROM players".format(strContr), 0)
            #for item in test1:
             #   if t == item:
              #      k = k + 1
            #k = 0
            k = test1.count(t)
            values.extend(str(k))

    print(tr)
    print(countr)
    print(len(countr))
    print(values)
    print(len(values))
    try:
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})

        plt.title('Распределение игроков по их родным странам (%)')

        xs = range(len(countr))

        plt.pie(
            values, autopct='%.1f', radius=1.1,
            explode=[0.15] + [0 for _ in range(len(countr) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='lower left', labels=countr)
        fig.savefig('pie.png')

    except Exception:
        print('Херня, по новой!')

def teamContrDiag(connection):#траблы с сортировкой, значений получается больше чем ключей
    test1 = db.select(connection, "SELECT country FROM teams", 0)
    test2 = db.select(connection, "SELECT DISTINCT country FROM teams", 0)
    countr = []
    values = []
    tr = 0
    for t in test2:
        if t not in countr and t != None:
            countr.extend(t)
            tr = tr + 1
            k = test1.count(t)
            values.extend(str(k))

    print(tr)
    print(countr)
    print(len(countr))
    print(values)
    print(len(values))
    try:
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})

        plt.title('Распределение команд по их странам (%)')

        xs = range(len(countr))

        plt.pie(
            values, autopct='%.1f', radius=1.1,
            explode=[0.15] + [0 for _ in range(len(countr) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='lower left', labels=countr)
        fig.savefig('pie.png')

    except Exception:
        print('Херня, по новой!')

def tornMoneyAnal(connection):
    test1 = db.select(connection, "SELECT date, winnings FROM tournaments", 0)
    test2 = db.select(connection, "SELECT date, winnings FROM tournaments", 0)
    years = []
    winnings = []
    result = 0.0
    k = 0
    for t in test1:
        if t[0] != '-':
            year = re.search(r'\d\d\d\d', str(t[0]))
            year = str(year.group(0))
            if year not in years and year != None:
                years.extend(year)
                for item in test2:
                    if item[0] == year and item[1] != '-' and t[1] != None:
                        win = str(t[1])
                        result = result + float(win)
                winnings.extend(result)
                result = 0.0
    print(len(years))
    print(years)
    print(len(winnings))
    print(winnings)
    try:
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})

        plt.title('Распределение команд по их странам (%)')

        xs = range(len(years))

        plt.pie(
            winnings, autopct='%.1f', radius=1.1,
            explode=[0.15] + [0 for _ in range(len(years) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='lower left', labels=years)
        fig.savefig('pie.png')

    except Exception:
        print('Херня, по новой!')