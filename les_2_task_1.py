import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import json
import pandas as pd


position = (str(input('Укажите интересующую вас вакансию: ')))

url = 'https://hh.ru'

params = {'clusters': 'true',
          'enable_snippets': 'true','salary': '','st': 'searchVacancy','text': position}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params = params, headers = headers)


dom = bs(response.text, 'html.parser')


vacancies = dom.find_all('div', {'class':'vacancy-serp-item'})
hh_ru = []

while True:
    for v in vacancies:
        try:
            vac_data = {}
            vacancy = v.find('a', {'class': 'bloko-link'}).getText()
            link_vacancy = v.find('a', {'class': 'bloko-link'})['href']
            employer = v.find('a', {'class':['bloko-link_secondary']}).getText()
            employer = re.sub('\xa0','',employer)
            compensation = v.findChildren('div',{'class':'vacancy-serp-item__sidebar'})[0].getText()
            location = v.find('span', {'class':'vacancy-serp-item__meta-info'}).getText()
            compensation = re.sub('\u202f','',compensation)
            compensation = re.sub('\xa0', '', compensation)
            currency = ''
        except(AttributeError):
            pass
        try:
            currency = compensation[compensation.rfind(' '):-1] + compensation[-1]
        except:
            pass
        vac_data['Название вакансии'] = vacancy
        vac_data['Ссылка на вакансию'] = link_vacancy
        vac_data['Работодатель'] = employer
        vac_data['Размер з/п'] = compensation
        vac_data['Валюта'] = currency
        vac_data['Местоположение'] = location
        hh_ru.append(vac_data)
    next_page = dom.find('a', {'data-qa': "pager-next"}, {'class': 'bloko-button'})
    if next_page != None:
        next_link = next_page['href']
        response = requests.get(url + next_link, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
        continue
    else:
        break


to_json = json.dumps(hh_ru, ensure_ascii=False)

with open('vacs.json','w', encoding='utf-8') as c:
    c.write(to_json)

hh_ru = pd.DataFrame(hh_ru)

print(hh_ru)