from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
# важно! если папка с парсером находится не сразу после корневой директории, то нужно будет
# прописать путь
# нам также нужно будет прописать путь до нашего паука

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    # setmodule парсит наш файл с настройками и создает файл с настройками для нашего паука

    process = CrawlerProcess(settings = crawler_settings)
    process.crawl(HhruSpider)

    process.start()
# именно это стоит за автоматической реализацией