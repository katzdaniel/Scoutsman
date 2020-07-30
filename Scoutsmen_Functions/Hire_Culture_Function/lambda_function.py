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
    file_name = 'hire_culture.json'
    lambda_path = "/tmp/" + file_name
    s3_path = cur_dt + '/' + file_name

    data = scrape()
    encoded_data = data.encode('utf-8')

    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_data)
    
    
def scrape():
    base_url = 'https://www.hireculture.org/'
    web_page_url = 'https://www.hireculture.org/findjob.aspx'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    }

    r = requests.get(web_page_url, headers=headers)
    tree = html.fromstring(r.text)
    jobs = tree.xpath('//tr')[1:]

    jobs_list = list()

    for job in jobs:
        try:
            attrs = [i for i in job.xpath('.//td') if str(i.xpath('.//text()')).strip() != '']

            job_dict = dict()

            job_dict['title'] = str(attrs[1].xpath('./a/text()')[0]).strip()
            job_dict['employer'] = str(attrs[2].xpath('./a/text()')[0]).strip()
            job_dict['posted'] = str(attrs[0].xpath('./text()')[0]).strip()
            job_dict['url'] = base_url + str(attrs[1].xpath('./a/@href')[0]).strip() 

            job_r = requests.get(job_dict['url'], headers=headers)
            job_page_tree = html.fromstring(job_r.text)
            
            job_dict['type'] = '-'

            job_dict['address'] = dict()
            add_dict = job_dict['address']

            job_desc = job_page_tree.xpath('//div[@class="content-left"]//p[1]//text()')
            add_dict['street'] = str(job_desc[0]).strip()

            second_line = str(job_desc[1]).strip()
            city, state_and_zip = second_line.split(',')
            add_dict['city'] = city.strip()

            state, zip_code = state_and_zip.strip().split()
            add_dict['state'] = state.strip()
            add_dict['zip'] = zip_code.strip()
            add_dict['country'] = 'United States'
            
            jobs_list.append(job_dict)

            sleep(uniform(0,3))
        
        except Exception:
            pass


    return str(json.dumps(jobs_list))
