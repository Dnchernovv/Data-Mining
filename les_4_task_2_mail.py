import requests
from lxml import html
from pprint import pprint
from datetime import datetime
import re
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

db = client['Mail_news']

news_mail = db.news_mail

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
url = 'https://news.mail.ru/economics/'

response = requests.get(url, headers = headers)

dom = html.fromstring(response.text)

mail_news = []
months = ['января','февраля', 'марта','апреля','мая','июня',
          'июля','августа','сентябрь','октября','ноября','декабря']
# pprint(response.text)
items = dom.xpath('//div[contains(@class, "newsitem newsitem")]')
# print(items)
for item in items:

    try:
        article = {}
        title = item.xpath('.//a[contains(@class, "newsitem__title")]//text()')
        title = title[0].replace('\xa0', '')
        link = item.xpath('.//a[@class = "newsitem__title link-holder"]/@href')
        date = item.xpath('.//span[@class = "newsitem__param js-ago"]//text()')[0]
        source = item.xpath('.//span[@class = "newsitem__param"]//text()')[0]
        article['Название новости'] = title
        article['Ссылка'] = link
        article['Источник'] = source
        article['Время публикации'] = date
        if ':' in date:
            article['Дата публикации'] = str(datetime.today())
        else:
            article['Дата публикации'] = f'{datetime.today().year}-{months.index(date[date.find(" ") + 1::]) + 1}-{date[0:2]}'
    except(IndexError):
        pass
    news_mail.insert_one(article)
    mail_news.append(article)

pprint(mail_news)
# //div[contains(@class, "item")]