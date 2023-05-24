from pathlib import Path
# Load the environment variables from the virtual environment
from dotenv import dotenv_values
# from clean_data import clean_data
import MySQLdb
import json

module_path = Path()
config = dotenv_values(f"{module_path.parent.absolute()}/.env")


class DefinitionError(Exception):
    # Raised when trying to create a table that already exists

    def __init__(self, table: str, message="Error: The table '{0}' already exists"):
        self.table = table
        self.message = message.format(self.table)
        super().__init__(self.message)


def _get_connection():
    connection = MySQLdb.connect(
        host="mysql",  # config["HOST"],
        user="root",
        passwd="password"
    )

    def _create_database():
        cursor = connection.cursor()

        cursor.execute(f"""
            CREATE DATABASE IF NOT EXISTS {config["DATABASE"]};
        """)
        cursor.close()

    _create_database()

    return connection


def _create_table(table_name: str, columns: dict) -> None:
    """
    This function it will create the table with the schema that
    we will pass.
    """
    try:
        connection = _get_connection()
        cursor = connection.cursor()

        cursor.execute(f"USE {config['DATABASE']};")

        def convert_tuple(tup):
            """
            This function will convert a tuple in a string.
            """
            string = ""
            for item in tup:
                string += f" {item}"

            return string

        def table_check():
            """
            This function will check in the database if the table
            that will be created already exists.
            """
            cursor.execute(f"""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{table_name}'
            """)

            if cursor.fetchone()[0] == 1:
                raise DefinitionError(table=table_name)

            return True

        # Verifying if the table already exists.
        table_check()

        # This variable is a docstring that will storage the columns
        # and yours data types.
        columns_ = """"""
        for index, obj in enumerate(columns.items()):
            if index != len(columns) - 1:
                columns_ += f"""{convert_tuple(obj)},"""
            else:
                columns_ += f"""{convert_tuple(obj)}"""

        cursor.execute(
            f"""CREATE TABLE {table_name} (
                    {columns_}
                );"""
        )

        cursor.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    file = open(f"{module_path}/mysql/schema/schema.json")
    data = json.load(file)

    _create_table("landing", data)
