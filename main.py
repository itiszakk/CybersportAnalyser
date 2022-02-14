import os
import json

from src import environment_handler as env
from src import database_handler as db

from src.analytics import ageAnalise
from src.analytics import averageWin
from src.analytics import tournaments_by_country
from src.analytics import ref_from_age_to_place
from src.analytics import in_and_out_age
from src.analytics import total_players_earnings
from src.analytics import total_teams_earnings
from src.analytics import number_of_wins_players
from src.analytics import number_of_wins_team
from src.analytics import statistic_of_wins_players
from src.analytics import statistic_of_wins_team
from src.analytics import players_performance_by_country

import config as cfg

def dropTables(connection):
    db.transaction(connection, """
        DROP TABLE IF EXISTS
            games,
            players, 
            teams, 
            tournaments, 
            players_results, 
            teams_results 
        CASCADE
    """)

def getGamesTableQuery():
    return """
        CREATE UNLOGGED TABLE games (
            id    SERIAL  NOT NULL  PRIMARY KEY,
            name  TEXT    NOT NULL
        )
    """

def getPlayersTableQuery():
    return """
        CREATE UNLOGGED TABLE players (
            id                 SERIAL   NOT NULL  PRIMARY KEY,
            game_id            INTEGER            REFERENCES games(id),
            nick               TEXT     NOT NULL,
            name               TEXT,
            country            TEXT,
            winnings           INTEGER, 
            born               TEXT,
            year_active_start  TEXT, 
            year_active_end    TEXT
        )
    """

def getTeamsTableQuery():
    return """
        CREATE UNLOGGED TABLE teams (
            id        SERIAL  NOT NULL  PRIMARY KEY,
            game_id   INTEGER           REFERENCES games(id),
            name      TEXT    NOT NULL,
            country   TEXT,
            winnings  INTEGER
        )
    """

def getTournamentsTableQuery():
    return """
        CREATE UNLOGGED TABLE tournaments (
            id        SERIAL  NOT NULL  PRIMARY KEY,
            game_id   INTEGER           REFERENCES games(id),
            name      TEXT    NOT NULL,
            date      TEXT,
            type      TEXT,
            country   TEXT[],
            winnings  NUMERIC(12, 3)
        )
    """

def getPlayersResultsTableQuery():
    return """
        CREATE UNLOGGED TABLE players_results (
            id             SERIAL  NOT NULL  PRIMARY KEY,
            player_id      INTEGER           REFERENCES players(id),
            tournament_id  INTEGER           REFERENCES tournaments(id),
            place          TEXT
        )
    """

def getTeamsResultsTableQuery():
    return """
        CREATE UNLOGGED TABLE teams_results (
            id             SERIAL  NOT NULL  PRIMARY KEY,
            team_id        INTEGER           REFERENCES teams(id),
            tournament_id  INTEGER           REFERENCES tournaments(id),
            place          TEXT
        )
    """

def createTables(connection):
    db.transaction(connection, getGamesTableQuery())
    db.transaction(connection, getPlayersTableQuery())
    db.transaction(connection, getTeamsTableQuery())
    db.transaction(connection, getTournamentsTableQuery())
    db.transaction(connection, getPlayersResultsTableQuery())
    db.transaction(connection, getTeamsResultsTableQuery())

def insertGames(connection):
    for gameIndex in range(len(cfg.games)):
        db.transaction(connection, """
        INSERT INTO games(id, name) VALUES ({}, '{}')
    """.format(gameIndex, cfg.games[gameIndex]))
            
def insertPlayers(connection):
    batchElements = []
    playerIndex = 0

    for gameIndex in range(len(cfg.games)):
        with open(cfg.inputPath + r"\{0}\{0}_players.json".format(cfg.games[gameIndex]), mode="r", encoding="utf-8") as file:
            print("Loading players data from: {}".format(os.path.realpath(file.name)))

            data = json.load(file)

            for player in data[0]:
                if not player:
                    continue
                
                nick = player["nick"]
                name = player["name"]
                country = player["country"]
                winnings = player["winnings"]
                born = player["born"]
                year_active_start = player["year_active_start"]
                year_active_end = player["year_active_end"]
                
                nick = nick.replace("\'", "\'\'")
                name = name.replace("\'", "\'\'")
                winnings = winnings.replace("-", "NULL")
                
                line = "({}, {}, '{}', '{}', '{}', {}, '{}', '{}', '{}')".format(
                    playerIndex, 
                    gameIndex, 
                    nick, 
                    name, 
                    country, 
                    winnings, 
                    born, 
                    year_active_start, 
                    year_active_end
                )
                
                batchElements.append(line)
        
                playerIndex += 1

                if len(batchElements) >= cfg.batchSize:
                    db.transaction(connection, """
                        INSERT INTO players VALUES {}
                    """.format(",".join(batchElements)))
                    batchElements = []

    if len(batchElements) > 0:
        db.transaction(connection, """
            INSERT INTO players VALUES {}
        """.format(",".join(batchElements)))

