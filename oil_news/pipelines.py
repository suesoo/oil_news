# -*- coding: utf-8 -*-

# from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
# from scrapy.conf import settings
# from scrapy.exceptions import DropItem
# from scrapy import log
from mysql.connector import connection, Error
from w3lib.html import remove_tags, remove_tags_with_content
import logging
import datetime

logging.basicConfig(filename='/home/bunker/scraping/oil_news/log/log.txt', level=logging.DEBUG)

# Define your item pipelines here
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
        self.conn = connection.MySQLConnection(host='130.1.12.241', user='root', password='!pan123', database='oil_news')
        self.cursor = self.conn.cursor()
        print('db connection success1')

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        print('==================spider.name:', spider.name)
        # try:
        issue_datetime = ''
        for word in item['datetime']:
            issue_datetime += word
        print('---------title:', issue_datetime)

        title = ''
        for word in item['title']:
            title += remove_tags(word)
        title = title.strip()
        print('---------title:', title)

        link = ''
        for word in item['link']:
            link += word
        print('---------link:', link)

        # for word in item['brief']:
        #     brief += word
        # brief = remove_tags(brief)
        # print('---------brief:', brief)

        content = ''
        for word in item['content']:
            content += word
        # content = content.replace('</p>', '\n')
        content = remove_tags(remove_tags_with_content(content, ('script',)))
        content = content.replace('   ', '')
        content = content.replace('\t', '')
        content = content.replace('\n\n', '\n')
        content = content.replace('&nbsp;', ' ')
        content = content.replace('&amp;', '')
        brief = content[:300]
        brief += '......'

        this_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        args = (item['company'], title, issue_datetime, link, brief, content, this_time)

        if spider.name in ['info', 'ed']:
            query = """INSERT INTO local (company, title, issue_date, link, brief, contents, record_date) 
                         VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        elif spider.name in ['bb', 'rt']:
            query = """INSERT INTO abroad (company, title, issue_date, link, brief, contents, record_date) 
                         VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        try:
            self.cursor.execute(query, args)
            self.conn.commit()
        except Error as err:
            if err.args[0] == 1062:
                print('news already stored!')
            else:
                print("Error %d: %s" % (err.args[0], err.args[1]))
        return item


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
