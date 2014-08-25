import scrapy

class NytimesItem(scrapy.Item):
    headline = scrapy.Field()
    link = scrapy.Field()
    text = scrapy.Field()
    keywords = scrapy.Field()
