# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from urllib.parse import urlparse
import re
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os

class ShopPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.goods_database
    def process_item(self, item, spider):
        item['chars'] = {}
        for i in range(len(item['chars_values'])):
            item['chars'][item['chars_names'][i]] = item['chars_values'][i]
        item.pop('chars_names')
        item.pop('chars_values')
        collection = self.mongo_base[spider.name]
        collection.insert_one(item, upsert = True)
        return item
class ShopPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                yield scrapy.Request(img)
    def file_path(self, request, response=None, info=None, *, item=None):
        name = item['name']
        return f'files/{item["name"]}/' + os.path.basename(urlparse(request.url).path)