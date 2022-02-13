from src import database_handler as db
import re
import plotly.io as pio
import plotly.graph_objects as go

def inAndOutAge(connection):
    test1 = db.select(connection, "SELECT born, year_active_end FROM players", 0)
    test2 = db.select(connection, "SELECT born, year_active_start FROM players", 0)
    years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
    averinAge = []
    averoutAge = []
    result = 0.0
    k = 0
    for y in years:
        for t in test1:
            if t[0] != '-':
                year = re.search(r'\d\d\d\d', str(t[0]))
                if year != None:
                    if t[1] != '-':
                        year1 = re.search(r'\d\d\d\d', str(t[1]))
                        if year1 != None:
                            if float(str(year1.group(0))) == float(y):
                                result = result + float(str(year1.group(0))) - float(str(year.group(0)))
                                k = k+1
        try:
            result = result / k
        except ZeroDivisionError:
            result = 0
        averoutAge.append(str(result))
        k = 0

    for y in years:
        for t in test2:
            if t[0] != '-':
                year = re.search(r'\d\d\d\d', str(t[0]))
                if year != None:
                    if t[1] != '-':
                        year1 = re.search(r'\d\d\d\d', str(t[1]))
                        if year1 != None:
                            if float(str(year1.group(0))) == float(y):
                                result = result + float(str(year1.group(0))) - float(str(year.group(0)))
                                k = k+1
        try:
            result = result / k
        except ZeroDivisionError:
            result = 0
        averinAge.append(str(result))
        k = 0
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=averoutAge, name='возраст выхода'))
    fig.add_trace(go.Scatter(x=years, y=averinAge, name='возраст входа'))
    fig.show()
    result = 1
    return result