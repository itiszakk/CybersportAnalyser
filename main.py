import os
import json

from src import environment_handler as env
from src import database_handler as db
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

    print(db.select(connection, "SELECT * FROM players WHERE players.nick = 's1mple'", 0))


def main():
    env.createDirectory(cfg.tempPath)
    env.installSoft(cfg.softPath, cfg.tempPath, "postgresql-14.1-1-windows-x64-binaries.zip")
    env.execFile(cfg.tempPath + r"\pgsql\bin\initdb.exe", "-D {} -U {} -E UTF8".format(cfg.databasePath, cfg.userName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} start".format(cfg.databasePath))
    env.execFile(cfg.tempPath + r"\pgsql\bin\createdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))

    connection = db.openConnection(cfg.databaseName, cfg.userName)
    loadData(connection)
    # TODO Меню выбора аналитики
    os.system("pause")
    db.stopConnection(connection)
    
    env.execFile(cfg.tempPath + r"\pgsql\bin\dropdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} stop".format(cfg.databasePath))
    env.removeDirectory(cfg.tempPath)

if __name__ == "__main__":
    main()