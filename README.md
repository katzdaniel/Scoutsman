# Scoutsmen
#### A web scraping project.

##### Aim
The aim of this project was to scrape data that is essential during the COVID pandemic. To accomplish this we targeted the prices of products essential during COVID (Masks, Sanitizer, etc) and culture jobs that are being lost. We then wanted to provide the data and an interface to access it.

##### Tech
These are the main tools we used during this project:

- Requests: Python library for http requests.
- Lxml: Python library for parsing html.
- Selenium Webdriver: Python library for scripting a web browser. It is useful for bypassing anti-botting measures.
- AWS Lambda and S3: Cloud services that we used for running scrapers and storing data. S3 was also used for hosting the static websites.

##### Links
[Mask Price Website](https://test-scoutsman-60500037.s3-us-west-1.amazonaws.com/index.html)

[Job Website](https://job-scraper-bucket.s3.us-east-2.amazonaws.com/index.html)

[Job Data Set](https://s3.console.aws.amazon.com/s3/buckets/job-scraper-bucket/?region=us-east-2&tab=overview)


##### Credits

Creating during CodeLabs 2020

By: Nicholas Contreras, Daniel Katz, and Joseph Ngo

Mentor: Quentin Geddes

![Logo](logo.jpg)