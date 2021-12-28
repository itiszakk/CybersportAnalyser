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

def insertGame(connection, gameIndex):
    db.transaction(connection, """
        INSERT INTO games(id, name) VALUES ({}, '{}')
    """.format(gameIndex, cfg.games[gameIndex]))

def insertTournaments(connection, gameIndex, batchSize):
    batchElements = []

    fix_quote = lambda s : s.replace("\'", "\'\'")
    fix_dash = lambda s : s.replace("-", "NULL")
    fix_empty = lambda s : "NULL" if not s else s

    with open(cfg.inputPath + r"\{0}\{0}_tournament.json".format(cfg.games[gameIndex]), mode="r", encoding="utf-8") as file:
            data = json.load(file)
            for tournament in data[0]:
                if not tournament:
                    continue
                
                name = tournament["name"]
                date = tournament["date"]
                type = tournament["type"]
                winnings = tournament["winnings"]

                name = fix_quote(name)
                winnings = fix_dash(winnings)
                winnings = fix_empty(winnings)

                countries = []

                for country in tournament["country"]:
                    country = fix_quote(country)
                    country = fix_dash(country)
                    country = fix_empty(country)
                    countries.append("\'{}\'".format(country))

                line = "(DEFAULT, {}, '{}', '{}', '{}', array[{}], {})".format(gameIndex, name, date, type, ",".join(countries), winnings)
                batchElements.append(line)

                if len(batchElements) >= batchSize:
                    db.transaction(connection, """
                        INSERT INTO tournaments VALUES {}
                    """.format(",".join(batchElements)))
                    batchElements = []

    if len(batchElements) > 0:
        db.transaction(connection, """
            INSERT INTO tournaments VALUES {}
        """.format(",".join(batchElements)))

#def insertPlayers(connection, gameIndex, batchSize):

#def insertTeams(connection, gameIndex, batchSize):

def insertData(connection, batchSize):
    for i in range(len(cfg.games)):
        insertGame(connection, i)
        insertTournaments(connection, i, batchSize)
        #insertPlayers(connection, i, batchSize)
        #insertTeams(connection, i, batchSize)

def loadData():
    connection = db.openConnection(cfg.databaseName, cfg.userName)
    dropTables(connection)
    createTables(connection)
    insertData(connection, 100)

    print(db.select(connection, "SELECT * FROM tournaments WHERE 'South Korea' = ANY(country)", 1))

    db.stopConnection(connection)

def main():
    env.createDirectory(cfg.tempPath)
    env.installSoft(cfg.softPath, cfg.tempPath, "postgresql-14.1-1-windows-x64-binaries.zip")
    env.execFile(cfg.tempPath + r"\pgsql\bin\initdb.exe", "-D {} -U {} -E UTF8".format(cfg.databasePath, cfg.userName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} start".format(cfg.databasePath))
    env.execFile(cfg.tempPath + r"\pgsql\bin\createdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))

    loadData()

    os.system("pause")
    
    env.execFile(cfg.tempPath + r"\pgsql\bin\dropdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} stop".format(cfg.databasePath))
    env.removeDirectory(cfg.tempPath)

if __name__ == "__main__":
    main()