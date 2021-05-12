# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose,TakeFirst

def process_photo_links(photo_url):
    correct_url = photo_url.replace('q_90','q_800')
    correct_url = correct_url.replace('w_82', 'w_900')
    correct_url = correct_url.replace('h_82', 'h_900')
    return correct_url
def process_price(price):
    price[0] = int(price[0].replace(' ', ''))
    return price
def process_chars(chars):
    chars = chars.replace('\n',' ')
    chars = chars.strip()
    return chars

class LeroyItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field(input_processor = Compose(process_price),
                         output_processor = TakeFirst())
    currency = scrapy.Field()
    unit = scrapy.Field()
    chars_names = scrapy.Field()
    chars_values = scrapy.Field(input_processor = MapCompose(process_chars))
    chars = scrapy.Field()
    photos = scrapy.Field(input_processor = MapCompose(process_photo_links))
    pass
