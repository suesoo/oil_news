# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Bloomberg(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    datetime = scrapy.Field()
    brief = scrapy.Field()
    link = scrapy.Field()
    contest = scrapy.Field()


class OilNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
