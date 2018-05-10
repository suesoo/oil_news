# -*- coding: utf-8 -*-

# from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
# from scrapy.conf import settings
# from scrapy.exceptions import DropItem
# from scrapy import log
from mysql.connector import connection

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


class MySqlPipeline(object):

    def __init__(self):
        self.conn = connection.MySQLConnection(host='130.1.12.38', user='bunker', password='cost', database='oil_news')
        self.cursor = self.conn.cursor()
        print('db connection success1')

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        # try:
        datetime = ''
        for word in item['datetime']:
            datetime += word
        print('---------title:', datetime)

        title = ''
        for word in item['title']:
            title += word
        print('---------title:', title)

        link = ''
        for word in item['link']:
            link += word
        print('---------link:', link)

        brief = ''
        for word in item['brief']:
            brief += word
        print('---------brief:', brief)

        content = ''
        for word in item['content']:
            content += word
        print('---------content:', content)

        args = (item['company'], title, datetime, link, brief, content)
        query = """INSERT INTO local (company, title, issue_date, link, brief, contents) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(query, args)
        self.conn.commit()
        return item
        # except errorcode, e:
        #     print "Error %d: %s" % (e.args[0], e.args[1])


    # def process_item(self, item, spider):
    #     try:
    #         args=(item['title'])
    #         self.cursor.execute("""INSERT INTO example_book_store (book_name, price)
    #                     VALUES (%s, %s)""",
    #                    (item['title'].encode('utf-8'),
    #                     item['link'].encode('utf-8')))
    #         self.conn.commit()
    #     except mysql.connector.error, e:
    #         print "Error %d: %s" % (e.args[0], e.args[1])
    #     return item
