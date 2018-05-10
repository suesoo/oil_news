# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OilNewsItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()
    title = scrapy.Field()
    datetime = scrapy.Field()
    brief = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()

