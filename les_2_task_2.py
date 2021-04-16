import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
params = {'keywords': 'Финансист'}
url = 'https://www.superjob.ru'

response = requests.get(url + '/vacancy/search', headers = headers)
dom = bs(response.text, 'html.parser')


vacancies = dom.find_all('div', {'class': "iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL"})
superjob = []

while True:
    for v in vacancies:
        try:
            vac_data = {}
            link_vacancy = 'https://www.superjob.ru' + v.find('a')['href']
            vacancy = v.find('div', {'class': "_3mfro PlM3e _2JVkc _3LJqf"}).getText()
            employer = v.find('span',{'class':"_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI"}).getText()
            salary = v.find('span', {'class': "_1OuF_ _1qw9T f-test-text-company-item-salary"}).getText()
            location = dom.find('span',{'class':"_3mfro f-test-text-company-item-location _9fXTd _2JVkc _2VHxz"}).getText()
            location = location[location.rfind(' ')::].lstrip()
            link_1 = v.find('div', {'class':"_3mfro PlM3e _2JVkc _3LJqf"})
            link = link_1.findChildren()[0]['href']
        except(AttributeError):
            pass
        currency = ''
        try:
            currency = salary[salary.rfind('р')::]
        except:
            pass
        vac_data['Название вакансии'] = vacancy
        vac_data['Ссылка на вакансию'] = link_vacancy
        vac_data['Работодатель'] = employer
        vac_data['Валюта'] = currency
        vac_data['Зарплата'] = salary
        vac_data['Местоположение'] = location
        superjob.append(vac_data)
        next_page = dom.find('a', {'rel': "next"},
                                {'class': "icMQ_ bs_sM _3ze9n f-test-button-dalshe f-test-link-Dalshe"})
    if next_page != None:
        next_link = next_page['href']
        response = requests.get(url + next_link, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
        continue
    else:
        break

print(superjob)

superjob = json.dumps(superjob, ensure_ascii=False)


with open('sup_vacs.json','w', encoding='utf-8') as c:
    c.write(superjob)

