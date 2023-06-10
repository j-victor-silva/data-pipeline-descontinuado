import MySQLdb

connection = MySQLdb.connect(
    user="root",
    passwd="root"
)
cursor = connection.cursor()
cursor.execute("USE track")

var = """INSERT INTO landing (
                id,
                name,
                subname
            ) VALUES (
                "3427813fdsa21245gf",
                "joao",
                "victor"
            )"""

cursor.execute(var)
