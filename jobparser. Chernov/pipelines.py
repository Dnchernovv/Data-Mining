# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.vacancies_database
    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary'] = item['salary']
            if '—' in item['salary']:
                item['min_salary'] = item['salary'][0] + item['salary'][1]
                item['max_salary'] = item['salary'][3] + item['salary'][4]
            elif 'от '  and ' до ' in item['salary']:
                item['min_salary'] = item['salary'][1]
                item['max_salary'] = item['salary'][3]
            elif ' до ' in item['salary'] and 'от ' not in item['salary']:
                item['max_salary'] = item['salary'][1]
                item['min_salary'] = 'Не указана'
            elif ' до ' not in item['salary'] and 'от ' in item['salary']:
                item['max_salary'] = item['salary'][1]
                item['min_salary'] = 'Не указана'
            else:
                item['min_salary'] = 'Не указана'
                item['max_salary'] = 'Не указана'
            if isinstance(item['max_salary'],str):
                item['max_salary'] = item['max_salary'].replace('\xa0', ' ')
            if isinstance(item['min_salary'], str):
                item['min_salary'] = item['min_salary'].replace('\xa0', ' ')
            if len(item['salary']) > 1:
                if len(item['salary'][-1]) < 4:
                    item['currency'] = item['salary'][-1]
                else:
                    item['currency'] = item['salary'][-2]
            item.pop('salary')
        elif spider.name == 'superjob':
            if len(item['salary']) == 4:
                item['min_salary'] = item['salary'][0]
                item['max_salary'] = item['salary'][1]
            # elif 'от'  and 'до' in item['salary']:
            #     item['min_salary'] = item['salary'][1]
            #     item['max_salary'] = item['salary'][3]
            elif 'до' in item['salary'] and 'от' not in item['salary']:
                item['max_salary'] = item['salary'][2]
                item['min_salary'] = 'Не указана'
            elif 'до' not in item['salary'] and 'от' in item['salary']:
                item['max_salary'] = 'Не указана'
                item['min_salary'] = item['salary'][2]
            else:
                item['min_salary'] = 'Не указана'
                item['max_salary'] = 'Не указана'
            if isinstance(item['max_salary'],str):
                item['max_salary'] = item['max_salary'].replace('\xa0', ' ')
            if isinstance(item['min_salary'], str):
                item['min_salary'] = item['min_salary'].replace('\xa0', ' ')
            if len(item['salary']) > 1:
                if 'до' in item['salary'] or 'от' in item['salary']:
                    item['currency'] = item['salary'][-1][item['salary'][-1].rfind('р'):item['salary'][-1].rfind('.')]
                else:
                    item['currency'] = 'Не указана'
            item.pop('salary')
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
