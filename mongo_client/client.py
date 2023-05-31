"""
    Este código servirá para conectar no servidor do Atlas para enviar uma
    requisição HTTP e retornar a resposta mostrando todos os documentos dentro
    da conexão feita neste script.
    
    Ainda é uma versão básica de teste de conexão e será atualizada
    de tempos em tempos.
    
    Versão: dev-0.1

    Update: 0.1
    - Adicionada verificação de erro de conexão com o bando de dados;
    - Adicionada documentação;
    - Adicionado variáveis default na classe (SRV, HOST e PORT);
    - Adicionado arg srv no método __init__;
    - Adicionado condições de type para os args: host, port e srv;
    - Connection_string agora é uma junção de host, user, passwd, srv e port;
    - Adicionado método de close connection na classe e no fim do código.
"""
import os
import json
import time
from pathlib import Path
# Load the environment variables from the virtual environment
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure
)
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
    HOST = "mongodb://{}:{}@{}"
    PORT = 27017
    SRV = "mongo"

    def __init__(
            self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            srv: Optional[str] = None,
            user: Optional[str] = "",
            passwd: Optional[str] = "",
            database: str = "track",
            collection: str = "data",
            messages: list = None
     ) -> None:
        """
        :Parameters:
            - `host` (opcional): nome do host ou IP para conectar ao servidor ou
              banco de dados (default=mongodb://{}:{}@{}).
            - `port` (opcional): número da porta que será conectada.
            - `srv` (opcional): nomenclatura do servidor em que o client tentará conectar
              (default="mongo").
            - `user` (opcional): usuário com o acesso ao banco de dados (pode
              ser nulo).
            - `passwd` (opcional): senha do usuário (pode ser nulo).
            - `database`: nome do banco de dados que o client irá conectar
              (default="track").
            - `collection`: nome da coleção que o client irá conectar
              (default="data").
            - `messages`: uma lista com mensagens em formato dict contendo
              o conteúdo que será inserido dentro da coleção.
        """
        if not isinstance(host, str):
            if host is None:
                self.host = self.HOST
            elif type(host) != str:
                raise TypeError("O host precisa ser em tipo string.")
        else:
            self.host = host

        if not isinstance(port, int):
            if port is None:
                self.port = self.PORT
            elif type(port) != int:
                raise TypeError("A port precisa ser do tipo int.")
        else:
            self.port = port

        if not isinstance(srv, str):
            if srv is None:
                self.srv = self.SRV
            elif type(srv) != str:
                raise TypeError("O srv precisa ser do tipo string.")
        else:
            self.srv = srv

        self.database = database
        self.user = user
        self.passwd = passwd
        self.collection = collection
        self.messages = messages

    def get_connection(self):
        """
        Fornece conexão com o servidor mongo

        Retorna a conexão com o servidor, se não for possível conectar irá retornar um erro.
        """
        # Provide the Mongodb URI to connect python to Mongo database
        connection_string = self.host.format(self.user, self.passwd,
                                             self.srv)
        connection_string = f"{connection_string}:{self.port}"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient()
        try:
            _client = MongoClient(connection_string)
        except ConnectionFailure as connection_error:
            raise connection_error

        # Create the database
        return _client

    def get_database(self):
        """
        Conecta com o banco de dados passado no arg no método __init__ usando
        o objeto criado no método get_connection.
        """
        # Get the connection from the previous function and call the database which we will want to get information
        database = self.get_connection()[self.database]

        return database

    def get_collection(self):
        """
        Conecta na coleção passada no arg no método __init__ usando o objeto
        criado no método get_database.
        """
        # Get the collection from the database that we call previously
        collection = self.get_database()[self.collection]

        return collection

    def get_messages(self):
        """
        Retorna todas as mensagens da coleção usando o objeto do método
        get_collection.
        """
        # Returning all messages from the collection
        # Obs: it needed iterate from this object to collect the messages
        return self.get_collection().find()

    def send_messages(self):
        """
        Envia as mensagens armazenas no arg `messages` passado no método __init__
        """
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

    try:
        client = Mongo(
            host=os.environ["MONGO_URI"],
            port=int(os.environ["MONGO_PORT"]),
            srv=os.environ["MONGO_SRV"],
            user=os.environ["MONGO_USER"],
            passwd=os.environ["MONGO_PASSWD"],
            messages=messages_file
        )
        print(f"[{time.strftime('%I:%M:%S %p')}] Started connection.")
    except ConnectionFailure as e:
        print(f"[{time.strftime('%I:%M:%S %p')}] Connection Fail... Error: {e}")

    try:
        client.send_messages()
        print(f"[{time.strftime('%I:%M:%S %p')}] Messages sent successfully!")

        client.close()
        print(f"[{time.strftime('%I:%M:%S %p')}] Connection closed.")
    except Exception as e:
        print(f"[{time.strftime('%I:%M:%S %p')}] Error: {e}")

