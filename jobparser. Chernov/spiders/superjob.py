import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://korolev.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response):

        # в рамках этого метода будет прописана логика обработки полученного нами response
        # при этом сам паук запускается через консоль
        # в любом случае в объект response приходит dom структура
        # теперь нас буду интересовать ссылки на вакансии

        vacancies_links = response.xpath('//div[contains(@class, "iJCa5 f-test-vacancy-item")]/div/div/div/div/div/a/@href').extract()
        # с помощью метода extract получаем содержимое ссылки
        next_page = response.xpath('//a[contains(@class, "f-test-button")]').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)
        #     response.follow() передает управление в другой метод

    def vacancy_parse(self, response):
        name = response.css('h1::text').extract()
        min_salary = ''
        max_salary = ''
        currency = ''
        salary = response.xpath('//span[@class = "_1h3Zg _2Wp8I _2rfUm _2hCDz"]/text()').extract()
        link = response.url
        site_name = 'superjob.ru'
        yield JobparserItem(name = name, salary = salary, link = link, site_name = site_name,
                            min_salary = min_salary, max_salary = max_salary,currency = currency)
