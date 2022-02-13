from src import database_handler as db
import re
import plotly.graph_objects as go
import webbrowser
import config as cfg

def refAgePlace(connection):
    test2 = db.select(connection, "SELECT players.id, players.born, players_results.place, tournaments.date FROM players, players_results, tournaments WHERE players.id = players_results.player_id AND tournaments.id = players_results.tournament_id", 0)
    age = []
    averPlace = []
    for t in test2:
        if t[1] != None and t[3] != None:
            age1 = re.search(r'\d\d\d\d', str(t[1]))
            age2 = re.search(r'\d\d\d\d', str(t[3]))
            if age1 != None and age2 != None:
                age1 =str(int(str(age2.group(0))) - int(str(age1.group(0))))
                if age1 not in age:
                    age.append(age1)
    age.sort()

    for a in age:
        k = 0
        res = 0
        for t in test2:
            if t[1] != None and t[3] != None:
                age1 = re.search(r'\d\d\d\d', str(t[1]))
                age2 = re.search(r'\d\d\d\d', str(t[3]))
                if age1 != None and age2 != None:
                    age1 = str(int(str(age2.group(0))) - int(str(age1.group(0))))
                    if age1 == a and t[2] != None:
                        plc = re.search(r'\d', str(t[2]))
                        if plc != None:
                            plc = int(str(plc.group(0)))
                            res += plc
                            k += 1
        try:
            res = res/k
        except ZeroDivisionError:
            res = 0
        averPlace.append(res)

    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=age, y=averPlace))
        file_path = '{}/ref_from_age.html'.format(cfg.outputPath)
        fig.write_html(file_path)
        webbrowser.open('file://{}'.format(file_path))

    except Exception:
        print('Херня, по новой!')
    return 1