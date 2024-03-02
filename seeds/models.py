from bson import json_util
from mongoengine import (
    connect,
    Document,
    StringField,
    ReferenceField,
    ListField,
    CASCADE,
)

from conf.conn import uri

# Модуль конфігурації з'єднання
connect(host=uri, ssl=True)


# Модель автора
class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=75)
    born_location = StringField(max_length=200)
    description = StringField()
    meta = {"collection": "authors"}  # Назва колекції для зберігання


# Модель цитати
class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=200))
    quote = StringField()
    meta = {"collection": "quotes"}  # Назва колекції для зберігання

    # Перетворення документа цитати в JSON
    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)
