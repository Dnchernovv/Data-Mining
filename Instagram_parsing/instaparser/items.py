# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class User_Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    user_id = scrapy.Field()
    photo = scrapy.Field()
    likes = scrapy.Field()
    _id = scrapy.Field()

class Subscriber_Item(scrapy.Item):
    user_id = scrapy.Field()
    subscriber_id = scrapy.Field()
    subscriber_name = scrapy.Field()
    subscriber_pic = scrapy.Field()
    _id = scrapy.Field()

class Subcriptions_Item(scrapy.Item):
    user_id = scrapy.Field()
    subscription_id = scrapy.Field()
    subscription_name = scrapy.Field()
    subscription_pic = scrapy.Field()
    _id = scrapy.Field()

