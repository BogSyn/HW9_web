import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote

if __name__ == "__main__":

    # Завантаження авторів з JSON-файлу
    with open("authors.json", encoding="utf-8") as fd:
        data = json.load(fd)  # Зчитування даних з JSON
        for el in data:
            try:
                author = Author(
                    fullname=el.get("fullname"),
                    born_date=el.get("born_date"),
                    born_location=el.get("born_location"),
                    description=el.get("description"),
                )
                author.save()  # Збереження автора в БД
            except NotUniqueError:
                print(f"Автор вже існує {el.get('fullname')}")

    # Завантаження цитат з JSON-файлу
    with open("quotes.json", encoding="utf-8") as fd:
        data = json.load(fd)  # Зчитування даних з JSON
        for el in data:
            author, *_ = Author.objects(fullname=el.get("author"))
            quote = Quote(quote=el.get("quote"), tags=el.get("tags"), author=author)
            quote.save()  # Збереження цитати в БД
