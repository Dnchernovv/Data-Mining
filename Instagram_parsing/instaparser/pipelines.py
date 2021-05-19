# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from instaparser.items import User_Item
from instaparser.items import Subscriber_Item
from instaparser.items import Subcriptions_Item

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.insta_database

    def process_item(self, item,spider):
        if isinstance(item, User_Item):
            return self.handleUser(item)
        elif isinstance(item, Subscriber_Item):
            return self.handleSubsriber(item)
        elif isinstance(item, Subcriptions_Item):
            return self.handleSubscription(item)
        return item

    def handleUser(self, item):
        collection = self.mongo_base['User']
        collection.insert_one(item)

    def handleSubsriber(self, item):
        collection = self.mongo_base['Subscribers']
        collection.insert_one(item)

    def handleSubscription(self,item):
        collection = self.mongo_base['Subscriptions']
        collection.insert_one(item)

