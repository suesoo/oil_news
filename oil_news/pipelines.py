# -*- coding: utf-8 -*-

# from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
# from scrapy.conf import settings
# from scrapy.exceptions import DropItem
# from scrapy import log
# import pymongo

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class OilNewsPipeline(object):
    def process_item(self, item, spider):
        return item


class BBCsvPipeline(object):

    def __init__(self):
        self.file = open("bloomberg.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