def insertTeams(connection):
    batchElements = []
    teamIndex = 0

    for gameIndex in range(len(cfg.games)):
        with open(cfg.inputPath + r"\{0}\{0}_teams.json".format(cfg.games[gameIndex]), mode="r", encoding="utf-8") as file:
            print("Loading teams data from: {}".format(os.path.realpath(file.name)))

            data = json.load(file)

            for team in data[0]:
                if not team:
                    continue

                name = team["name"]
                country = team["country"]     
                winnings = team["winnings"]

                name = name.replace("\'", "\'\'")
                winnings = winnings.replace("-", "NULL")

                line = "({}, {}, '{}', '{}', {})".format(teamIndex, gameIndex, name, country, winnings)
                batchElements.append(line)
        
                teamIndex += 1

                if len(batchElements) >= cfg.batchSize:
                    db.transaction(connection, """
                        INSERT INTO teams VALUES {}
                    """.format(",".join(batchElements)))
                    batchElements = []

    if len(batchElements) > 0:
        db.transaction(connection, """
            INSERT INTO teams VALUES {}
        """.format(",".join(batchElements)))

def insertTournaments(connection, tournamentsDict):
    batchElements = []
    tournamentIndex = 0

    for gameIndex in range(len(cfg.games)):
        subDict = {}
        
        with open(cfg.inputPath + r"\{0}\{0}_tournament.json".format(cfg.games[gameIndex]), mode="r", encoding="utf-8") as file:
            print("Loading tournaments data from: {}".format(os.path.realpath(file.name)))

            data = json.load(file)
            
            for tournament in data[0]:
                if not tournament:
                    continue
                
                name = tournament["name"]
                date = tournament["date"]
                type = tournament["type"]
                winnings = tournament["winnings"]

                name = name.replace("\'", "\'\'")
                winnings = winnings.replace("-", "NULL")
                winnings = "NULL" if not winnings else winnings
                
                countries = []

                for country in tournament["country"]:
                    country = country.replace("\'", "\'\'")
                    country = country.replace("-", "NULL")
                    country = "NULL" if not country else country
                    
                    countries.append("\'{}\'".format(country))

                line = "({}, {}, '{}', '{}', '{}', array[{}], {})".format(tournamentIndex, gameIndex, name, date, type, ",".join(countries), winnings)
                batchElements.append(line)
                
                subDict[name] = tournamentIndex
                tournamentIndex += 1

                if len(batchElements) >= cfg.batchSize:
                    db.transaction(connection, """
                        INSERT INTO tournaments VALUES {}
                    """.format(",".join(batchElements)))
                    batchElements = []

        tournamentsDict[cfg.games[gameIndex]] = subDict

    if len(batchElements) > 0:
        db.transaction(connection, """
            INSERT INTO tournaments VALUES {}
        """.format(",".join(batchElements)))

def insertPlayersResults(connection, tournamentsDict):
    batchElements = []
    playerIndex = 0

    for gameIndex in range(len(cfg.games)):
        with open(cfg.inputPath + r"\{0}\{0}_players.json".format(cfg.games[gameIndex]), mode="r", encoding="utf-8") as file:
            print("Loading results data from: {}".format(os.path.realpath(file.name)))

            data = json.load(file)

            for player in data[0]:
                if not player:
                    continue
                
                for tournament in player["tournaments"]:
                    if tournament["name"] not in tournamentsDict[cfg.games[gameIndex]]:
                        continue
                    
                    tournamentIndex = tournamentsDict[cfg.games[gameIndex]][tournament["name"]]
                    playerPlace = tournament["place"]
                    
                    line = "(DEFAULT, {}, {}, '{}')".format(playerIndex, tournamentIndex, playerPlace)
                    batchElements.append(line)

                    if len(batchElements) >= cfg.batchSize:
                        db.transaction(connection, """
                            INSERT INTO players_results VALUES {}
                        """.format(",".join(batchElements)))
                        batchElements = []
        
                playerIndex += 1

    if len(batchElements) > 0:
        db.transaction(connection, """
            INSERT INTO players_results VALUES {}
        """.format(",".join(batchElements)))

