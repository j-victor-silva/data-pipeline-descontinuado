"""
    Este código servirá para conectar no servidor do Atlas para enviar uma
    requisição HTTP e retornar a resposta mostrando todos os documentos dentro
    da conexão feita neste script.
    
    Ainda é uma versão básica de teste de conexão e será atualizada
    de tempos em tempos.
    
    Versão: dev-0
"""
import os
import json
from pathlib import Path
# Load the environment variables from the virtual environment
from dotenv import dotenv_values
from pymongo import MongoClient
from typing import Optional

module_path = Path()
config = dotenv_values(f"{module_path.parent.absolute()}/.env")


class Mongo:
    """
    Um conector para o MongoDB com padrões específicos para um certo tipo de conexão, que no caso será para
    o projeto DocAssure

    - A classe possui o método de inicialização (:method:`__init__`) que recebe os parâmetros iniciais

    - :method:`get_connection()` recebe os args (host, port) de conexão com o banco de dados e cria essa conexão

    - :method:`get_database()` recebe a conexão que foi criada e junto com o arg `database` cria o objeto
    `pymongo.database.Database`

    - :method:`get_collection()` cria a conexão para a coleção desejada utilizando do arg `collection`, criando
    o objeto `pymongo.collection.Collection`

    - :method:`get_messages()` irá listar as mensagens da nossa coleção

    - :method:`send_messages()` irá enviar as mensagens do arg `messages` para nossa coleção

    - :method:`close()` encerra a conexão
    """
    HOST = "localhost"
    PORT = 27017

    def __init__(
            self,
            host: Optional[str] = None,
            port: Optional[str] = None,
            user: Optional[str] = "",
            passwd: Optional[str] = "",
            database: str = "track",
            collection: str = "data",
            messages: list = None
     ) -> None:
        """

        """
        self.host = self.HOST if host is None else host
        self.port = self.PORT if port is None else port
        self.database = database
        self.user = user
        self.passwd = passwd
        self.collection = collection
        self.messages = messages

    def get_connection(self):
        # Provide the Mongodb URI to connect python to Mongo database
        connection_string = f"{self.host}:{self.port}"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient()
        _client = MongoClient(connection_string)

        # Create the database
        return _client

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

    def close(self):
        # Close the connection
        self.get_connection().close()


if __name__ == "__main__":
    try:
        messages_file = json.load(open(f"{module_path.parent.absolute()}/output/messages.json", "r"))
    except FileNotFoundError as e:
        raise e

    client = Mongo(
        host=os.environ["MONGO_URI"],
        port=os.environ["MONGO_PORT"],
        user=os.environ["MONGO_USER"],
        passwd=os.environ["MONGO_PASSWD"],
        messages=messages_file
    )
    try:
        client.send_messages()
        print("Messages sent successfully!")
    except Exception as e:
        print(e)

    client.close()
