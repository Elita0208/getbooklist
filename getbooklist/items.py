# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetbooklistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    score = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    publishdate = scrapy.Field()
    image = scrapy.Field()
