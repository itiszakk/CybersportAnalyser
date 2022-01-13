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
            born               DATE,
            year_active_start  NUMERIC(4), 
            year_active_end    NUMERIC(4)
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

def fixQuote(str):
    return str.replace("\'", "\'\'")

def fixDash(str):
    return str.replace("-", "NULL")

def fixEmpty(str):
    return "NULL" if not str else str

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

                name = fixQuote(name)
                winnings = fixDash(winnings)
                winnings = fixEmpty(winnings)

                countries = []

                for country in tournament["country"]:
                    country = fixQuote(country)
                    country = fixDash(country)
                    country = fixEmpty(country)
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
            

#def insertPlayers(connection, tournamentsDict, gameIndex, batchSize):

#def insertTeams(connection, tournamentsDict, gameIndex, batchSize):

def insertData(connection, batchSize):
    tournamentsDict = {} # [game][tournament] = index
    insertGames(connection)
    insertTournaments(connection, tournamentsDict, batchSize)
    #insertPlayers(connection, tournamentsDict, batchSize)
    #insertTeams(connection, tournamentsDict, batchSize)

def loadData():
    connection = db.openConnection(cfg.databaseName, cfg.userName)
    dropTables(connection)
    createTables(connection)
    insertData(connection, 100)

    #print(db.select(connection, "SELECT * FROM tournaments WHERE 'South Korea' = ANY(country)", 1))

    db.stopConnection(connection)

def main():
    #env.createDirectory(cfg.tempPath)
    #env.installSoft(cfg.softPath, cfg.tempPath, "postgresql-14.1-1-windows-x64-binaries.zip")
    env.execFile(cfg.tempPath + r"\pgsql\bin\initdb.exe", "-D {} -U {} -E UTF8".format(cfg.databasePath, cfg.userName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} start".format(cfg.databasePath))
    env.execFile(cfg.tempPath + r"\pgsql\bin\createdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))

    loadData()

    os.system("pause")
    
    #env.execFile(cfg.tempPath + r"\pgsql\bin\dropdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))
    #env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} stop".format(cfg.databasePath))
    #env.removeDirectory(cfg.tempPath)

if __name__ == "__main__":
    main()