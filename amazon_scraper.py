# Test Name: Scoutsmen
from time import sleep
from random import uniform
import csv

from selenium import webdriver
from lxml import html
from fake_useragent import UserAgent

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument(f'--user-agent={UserAgent(cache=False).random}')
driver = webdriver.Chrome('./chromedriver', options=options)

main_url = 'https://amazon.com/'

driver.get(main_url)
driver.find_element_by_id('twotabsearchtextbox').send_keys('Masks\ue007')

sleep(uniform(.5,3.1))

tree = html.fromstring(driver.page_source)
products = tree.xpath('//div[@class="a-section a-spacing-medium"]')

with open('mask_prices.csv', 'w', newline='') as file:

    fieldnames = ['name', 'price', 'num_reviews', 'per_cnt_price', 'url']

    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()

    for i in range(10):

        if i != 0:
            sleep(uniform(.2, .9))
            driver.find_element_by_xpath('//ul[@class="a-pagination"]/li[@class="a-last"]/a').click()
            sleep(uniform(.4, 1.9))
            tree = html.fromstring(driver.page_source)
            products = tree.xpath('//div[@class="a-section a-spacing-medium"]')

        for product in products:
            product_dict = dict()
            product_dict['price'] = ''.join(product.xpath('.//span[@class="a-price"]//text()')[2:])
            product_dict['name'] = product.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text()')[0]
    
            per_cnt_price = product.xpath('.//span[@class="a-size-base a-color-secondary"]/text()')
            product_dict['per_cnt_price'] = per_cnt_price[0] if len(per_cnt_price) > 0 else '-'
    
            product_dict['url'] = main_url + product.xpath('.//a[@class="a-link-normal a-text-normal"]/@href')[0]
            num_reviews = product.xpath('.//span[@class="a-size-base"]/text()')
            product_dict['num_reviews'] = num_reviews[0] if len(num_reviews) > 0 else '0'
    
            csv_writer.writerow(product_dict)
    

driver.quit()
