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
    
    Versão: dev-0
"""
# Load the environment variables from the virtual environment
from dotenv import load_dotenv
load_dotenv()


import os
import MySQLdb
from mongo_client import Mongo


def clean_data():
    ...    


if __name__ == '__main__':
    ...
