"""
    Este script vai organizar o documento mongo para um padrão em comum
    que será usado para todas as mensagens que serão enviadas para o servidor
    SQL.
    
    Nesta versão ainda não existe um padrão certo, mas servirá de base para as
    próximas versões.
    
    Padrão atual:
        {
            id: hash,
            ip: string,
            user_id: string,
            action: string,
            traits: {
                    name: string,
                    email: string,
                    birthday: string,
                    created_at: timestamp,
                    phone: string,
                    id: string,
                    timezone: string,
                    address: {
                            brand: string,
                            department: string,
                            role: string,
                            permissions: array<string>,
                        },
                    gender: string
            }
            properties: {
                action: string,
                post_id: string,
                post_name: string,
                post_type: string,
                post_description: string,
                post_url: string,
                post_owner: string,
                post_status: string
            }
            browser: {
                    version: string,
                    value: string
                },
            device: {
                type: string,
                token: string,
                enable: bool
            }
            request: {
                    value: string,
                    timestamp: timestamp
                },
            timestamp: timestamp,
            ingestion_at: timestamp
        }

    O que fazer em seguida:
        - Verificar se as mensagens são inseridas corretamente;
        - Criar condição para que mensagens iguais não se repitam.
        
    Versão: dev-0.1
"""
import os
import time
import MySQLdb
from MySQLdb import (
    InternalError
)
from pymongo import MongoClient
from pathlib import Path
from typing import Optional
# Load the environment variables from the virtual environment
from dotenv import dotenv_values

module_path = Path()
config = dotenv_values(f"{module_path.parent.absolute()}/.env")


def get_messages_from_mongo(
        host: Optional[str] = os.environ["MONGO_URI"],
        port: Optional[int] = int(os.environ["MONGO_PORT"]),
        srv: Optional[str] = os.environ["MONGO_SRV"],
        user: Optional[str] = os.environ["MONGO_USER"],
        passwd: Optional[str] = os.environ["MONGO_PASSWD"],
        database: str = "track",
        collection: str = "data"
):
    def get_connection_to_mongo():
        # debug_connection_string = host
        # debug_connection = MongoClient(debug_connection_string)

        connection_string = host.format(user, passwd, srv)
        connection_string = f"{connection_string}:{port}"
        connection = MongoClient(connection_string)

        return connection

    return get_connection_to_mongo()[database][collection].find()


def insert_messages_to_mysql():
    def get_connection_to_mysql():
        try:
            connection = MySQLdb.connect(
                host=config["HOST"],
                user=config["USERNAME"],
                passwd=config["PASSWORD"]
            )
        except:
            raise InternalError(f"[{time.strftime('%I:%M:%S %p')}] Erro: verifique se o host existe e está digitado"
                                f" corretamente, ou então verifique as credenciais.")

        return connection

    cursor = get_connection_to_mysql().cursor()

    try:
        count: int = 0
        for message in get_messages_from_mongo():
            cursor.execute(f"""INSERT INTO landing (
                user_id,
                ip,
                action,
                traits,
                properties,
                browser,
                device,
                request,
                timestamp,
                ingestion_at
            ) VALUES (
                {message["user_id"]},
                {message["ip"]},
                {message["action"]},
                {message["traits"]},
                {message["properties"]},
                {message["browser"]},
                {message["device"]},
                {message["request"]},
                {message["timestamp"]},
                {message["ingestion_at"]}
            )"""
                           )

            count += 1
    except:
        raise

    print(f"[{time.strftime('%I:%M:%S %p')}] {count} linhas adicionadas à tabela `landing`.")


if __name__ == '__main__':
    for i in get_messages_from_mongo():
        print(type(i))
    # insert_messages_to_mysql()
