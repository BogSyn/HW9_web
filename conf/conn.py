import pathlib

import configparser

from mongoengine import connect

# Шлях до конфігураційного файлу
file_config = pathlib.Path(__file__).parent.joinpath("config.ini")

# Читання конфігурації
config = configparser.ConfigParser()
config.read(file_config)

# Параметри з'єднання з MongoDB
mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

# Формування URI
uri = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
print(uri)

# З'єднання з MongoDB
connection = connect(host=uri, ssl=True)

# Перевірка приєднання до БД
if __name__ == "__main__":
    try:
        cn = connect(host=uri, ssl=True)
        print("Successfully connected to MongoDB!")

        db = cn.get_database(db_name)
        collection_names = db.list_collection_names()
        print(f"Collections in database '{db_name}': {collection_names}")

    except Exception as e:
        print(e)
