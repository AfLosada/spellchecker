# Se importa la librería sqlite3 y se mantiene la conexión abierta desde que carga la aplicación
import sqlite3
conn = sqlite3.connect('database.db')

def createTable():
    command = """
        CREATE TABLE IF NOT EXISTS petitionhistory (
            petition TEXT, 
            response TEXT
        )
        """
    conn.execute(command)
    conn.commit()

def insertPetition(petition, response):
    sql = """INSERT INTO petitionhistory VALUES(?, ?)"""
    conn.execute(sql, (petition, response))
    conn.commit()
