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
    file_name = 'art_jobs.json'
    lambda_path = "/tmp/" + file_name
    s3_path = cur_dt + '/' + file_name

    data = scrape()
    encoded_data = data.encode('utf-8')

    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_data)
    

def scrape():
    base_url = 'https://artjobs.artsearch.us/'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    }

    jobs_list = list()

    for i in range(1,6):
        web_page_url = base_url + f'job/page/{i}/'

        r = requests.get(web_page_url, headers=headers)
        tree = html.fromstring(r.text)
        jobs = tree.xpath('//li[contains(concat(" ",normalize-space(@class)," ")," job ")]')
    
        for job in jobs:
            try:
                job_dict = dict()
    
                job_dict['title'] = str(job.xpath('./dl/dd[@class="title"]//a/text()')[0]).strip()
                job_dict['employer'] = str(job.xpath('.//dl/dd[@class="title"]/strong[2]/text()')).strip()
                job_dict['posted'] = '-'
                job_dict['url'] = str(job.xpath('./dl/dd[@class="title"]//a/@href')[0]).strip()
    
                job_dict['type'] = str(job.xpath('./dl/dd[@class="type"]//text()')[0]).strip()

                job_dict['address'] = dict()
                add_dict = job_dict['address']
    
                add_dict['street'] = '-'
                add_dict['city'] = str(job.xpath('./dl/dd[@class="location"]/strong/text()')[0]).strip()

                state_country = str(job.xpath('./dl/dd[@class="location"]/span/text()')[0]).strip()

                sc_list = state_country.split(', ')
                    

                if len(sc_list) == 2:
                    add_dict['state'] = sc_list[0]
                    add_dict['zip'] = '-'
                    add_dict['country'] = sc_list[1]

                elif len(sc_list) == 1:
                    add_dict['state'] = '-'
                    add_dict['zip'] = '-'
                    add_dict['country'] = sc_list[0]

                else:
                    add_dict['state'] = '-'
                    add_dict['zip'] = '-'
                    add_dict['country'] = '-'

                jobs_list.append(job_dict)
    
                sleep(uniform(0,3))
        
            except Exception as e:
                print(e)
                print('moving on to next job')


    return str(json.dumps(jobs_list))
