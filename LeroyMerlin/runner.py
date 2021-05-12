from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from shop.spiders.leroymerlin import LeroymerlinSpider
from shop import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings = crawler_settings)
    # query = input('')
    process.crawl(LeroymerlinSpider, q = 'обои')

    process.start()