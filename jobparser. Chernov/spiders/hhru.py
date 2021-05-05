import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    # класс паука
    # для начала можно взглянуть в файл с параметрами и дописать в него дополнительные
    # в нашем случае это сделать необходимо
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # разрешенные верхнеуровневые домены - верхним доменом является .ru, нам нужно дойти
    # до следующей точки и взять то, что было до нее
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=Accountant&from=suggest_post']
    # url формируется на основе домена

    def parse(self, response:HtmlResponse):

        # в рамках этого метода будет прописана логика обработки полученного нами response
        # при этом сам паук запускается через консоль
        # в любом случае в объект response приходит dom структура
        # теперь нас буду интересовать ссылки на вакансии

        vacancies_links = response.xpath('//a[@class = "bloko-link HH-LinkModifier"]/@href').extract()
        # с помощью метода extract получаем содержимое ссылки
        next_page = response.css('a.HH-Pager-Control::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)
        #     response.follow() передает управление в другой метод

    def vacancy_parse(self, response:HtmlResponse):
        name = response.css('h1::text').extract_first()
        min_salary = ''
        max_salary = ''
        currency = ''
        salary = response.css('p.vacancy-salary span::text').extract()
        link = response.url
        site_name = 'https://hh.ru/'
        yield JobparserItem(max_salary = max_salary, min_salary = min_salary,name = name,
                            salary = salary, link = link, site_name = site_name,
                            currency = currency)

