from pprint import pprint
from pymongo import MongoClient


min_info = int(input('Укажите предпочтительную минимальную зарплату: '))

max_info = int(input('Укажите предпочтительную максимальную запрлату: '))

client = MongoClient('127.0.0.1', 27017)

db = client['hh_superjob']

jobs = db.jobs


for job in jobs.find({'$and':[{'Минимальная зарплата' :{'$gt':min_info-1}}, {'Максимальная зарплата' : {'$lt':max_info}}]}):
    pprint(job)
