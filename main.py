import os
import subprocess
import zipfile
import psycopg2

def createDirectory():
    if (os.path.exists("temp")):
        removeDirectory()
    else:
        os.mkdir("temp")

def removeDirectory():
    for root, dirs, files in os.walk("temp", topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir("temp")

def installSoft():
    print("Installing PostgreSQL...")
    postgresZip = zipfile.ZipFile(r"vendor\postgresql-14.1-1-windows-x64-binaries.zip")
    postgresZip.extractall("temp")
    postgresZip.close()

def initDatabase():
    initPath = os.path.abspath(r"temp\pgsql\bin\initdb.exe")
    databasePath = os.path.abspath(r"temp\database")
    subprocess.call(initPath + " -D " + databasePath)

#def startDatabaseServer():  

def main():
    print("Creating directory...")
    createDirectory()

    print("Installing soft...")
    installSoft()

    print('Initializing database...')
    initDatabase()

    print('Starting database server...')
    #startDatabaseServer()

    os.system("pause")
    
    print("Removing directory...")
    removeDirectory()

if __name__ == "__main__":
    main()