import os

from src import environment_handler as env
from src import database_handler as db
import config as cfg

def loadData():
    connection = db.openConnection(cfg.databaseName, cfg.userName)
    db.execQuery(connection, "CREATE DATABASE players")
    db.stopConnection(connection)

def main():
    env.createDirectory(cfg.tempPath)
    env.installSoft(cfg.softPath, cfg.tempPath, "postgresql-14.1-1-windows-x64-binaries.zip")
    env.execFile(cfg.tempPath + r"\pgsql\bin\initdb.exe", "-D {} -U {}".format(cfg.databasePath, cfg.userName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} start".format(cfg.databasePath))
    env.execFile(cfg.tempPath + r"\pgsql\bin\createdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))

    print("Loading data...")
    loadData()

    os.system("pause")
    
    env.execFile(cfg.tempPath + r"\pgsql\bin\dropdb.exe", "-U {} {}".format(cfg.userName, cfg.databaseName))
    env.execFile(cfg.tempPath + r"\pgsql\bin\pg_ctl.exe", "-D {} stop".format(cfg.databasePath))
    env.removeDirectory(cfg.tempPath)

if __name__ == "__main__":
    main()