import requests
import datetime
import boto3
from time import sleep
from random import uniform
import json
from lxml import html

def lambda_handler(event, context):
    cur_dt = datetime.datetime.now().strftime('%Y-%m-%d')   

    bucket_name = 'job-scraper-bucket'
    file_name = 'arts_for_la.json'
    lambda_path = "/tmp/" + file_name
    s3_path = cur_dt + '/' + file_name

    data = scrape()
    encoded_data = data.encode('utf-8')

    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_data)
    

def scrape():
    base_url = 'https://www.artsforla.org/'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    }

    jobs_list = list()

    for i in range(1,10):
        web_page_url = base_url + f'/job_listings?page={i}'

        r = requests.get(web_page_url, headers=headers)
        tree = html.fromstring(r.text)
        jobs = tree.xpath('//div[@id="listing"]')
    
        for job in jobs:
            try:
                job_dict = dict()
    
                job_dict['title'] = str(job.xpath('.//div[@class="span4"][1]/h4/a/text()')[0]).strip()
                job_dict['employer'] = str(job.xpath('.//div[@class="span4"][2]/h4/text()')[0]).strip()
                job_dict['posted'] = str(job.xpath('.//div[@class="span4"][3]/p/text()')[0]).strip()
                job_dict['url'] = base_url + str(job.xpath('.//div[@class="span4"][1]/h4/a/@href')[0]).strip()

                job_dict['type'] = '-'

                job_dict['address'] = dict()
                add_dict = job_dict['address']
    
                add_dict['street'] = '-'

                city_state = str(job.xpath('.//div[@class="span4"][2]/p/strong/text()')[0]).strip()

                city, state = city_state.split(', ')

                add_dict['city'] = city

                add_dict['state'] = state
                add_dict['zip'] = '-'
                add_dict['country'] = 'United States'

                jobs_list.append(job_dict)
    
                sleep(uniform(0,3))
        
            except Exception as e:
                pass
                #print(e)
                #print('moving on to next job')


    return str(json.dumps(jobs_list))
