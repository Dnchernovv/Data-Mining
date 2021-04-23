import requests
from lxml import html
from datetime import datetime
from pprint import pprint
import re
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)

db = client['Lenta_news']

news_lenta = db.news_lenta

months = ['января','февраля', 'марта','апреля','мая','июня',
          'июля','августа','сентябрь','октября','ноября','декабря']

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
url = 'https://lenta.ru/'

response = requests.get(url, headers = headers)

dom = html.fromstring(response.text)

lenta_news = []

# pprint(response.text)
items = dom.xpath('//div[contains(@class, "item")]')
# print(items)
for item in items:
    article = {}
    title = item.xpath('.//h3/..//text()')
    if len(title) == 1:
        title = title[0].replace('\xa0', '')
    elif len(title) >= 2:
        title = ' '.join(title)
        title = title.replace('\xa0', '')
    else:
        pass
    link = item.xpath('.//div[contains(@class, "titles")]/*/*/@href')
    if len(link) == 1:
        link = link[0]
    date = item.xpath('.//span[contains(@class, "time")]//text()')
    date = item.xpath('.//span[contains(@class, "item__date")]//text()')
    source = 'Lenta.ru'
    article['Название новости'] = title
    if len(link) > 0:
        article['Ссылка'] = 'lenta.ru' + link
    article['Источник'] = source
    if len(date) > 0:
        if ' — ' in date:
            date.pop(date.index(' — '))
        article['Время публикации'] = date[0]
        if date[1] == 'Сегодня':
            article['Дата публикации'] = str(datetime.today().date())
        else:
            article['Дата публикации'] = f'{datetime.today().year}-{months.index(date[1][date[1].find(" ") + 1::]) + 1}-{date[1][0:2]}'

    # news.insert_one(article)
    if len(article['Название новости']) != 0:
        lenta_news.append(article)
        news_lenta.insert_one(article)

pprint(lenta_news)