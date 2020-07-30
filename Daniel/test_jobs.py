import requests

def scrape():
    web_page_url = 'https://www.hireculture.org/findjob.aspx'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
}

    r = requests.get(web_page_url, headers=headers)

    raw_text = str(r.content)

    with open('jobs_test.html', 'w') as f:
        f.write(raw_text)

scrape()
