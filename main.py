import os
import json

import psycopg2

from src import environment_handler as env
from src import database_handler as db
import config as cfg

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

def insertTournaments(connection, tournamentsDict, batchSize):
    batchElements = []
    tournamentIndex = 0

    for gameIndex in range(len(cfg.games)):
        subDict = {}
        with open(cfg.inputPath + r"\{0}\{0}_tournament.json".format(cfg.games[gameIndex]), mode="r", encoding="utf-8") as file:
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

                if len(batchElements) >= batchSize:
                    db.transaction(connection, """
                        INSERT INTO tournaments VALUES {}
                    """.format(",".join(batchElements)))
                    batchElements = []

        tournamentsDict[cfg.games[gameIndex]] = subDict

    if len(batchElements) > 0:
        db.transaction(connection, """
            INSERT INTO tournaments VALUES {}
        """.format(",".join(batchElements)))
            

def insertPlayers(connection, tournamentsDict, batchSize):
    batchElements = []

    playerIndex = 0

    for gameIndex in range(len(cfg.games)):
        with open(cfg.inputPath + r"\{0}\{0}_players.json".format(cfg.games[gameIndex]), mode="r", encoding="utf-8") as file:
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
                
                playerLine = "({}, {}, '{}', '{}', '{}', {}, '{}', '{}', '{}')".format(
                    playerIndex, 
                    gameIndex, 
                    nick, 
                    name, 
                    country, 
                    winnings, 
                    born, 
                    year_active_start, 
                    year_active_end)
                
                batchElements.append(playerLine)
        
                playerIndex += 1

                if len(batchElements) >= batchSize:
                    db.transaction(connection, """
                        INSERT INTO players VALUES {}
                    """.format(",".join(batchElements)))
                    batchElements = []

    if len(batchElements) > 0:
        db.transaction(connection, """
            INSERT INTO players VALUES {}
        """.format(",".join(batchElements)))

#def insertTeams(connection, tournamentsDict, gameIndex, batchSize):

def insertData(connection, batchSize):
    tournamentsDict = {} # [game][tournament] = index
    insertGames(connection)
    insertTournaments(connection, tournamentsDict, batchSize)
    insertPlayers(connection, tournamentsDict, batchSize)
    #insertTeams(connection, tournamentsDict, batchSize)

def loadData():
    connection = db.openConnection(cfg.databaseName, cfg.userName)
    dropTables(connection)
    createTables(connection)
    insertData(connection, 100)

    #print(db.select(connection, "SELECT * FROM players WHERE players.nick = 's1mple'", 1))

    db.stopConnection(connection)

def main():
    #env.createDirectory(cfg.tempPath)
    #env.installSoft(cfg.softPath, cfg.tempPath, "postgresql-14.1-1-windows-x64-binaries.zip")
    env.execFile(cfg.tempPath + r"\pgsql\bin\initdb.exe", "-D {} -U {} -E UTF8".format(cfg.databasePath, cfg.userName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} start".format(cfg.databasePath))
    env.execFile(cfg.tempPath + r"\pgsql\bin\createdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))

    loadData()

    os.system("pause")
    
    env.execFile(cfg.tempPath + r"\pgsql\bin\dropdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} stop".format(cfg.databasePath))
    #env.removeDirectory(cfg.tempPath)

if __name__ == "__main__":
    main()