def insertTeamsResults(connection, tournamentsDict):
    batchElements = []
    teamIndex = 0

    for gameIndex in range(len(cfg.games)):
        with open(cfg.inputPath + r"\{0}\{0}_teams.json".format(cfg.games[gameIndex]), mode="r", encoding="utf-8") as file:
            print("Loading results data from: {}".format(os.path.realpath(file.name)))

            data = json.load(file)

            for team in data[0]:
                if not team:
                    continue
                
                for tournament in team["tournaments"]:
                    if tournament["name"] not in tournamentsDict[cfg.games[gameIndex]]:
                        continue
                    
                    tournamentIndex = tournamentsDict[cfg.games[gameIndex]][tournament["name"]]
                    teamPlace = tournament["place"]

                    line = "(DEFAULT, {}, {}, '{}')".format(teamIndex, tournamentIndex, teamPlace)
                    batchElements.append(line)

                    if len(batchElements) >= cfg.batchSize:
                        db.transaction(connection, """
                            INSERT INTO teams_results VALUES {}
                        """.format(",".join(batchElements)))
                        batchElements = []
        
                teamIndex += 1

    if len(batchElements) > 0:
        db.transaction(connection, """
            INSERT INTO teams_results VALUES {}
        """.format(",".join(batchElements)))

def insertData(connection):
    tournamentsDict = {} # Словарь индексов турниров вида: [game][tournament] = index
    insertGames(connection)
    insertPlayers(connection)
    insertTeams(connection)
    insertTournaments(connection, tournamentsDict)
    insertPlayersResults(connection, tournamentsDict)
    insertTeamsResults(connection, tournamentsDict)

def loadData(connection):
    dropTables(connection)
    createTables(connection)
    insertData(connection)

def runMenu(connection):
    menu_options = {
        1: 'Возраст киберспортсменов',
        2: 'Национальность киберспортсменов',
        3: 'Страны киберспортивных клубов',
        4: 'Призовые от времени',
        5: 'Возраст входа/выхода в киберспорт',
        6: 'Победы киберспортсменов',
        7: 'Победы киберспортивных клубов',
        8: 'Заработок киберспортсменов',
        9: 'Заработок киберспортивных клубов',
        10: 'Турниры по местам проведения',
        11: 'Влияние возраста на результаты',
        12: 'Динамика выигрышей киберспортсмена',
        13: 'Динамика выигрышей киберспортивного клуба',
        14: 'Результативность игроков по странам',
        15: 'Завершить работу!'
    }

    running = True

    while(running):
        os.system("cls")
        
        for key in menu_options.keys():
            print('{}.\t{}'.format(key, menu_options[key]))
        
        try:
            option = int(input('Выбери пункт меню: '))
        except:
            print('Некорректный ввод! Введите число...')
            
        if (option) == 1:
            ageAnalise.averAge(connection)
        elif (option) == 2:
            ageAnalise.nationDiag(connection)
        elif (option) == 3:
            ageAnalise.teamContrDiag(connection)
        elif (option) == 4:
            ageAnalise.tornMoneyAnal(connection)
        elif (option) == 5:
            in_and_out_age.inAndOutAge(connection)
        elif (option) == 6:
            number_of_wins_players.run(connection)
        elif (option) == 7:
            number_of_wins_team.run(connection)
        elif (option) == 8:
            total_players_earnings.run(connection)
        elif (option) == 9:
            total_teams_earnings.run(connection)
        elif (option) == 10:
            tournaments_by_country.run(connection)
        elif (option) == 11:
            ref_from_age_to_place.refAgePlace(connection)
        elif (option) == 12:
            statistic_of_wins_players.run(connection)
        elif (option) == 13:
            statistic_of_wins_team.run(connection)
        elif (option) == 14:
            players_performance_by_country.run(connection)
        elif (option) == 15:
            running = False
        else:
            print('Некорректный ввод!')

        os.system("pause")

def main():
    env.createDirectory(cfg.tempPath)
    env.createDirectory(cfg.outputPath)
    env.install_py_libs()
    env.installSoft(cfg.softPath, cfg.tempPath, "postgresql-14.1-1-windows-x64-binaries.zip")
    env.execFile(cfg.tempPath + r"\pgsql\bin\initdb.exe", "-D {} -U {} -E UTF8".format(cfg.databasePath, cfg.userName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} start".format(cfg.databasePath))
    env.execFile(cfg.tempPath + r"\pgsql\bin\createdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))

    connection = db.openConnection(cfg.databaseName, cfg.userName)
    loadData(connection)
    
    runMenu(connection)

    db.stopConnection(connection)
    
    env.execFile(cfg.tempPath + r"\pgsql\bin\dropdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} stop".format(cfg.databasePath))
    env.removeDirectory(cfg.tempPath)

if __name__ == "__main__":
    main()
