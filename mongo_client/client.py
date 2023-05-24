"""
    Este código servirá para conectar no servidor do Atlas para enviar uma
    requisição HTTP e retornar a resposta mostrando todos os documentos dentro
    da conexão feita neste script.
    
    Ainda é uma versão básica de teste de conexão e será atualizada
    de tempos em tempos.
    
    Versão: dev-0
"""
from pathlib import Path
# Load the environment variables from the virtual environment
from dotenv import dotenv_values
from pymongo import MongoClient
import os
import json

module_path = Path()
config = dotenv_values(f"{module_path.parent.absolute()}/.env")


class Mongo:
    def __init__(self,
                 host: str, user: str, passwd: str, database: str, collection: str, messages: list
                 ):
        self.host = host
        self.database = database
        self.user = user
        self.passwd = passwd
        self.collection = collection
        self.messages = messages

    def get_connection(self):
        # Provide the mongodb atlas url to connect python to mongodb
        connection_string = f"mongodb+srv://{self.user}:{self.passwd}@cluster-1.lk1b0en.mongodb.net/{self.database}"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient()
        client = MongoClient(self.host)

        # Create the database
        return client

    def get_database(self):
        # Get the connection from the previous function and call the database which we will want to get information
        database = self.get_connection()[self.database]

        return database

    def get_collection(self):
        # Get the collection from the database that we call previously
        collection = self.get_database()[self.collection]

        return collection

    def get_messages(self):
        # Returning all messages from the collection
        return self.get_collection().find()

    def send_messages(self):
        # Sending messages for our collection
        self.get_collection().insert_many(self.messages)


if __name__ == "__main__":
    try:
        messages_file = json.load(open(f"{module_path.parent.absolute()}/output/messages.json", "r"))
    except FileNotFoundError as e:
        raise e

    client = Mongo(
        host=os.environ["MONGO_URI"],
        user="root",
        passwd="root",
        database="test",
        collection="test",
        messages=messages_file
    )
    try:
        client.send_messages()
        print("Messages sent successfully!")
    except Exception as e:
        print(e)
