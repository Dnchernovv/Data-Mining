#сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

db = client['mail_letters']

mails = db.mails


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru/')

login = driver.find_element_by_name('login')
login.send_keys('study.ai_172')

login.send_keys(Keys.ENTER)

time.sleep(2)
password = driver.find_element_by_name('password')
password.send_keys('NextPassword172')

password.send_keys(Keys.ENTER)

time.sleep(10)


letters = driver.find_elements_by_xpath("//a[contains(@class, 'js-letter-list-item')]")


senders = []
# //span[@class = "gAclTCd"]
while True:
    letters = driver.find_elements_by_xpath("//a[contains(@class, 'js-letter-list-item')]")
    for letter in letters:
        info = {}
        sender = letter.find_element_by_xpath(".//div/div/div/span[@title]").text
        sending_time = letter.find_element_by_xpath(".//div/div/div[@title]").text
        title = letter.find_element_by_xpath('.//div/div/div/span/span').text
        main_window = driver.current_window_handle
        letter.send_keys(Keys.CONTROL + Keys.RETURN)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)
        text = []
        full_message = driver.find_elements_by_xpath('//tbody/tr/td')
        for i in full_message:
            text.append(i.text)
        text = ' '.join(text)
        driver.close()
        driver.switch_to.window(main_window)
        info['Отправитель'] = sender
        info['Время отправления'] = sending_time
        info['Тема письма'] = title
        info['Полный текст'] = text
        mails.update_one(info, {'$set': info}, upsert=True)
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1])
    actions.perform()
    if info['Время отправления'] == '23 фев':
        break


pprint(senders)
