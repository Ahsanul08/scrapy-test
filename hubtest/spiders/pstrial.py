import scrapy


class PSSpider(scrapy.Spider):
    name = "pstrial"
    start_urls = [
        'http://pstrial-2017-12-18.toscrape.com/',
    ]

    def parse(self, response):
        pass