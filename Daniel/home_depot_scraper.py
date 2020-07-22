from time import sleep
from random import uniform
from datetime import datetime
import csv

from selenium import webdriver
from lxml import html
from fake_useragent import UserAgent

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument(f'--user-agent={UserAgent(cache=False).random}')
driver = webdriver.Chrome('./chromedriver', options=options)

main_url = 'https://amazon.com/'
search_term = 'Masks'

driver.get(main_url)
driver.find_element_by_id('twotabsearchtextbox').send_keys(search_term+'\ue007')

sleep(uniform(.5,3.1))

tree = html.fromstring(driver.page_source)

