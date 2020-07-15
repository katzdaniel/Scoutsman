import scrapy
from ..items import WebscrapeItem

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = ['https://www.amazon.com/s?k=masks+50pcs&ref=nb_sb_noss_1']
    pageNumber = 2

    def parse(self, response):
        items = WebscrapeItem()

        product_name = response.css('.a-color-base.a-text-normal').css('::text').extract()
        product_price = response.css('.a-price-whole::text').extract()

        items['product_name'] = product_name
        items['product_price'] = product_price

        yield items

        nextPage = 'https://www.amazon.com/s?k=masks+50pcs&page=' + str(AmazonSpiderSpider.pageNumber)

        if AmazonSpiderSpider.pageNumber <= 100:
            AmazonSpiderSpider.pageNumber += 1
            yield response.follow(nextPage, callback = self.parse)