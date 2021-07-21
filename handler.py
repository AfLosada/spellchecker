import json

# Importo el archivo que se conecta a la base de datos
from database import database

from spell_checker import spell_check_sentence

def get_from_database(event, context):
    total_petition_history = database.getPetitions()
    response = {
        "statusCode": 200,
        # Se transforma la variable a json para ser enviada
        "body": json.dumps({"petitions":total_petition_history})
    }
    return response
def spell_check(event, context):    
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    # Se crea la tabla o se revisa si esta ya existe
    database.createTable()

    # Primero se lee el body
    input_body= event["body"]
    # Se transforma de string a objeto/diccionario de python
    input_body_text= json.loads(input_body)

    petition = input_body_text["text"]

    if(petition.replace(" ", "")):
        # Se lee el atributo que es deseado y se guarda el resultado en una variable
        spell_check = spell_check_sentence(petition)

        # Acá se insertan en la base de datos
        database.insertPetition(petition, spell_check)

        body["input"] = spell_check

        response = {
            "statusCode": 200,
            # Se transforma la variable a json para ser enviada
            "body": json.dumps({"text":spell_check})
        }
    else:
        response = {
            "statusCode": 200,
            # Se transforma la variable a json para ser enviada
            "body": json.dumps({"text":"No se aceptan cadenas vacías"})
        }
    
    return response