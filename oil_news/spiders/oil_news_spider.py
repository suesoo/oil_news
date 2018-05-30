import scrapy
from scrapy.selector import Selector
from oil_news.items import OilNewsItem as Item
from selenium import webdriver
import time


page_time_delay = 5


class BloombergSpider(scrapy.Spider):
    name = 'bb'
    allowed_domains = ['https://www.bloomberg.com/']
    start_urls = [
        'https://www.bloomberg.com/search?query=wti+brent'
    ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome(executable_path="/home/bunker/scraping/oil_news/oil_news/chromedriver")
        self.item_list = []

    def parse(self, response):
        news_list = response.xpath('// *[ @ id = "content"] / div / section / section[2] / section[1] / div[3] / div / article / div[1]')
        print('len news list: ',  len(news_list))
        for news in news_list:
            item = Item()
            item['company'] = 'bloomberg'
            item['title'] = news.xpath('h1/a/text()').extract()
            item['datetime'] = news.xpath('div[1]/span[2]/time/text()').extract()
            item['brief'] = news.xpath('div[2]/text()').extract()
            item['link'] = news.xpath('h1/a/@href').extract()[0]
            # item['content'] = 'test content'
            self.item_list.append(item)

        for a_item in self.item_list:
            url = a_item['link']
            self.browser.get(url)
            time.sleep(page_time_delay)
            news_contents = []
            html = self.browser.find_element_by_xpath('//article').get_attribute('outerHTML')
            selector = Selector(text=html)
            news_contents += selector.xpath('//h1').extract()

            news_1 = selector.xpath('//section').extract()[0]
            selector = Selector(text=news_1)
            news_contents += selector.xpath('//li/div').extract()
            news_contents += selector.xpath('//p').extract()
            a_item['content'] = news_contents
            yield a_item


class ReutersSpider(scrapy.Spider):
    name = 'rt'
    allowed_domains = ['reuters.com']
    start_urls = [
        'https://www.reuters.com/search/news?sortBy=&dateRange=&blob=oil'
    ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome(executable_path="/home/bunker/scraping/oil_news/oil_news/chromedriver")
        self.item_list = []

    def parse(self, response):
        news_list = response.xpath('/html/body/div[3]/section[2]/div/div[1]/div[4]/div/div[3]/div').extract()
        for news in news_list:
            item = Item()
            selector = Selector(text=news)
            item['company'] = 'reuters'
            title = ''
            for word in selector.xpath('//a/text()').extract():
                title += word
            if 'BRIEF' in title:
                continue
            if 'VIDEO RESULTS' in title:
                continue

            item['title'] = title
            item['datetime'] = selector.xpath('//h5/text()').extract()
            # item['brief'] = news.xpath('div/div/text()').extract()
            item['link'] = 'https://www.reuters.com'+selector.xpath('//a/@href').extract()[0]
            self.item_list.append(item)

        for a_item in self.item_list:
            url = a_item['link']
            self.browser.get(url)
            time.sleep(page_time_delay)
            html = self.browser.find_element_by_xpath('/html').get_attribute('outerHTML')
            selector = Selector(text=html)
            news_contents = selector.xpath('//h1').extract()[0]
            news = ''
            for word in selector.xpath('//p').extract():
                news += word
            news_contents += news
            a_item['content'] = news_contents
            yield a_item
        self.browser.quit()


class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['yonhapnews.co.kr/']
    start_urls = [
        'http://www.yonhapnews.co.kr/home09/7091000000.html?query=국제유가%20wti'
    ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome(executable_path="/home/bunker/scraping/oil_news/oil_news/chromedriver")
        self.item_list = []

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(page_time_delay)
        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        news_list = selector.xpath('//*[@id="article_list"]/div[2]/ul/li')

        for news in news_list:
            item = Item()
            item['company'] = 'yonhap'
            item['title'] = news.xpath("a/span[1]").extract()
            item['datetime'] = news.xpath('a/span[2]/span[2]/text()').extract()
            item['link'] = news.xpath('a/@href').extract()[0]
            self.item_list.append(item)

        for a_item in self.item_list:
            url = a_item['link']
            self.browser.get(url)
            time.sleep(page_time_delay)
            html = self.browser.find_element_by_xpath('//*[@id="articleWrap"]/div[2]').get_attribute('outerHTML')
            a_item['content'] = html
            yield a_item
        self.browser.quit()


class eDailySpider(scrapy.Spider):
    name = 'ed'
    allowed_domains = ['www.edaily.co.kr']
    start_urls = [
        'http://www.edaily.co.kr/search/E00.html?searchvalue=%EA%B5%AD%EC%A0%9C%EC%9C%A0%EA%B0%80%20%26%20wti'
    ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome(executable_path="/home/bunker/scraping/oil_news/oil_news/chromedriver")
        self.item_list = []
        self.filter = ['[마감]', '[中증시 마감]', '[외환마감]', '[외환브리핑]']

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(page_time_delay)
        html = self.browser.find_element_by_xpath('/html/body/section/div/div/div[1]/div/div[4]/div/div[1]/div[1]/div/div[2]').get_attribute('outerHTML')
        selector = Selector(text=html)
        li = selector.xpath('//ul/li')
        for news in li:
            item = Item()
            item['company'] = 'eDaily'

            title = ''
            indic = False
            for word in news.xpath('a/div/div/strong').extract():
                title += word
            title = title.replace('<strong>', '')
            title = title.replace('</strong>', '')

            for a_word in self.filter:
                if a_word in title:
                    indic = True
                    break
            if indic:
                continue
            # item['content'] = title
            item['title'] = title + '\n'
            item['datetime'] = news.xpath('a/div/div/div/span[3]/text()').extract()
            item['link'] = 'http://www.edaily.co.kr'+news.xpath('a/@href').extract()[0]
            self.item_list.append(item)

        for a_item in self.item_list:
            url = a_item['link']
            self.browser.get(url)
            time.sleep(page_time_delay)
            html = self.browser.find_element_by_xpath('//*[@id="article_body"]').get_attribute('outerHTML')
            a_item['content'] += html
            yield a_item
        self.browser.quit()
