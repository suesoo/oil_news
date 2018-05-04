import scrapy
from scrapy.selector import Selector
from oil_news.items import OilNewsItem as Item
from selenium import webdriver
import csv
import time


class BloombergSpider(scrapy.Spider):
    name = 'bloomberg'
    allowed_domains = ['https://www.bloomberg.com/']
    start_urls = [
        'https://www.bloomberg.com/search?query=wti+brent'
    ]
    # def start_requests(self):
    #     with open('bloombergcsv') as csv_file:
    #         reader = csv.DictReader(csv_file)
    #         for row in reader:
    #             yield scrapy.Request(row['url'], self.parse_news)

    def parse(self, response):
        news_list = response.xpath('// *[ @ id = "content"] / div / section / section[2] / section[1] / div[3] / div / article / div[1]')
        print('len news list: ',  len(news_list))
        for news in news_list:
            item = Item()
            # item['source'] = sel.xpath('strong/span[@class="info_news"]/text()').extract()[0]
            # item['category'] = '정치'
            item['title'] = news.xpath('h1/a/text()').extract()
            item['datetime'] = news.xpath('div[1]/span[2]/time/text()').extract()
            item['brief'] = news.xpath('div[2]/text()').extract()
            item['link'] = news.xpath('h1/a/@href').extract()
            yield item


class ReutersSpider(scrapy.Spider):
    name = 'rt'
    allowed_domains = ['reuters.com']
    start_urls = [
        'https://www.reuters.com/search/news?blob=crude oil'
    ]

    def parse(self, response):
        news_list = response.xpath('//*[@id="content"]/section[2]/div/div[1]/div[4]/div/div[3]/div')
        for news in news_list:
            item = Item()
            # item['source'] = sel.xpath('strong/span[@class="info_news"]/text()').extract()[0]
            # item['category'] = '정치'
            item['title'] = news.xpath('div/h3/a/text()').extract()
            item['datetime'] = news.xpath('div/h5/text()').extract()
            item['brief'] = news.xpath('div/div/text()').extract()
            item['link'] = news.xpath('div/h3/a/@href').extract()
            if 'BRIEF' in item['title']:
                continue
            yield item


class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['yonhapnews.co.kr/']
    start_urls = [
        'http://www.yonhapnews.co.kr/home09/7091000000.html?query=국제유가%20wti'
    ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome(executable_path="C:\\Users\\suesoo\\oil_news\\oil_news\\chromedriver.exe")
        self.item_list = []

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)
        # html = self.browser.find_element_by_xpath('//*[@id="article_list"]/div[2]/ul/li/a/').get_attribute('outerHTML')
        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        news_list = selector.xpath('//*[@id="article_list"]/div[2]/ul/li')
        for news in news_list:
            print('---------------')
            item = Item()
            item['title'] = news.xpath('a/span[1]/text()').extract()
            item['datetime'] = news.xpath('a/span[2]/span[2]/text()').extract()
            item['brief'] = news.xpath('a/span[2]/span[1]/text()').extract()
            item['link'] = news.xpath('a/@href').extract()
            self.item_list.append(item)
            # print('---------------', item['title'])
            # yield item

        for a_item in self.item_list:
            url = a_item['link'][0]
            print('-------------url:', url)
            self.browser.get(url)
            time.sleep(5)
            html = self.browser.find_element_by_xpath('//*[@id="articleWrap"]/div[2]').get_attribute('outerHTML')
            a_item['content'] = html
            contents = Selector(text=html)
            briefs = contents.xpath('//*[@id="articleWrap"]/div[2]/p')
            con_text = ''
            for i, brief in enumerate(briefs):
                if i < 2:
                    con_text += contents.xpath('/text()').extract()
            item['brief'] = con_text
            print('--------- item[brief]:', item['brief'])
            yield a_item

        # self.browser.quit()


class eDailySpider(scrapy.Spider):
    name = 'edaily'
    allowed_domains = ['edaily.co.kr/']
    start_urls = [
        'http://www.edaily.co.kr/search/E00.html?searchvalue=wti'
    ]

    def parse(self, response):
        news_list = response.xpath('//*[@id="component_template_id_SEARCH_NEWS_SuVAlKkwWDwNcx7"]/div[1]/div/div[2]/ul/li/a/div/strong')
        print('---------------', len(news_list))
        for news in news_list:
            print('---------------')
            item = Item()
            item['title'] = news.xpath('div/strong').extract()
            # item['datetime'] = news.xpath('span[2]/span[2]/text()').extract()
            item['brief'] = news.xpath('div/text()').extract()
            # item['link'] = news.xpath('@href').extract()
            print('---------------', item['title'])
            yield item
