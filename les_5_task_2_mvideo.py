from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
import time
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient
from selenium.webdriver.common.by import By

client = MongoClient('127.0.0.1', 27017)

db = client['mvideo_products']

mvideo = db.mvideo


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/promo/novinki-tehniki-mark163900062')
# //span[@itemprop = "price"]
# //div[contains(@class,"fl-product-tile c-product-tile")]
# //a[contains(@class, "fl-product-tile-title__link sel-product-tile-title")]
# //span[contains(@class, "fl-product-tile-rating__stars-value")]
# //span[@class = "fl-product-tile-rating__reviews"]

goods = driver.find_elements_by_xpath('//div[contains(@class,"fl-product-tile c-product-tile")]')
catalogue = []

i = 1
while True:
    for good in goods:
        info = {}
        name = good.find_element_by_xpath('.//a[contains(@class, "fl-product-tile-title__link sel-product-tile-title")]').text
        rating = good.find_element_by_xpath('.//span[contains(@class, "fl-product-tile-rating__stars-value")]').text
        number_of_reviews = good.find_element_by_xpath('.//span[@class = "fl-product-tile-rating__reviews"]').text
        price = good.find_element_by_xpath('.//span[@itemprop = "price"]').text
        info['Название товара'] = name
        info['Рейтинг'] = rating
        info['Количество отзывов'] = number_of_reviews
        info['Цена'] = price
        mvideo.insert_one(info)
    try:
        i += 1
        next_page = driver.find_element_by_xpath(f'.//a[@title = "Перейти на страницу {i}"]')
        driver.get(next_page.get_attribute('href'))
        goods = driver.find_elements_by_xpath('//div[contains(@class,"fl-product-tile c-product-tile")]')
    except:
        break
        # time.sleep(15)
        # cookies = driver.find_element_by_xpath('//a[@class = "close"]')
        # cookies.click()

pprint(catalogue)
