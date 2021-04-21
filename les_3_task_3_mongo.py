from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs
import re




client = MongoClient('127.0.0.1', 27017)

db = client['hh_superjob']

jobs = db.jobs


position = (str(input('Укажите интересующую вас вакансию: ')))

url = 'https://hh.ru'

params = {'clusters': 'true',
          'enable_snippets': 'true','salary': '','st': 'searchVacancy','text': position,
          'area':0}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params = params, headers = headers)


dom = bs(response.text, 'html.parser')


vacancies = dom.find_all('div', {'class':'vacancy-serp-item'})


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
            if '–' in compensation:
                max_salary = int(compensation[compensation.find('–')+2:compensation.rfind(' ')])
                min_salary = int(compensation[0:compensation.find(' ')])
            elif 'от' in compensation:
                min_salary = int(compensation[compensation.find(' ')+1:compensation.rfind(' ')])
                max_salary = None
            elif 'до' in compensation:
                max_salary = int(compensation[compensation.find(' ') + 1:compensation.rfind(' ')])
                min_salary = None
            else:
                max_salary = None
                min_salary = None
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
        vac_data['Минимальная зарплата'] = min_salary
        vac_data['Максимальная зарплата'] = max_salary
        vac_data['Валюта'] = currency
        vac_data['Местоположение'] = location
        jobs.update_one(vac_data, {'$set': vac_data}, upsert=True)
        next_page = dom.find('a', {'data-qa': "pager-next"}, {'class': 'bloko-button'})
    if next_page != None:
        next_link = next_page['href']
        response = requests.get(url + next_link, headers=headers)
        dom = bs(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
        continue
    else:
        break


params = {'keywords': position}
url = 'https://www.superjob.ru'

response = requests.get(url + '/vacancy/search', headers = headers, params = params)
dom = bs(response.text, 'html.parser')


vacancies = dom.find_all('div', {'class': "iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL"})

while True:
    for v in vacancies:
        try:
            vac_data = {}
            link_vacancy = 'https://www.superjob.ru' + v.find('a')['href']
            vacancy = v.find('div', {'class': "_3mfro PlM3e _2JVkc _3LJqf"}).getText()
            employer = v.find('span',{'class':"_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI"}).getText()
            vacancy_salary = v.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})
            salary = vacancy_salary.getText().replace("\xa0", " ").split(' ')
            if '—' in salary:
                min_salary = salary[0] + salary[1]
                max_salary = salary[3] + salary[4]
            elif 'от' in salary:
                min_salary = salary[1] + salary[2]
                max_salary = None
            elif 'до' in salary:
                max_salary = salary[1] + salary[2]
                min_salary = None
            else:
                max_salary = None
                min_salary = None
            location = dom.find('span',{'class':"_3mfro f-test-text-company-item-location _9fXTd _2JVkc _2VHxz"}).getText()
            location = location[location.rfind(' ')::].lstrip()
            link_1 = v.find('div', {'class':"_3mfro PlM3e _2JVkc _3LJqf"})
            link = link_1.findChildren()[0]['href']
            currency = ''
        except(AttributeError):
            pass
        try:
            currency = salary[salary.rfind('р')::]
        except:
            pass
        vac_data['Название вакансии'] = vacancy
        vac_data['Ссылка на вакансию'] = link_vacancy
        vac_data['Работодатель'] = employer
        vac_data['Валюта'] = currency
        vac_data['Местоположение'] = location
        vac_data['Минимальная зарплата'] = min_salary
        vac_data['Максимальная зарплата'] = max_salary
        jobs.update_one(vac_data, {'$set': vac_data}, upsert=True)
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