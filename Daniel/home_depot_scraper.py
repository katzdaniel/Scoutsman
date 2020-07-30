from time import sleep
from random import uniform
from datetime import datetime
from os.path import getsize
from traceback import format_exc
from json import load, dump


from selenium import webdriver
from lxml import html
from fake_useragent import UserAgent
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument(f'--user-agent={UserAgent().random}')


driver = webdriver.Chrome('./chromedriver', options=options)

main_url = 'https://www.homedepot.com/'
site_name = 'home_depot'
search_term = 'Disposable Masks'

driver.get(main_url)
driver.find_element_by_id('headerSearch').send_keys(search_term+'\ue007')

sleep(uniform(.5,3.1))

tree = html.fromstring(driver.page_source)
products = tree.xpath('//div[@class="a-section a-spacing-medium"]')

file_name = site_name + '_' + search_term + '_prices.json'

products_list = list()

with open(file_name, 'a+') as f:
    try:
        #fieldnames = ['name', 'price', 'review_score', 'num_reviews', 'per_cnt_price', 'url', 'timestamp']
    
        #csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        #csv_writer.writeheader()

        f.seek(0)

        if getsize(file_name) != 0:
            products_list = load(f)
    
        for i in range(20):
    
            if i != 0:
                sleep(uniform(.2, .9))
                driver.find_element_by_xpath('//ul[@class="a-pagination"]/li[@class="a-last"]/a').click()
                sleep(uniform(.4, 1.9))
                tree = html.fromstring(driver.page_source)
                products = tree.xpath('//div[@class="a-section a-spacing-medium"]')
    
            for product in products:
                product_dict = dict()
    
                product_name = str(product.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text()')[0])
                timestamp = str(datetime.now()).split('.')[0]

                existing_product_list = [d for d in products_list if d['name'] == product_name]

                if len(existing_product_list) > 0: 
                    product_dict = existing_product_list[0]

                    #print(list([k.split(' ')[0] for k, v in product_dict['time_based'].items()]))
                    if timestamp.split(' ')[0] in [k.split(' ')[0] for k, v in product_dict['time_based'].items()]:
                        #print('skipped')
                        #print(timestamp.split(' ')[0])
                        #print('\n')
                        continue

                else:
                    products_list.append(product_dict)

                    product_dict['name'] = product_name

                    product_dict['url'] = str(main_url + product.xpath('.//a[@class="a-link-normal a-text-normal"]/@href')[0])
                    
                    product_dict['time_based'] = dict()
                    product_dict['time_based'][timestamp] = dict()

                time_based_dicts = product_dict['time_based'][timestamp]

                time_based_dicts['price'] = str(''.join(product.xpath('.//span[@class="a-price"]//text()')[2:]))
        
                per_cnt_price = product.xpath('.//span[@class="a-size-base a-color-secondary"]/text()')
                time_based_dicts['per_cnt_price'] = str(per_cnt_price[0]) if len(per_cnt_price) > 0 else '-'
        
                review_score = product.xpath('.//span[@class="a-declarative"]/../@aria-label')
                time_based_dicts['review_score'] = str(review_score[0]) if len(review_score) > 0 else '-'
    
                num_reviews = product.xpath('.//span[@class="a-size-base"]/text()')
                time_based_dicts['num_reviews'] = str(num_reviews[0]) if len(num_reviews) > 0 else '0'
    
    except Exception: 
        print(format_exc())
    
with open(site_name + '_' + search_term + '_prices.json', 'w') as f:
    dump(products_list, f, indent=4)

driver.quit()
