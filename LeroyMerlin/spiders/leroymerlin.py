import scrapy
from scrapy.http import HtmlResponse
from shop.items import LeroyItem
from scrapy.loader import ItemLoader
import re

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, q):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={q}']

    def parse(self, response):
        goods_links = response.xpath('//div/div/div[contains(@class,"largeCard")]/a/@href').extract()
        next_page = response.xpath(
            '//div[@class = "s1pmiv2e_plp"]/a[contains(@class, "bex6mjh")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

    def parse_good(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        chars_names = []
        chars_values = []
        chars = {}
        for i in response.xpath('//dl[@class = "def-list"]'):
            for j in i.xpath('//dt[@class = "def-list__term"]/text()').extract():
                chars_names.append(j)
        for i in response.xpath('//dl[@class = "def-list"]'):
            for j in i.xpath('//dd[@class = "def-list__definition"]/text()').extract():
                chars_values.append(j)
        loader.add_xpath('price','//uc-pdp-price-view[@class = "primary-price"]/span[@slot = "price"]/text()')
        loader.add_xpath('photos','//img[@slot = "thumbs"]/@src')
        loader.add_value('chars_names', chars_names)
        loader.add_value('chars_values', chars_values)
        loader.add_value('chars',chars)
        loader.add_xpath('name','//h1[@class = "header-2"]/text()')
        loader.add_value('link',response.url)
        loader.add_xpath('currency','//uc-pdp-price-view[@class = "primary-price"]/span[@slot = "currency"]/text()')
        loader.add_xpath('unit','//uc-pdp-price-view[@class = "primary-price"]/span[@slot = "unit"]/text()')
        yield loader.load_item()

