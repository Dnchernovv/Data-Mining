import requests
from lxml import html
from pprint import pprint
import re
from pymongo import MongoClient
import datetime


client = MongoClient('127.0.0.1', 27017)

db = client['Yandex_news']

news = db.news

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
url = 'https://yandex.ru/news'

response = requests.get(url, headers = headers)

dom = html.fromstring(response.text)

yandex_news = []

# pprint(response.text)
items = dom.xpath('//article[contains(@class,"mg-card")]')
# print(items)
for item in items:
    article = {}
    title = item.xpath('.//h2[@class = "mg-card__title"]//text()')[0]
    title = title.replace('\xa0', '')
    link = item.xpath('.//a[@class = "mg-card__link"]/@href')[0]
    date = item.xpath('.//span[@class = "mg-card-source__time"]//text()')[0]
    source = item.xpath('.//a[@class = "mg-card__source-link"]//text()')[0]
    article['Название новости'] = title
    article['Ссылка'] = link
    article['Источник'] = source
    article['Время публикации'] = date
    article['Дата публикации'] = str(datetime.date.today())
    news.insert_one(article)
    yandex_news.append(article)

pprint(yandex_news)