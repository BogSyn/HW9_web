import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

from pathlib import Path
import json


class QuoteItem(Item):
    """
    Структура елемента даних для цитат, що містить поля для тексту цитати, автора та тегів.
    """

    quote = Field()
    author = Field()
    tags = Field()


class AuthorItem(Item):
    """
    Структура елемента даних для авторів, що містить поля для повного імені, дати народження, місця народження та опису.
    """

    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class DataPipline:
    """
    Складовий елемент Scrapy, що відповідає за обробку та збереження даних.
    """

    quotes = []
    authors = []

    def process_item(self, item, spider):
        """
        Обробляє елемент даних, додаючи його до відповідного списку (цитати або автори).
        """
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append(dict(adapter))
        if "quote" in adapter.keys():
            self.quotes.append(dict(adapter))

    def close_spider(self, spider):
        """
        Закриває павука та зберігає дані у форматі JSON.
        """
        path = Path("seeds")

        with open(path / "quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)
        with open(path / "authors.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=2)


class QuotesSpider(scrapy.Spider):
    """
    Павук Scrapy, що завантажує та обробляє дані з веб-сайту "Quotes to Scrape".
    """

    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {DataPipline: 300}}

    def parse(self, response, **kwargs):
        """
        Парсить головну сторінку, витягує цитати та посилання на сторінки авторів.
        """
        for qt in response.css("div.quote"):
            yield QuoteItem(
                tags=qt.css("div.tags a.tag::text").getall(),
                author=qt.css("small.author::text").get().strip(),
                quote=qt.css("span.text::text").get().strip(),
            )
            yield response.follow(
                url=self.start_urls[0] + qt.css("span a::attr(href)").get(),
                callback=self.parse_author,
            )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    @classmethod
    def parse_author(cls, response, **kwargs):
        """
        Парсить сторінку автора, витягуючи його повне ім'я, дату народження, місце народження та опис.
        """
        content = response.css("div.author-details")
        yield AuthorItem(
            fullname=content.css("h3.author-title::text").get().strip(),
            born_date=content.css("span.author-born-date::text").get().strip(),
            born_location=content.css("span.author-born-location::text").get().strip(),
            description=content.css("div.author-description::text").get().strip(),
        )


if __name__ == "__main__":
    # Запуск та керування павуком
    process = CrawlerProcess()
    # Додавання скраперу до процесу
    process.crawl(QuotesSpider)
    # Запуск процесу
    process.start()
