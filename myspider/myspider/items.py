# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    stanje = scrapy.Field()
    marka = scrapy.Field()
    model = scrapy.Field()
    godiste = scrapy.Field()
    kilometraza = scrapy.Field()
    karoserija = scrapy.Field()
    gorivo = scrapy.Field()
    kubikaza = scrapy.Field()
    snaga = scrapy.Field()
    menjac = scrapy.Field()
    vrata = scrapy.Field()
    boja = scrapy.Field()
    lokacija = scrapy.Field()
    cena = scrapy.Field()
