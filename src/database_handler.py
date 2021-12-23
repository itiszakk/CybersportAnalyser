import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def openConnection(databaseName, userName):
    try: 
        connection = psycopg2.connect(dbname=databaseName, user=userName, host="localhost")
        connection.autocommit = False
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except(Exception, psycopg2.Error) as error:
        print("Failed to connect to database: {}".format(error))
    return connection

def stopConnection(connection):
    if connection:
        connection.close()

def execQuery(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except(Exception, psycopg2.Error) as error:
        print("Failed to execute query: {}".format(error))
        connection.rollback()
    finally:    
        if connection:
            cursor.close()