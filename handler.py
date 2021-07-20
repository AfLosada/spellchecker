import json
import sqlite3
conn = sqlite3.connect('database.db')

from spell_checker import spell_check_sentence

def createTable():
    command = """
        CREATE TABLE IF NOT EXISTS petitionhistory (
            petition TEXT, 
            response TEXT
        )
        """
    conn.execute(command)

def insertPetition(petition, response):
    sql = """INSERT INTO petitionhistory VALUES(?, ?)"""
    conn.execute(sql, (petition, response))

def spell_check(event, context):    
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    # Se crea la tabla o se revisa si esta ya existe
    createTable()

    # Primero se lee el body
    input_body= event["body"]
    # Se transforma de string a objeto/diccionario de python
    input_body_text= json.loads(input_body)

    petition = input_body_text["text"]

    # Se lee el atributo que es deseado y se guarda el resultado en una variable
    spell_check = spell_check_sentence(petition)

    insertPetition(petition, spell_check)

    body["input"] = spell_check

    response = {
        "statusCode": 200,
        # Se transforma la variable a json para ser enviada
        "body": json.dumps({"text":spell_check})
    }
    return response