import scrapy


class PSSpider(scrapy.Spider):
    name = "pstrial"
    start_urls = [
        'http://pstrial-2017-12-18.toscrape.com/browse/',
    ]

    def parse(self, response):
        category = response.xpath('//div[@id = "subcats"]/div')
        if category:
            for element in category:
                ul_items = element.xpath('ul/li')
                if len(ul_items):
                    for li_elements in ul_items:
                        for link in li_elements.xpath('a/@href').extract():
                            yield scrapy.Request(response.urljoin(link), callback= self.parse)
                else:
                    item_page = element.xpath('a/@href').extarct_first()
                    yield scrapy.Request(response.urljoin(item_page), callback= self.parse)
        else:
            element_list = response.xpath('div[@id="body"]/a/@href').extract()
            links_to_folow = element_list[1:-1]
            pagination = element_list[-1]
            for link in links_to_folow:
                request = scrapy.Request(response.urljoin(link), callback= self.process_each_item)
                request.meta['path'] = response.url
            yield scrapy.Request(response.urljoin(pagination), callback= self.parse)

    def process_each_item(self, response):
        artist_list = response.xpath('//h2/text()').extract_first()
        if artist_list:
            artist_list  = ','.join(i.split(':')[1].strip() for i in artist_list.split(';'))



        yield {
            'url': response.url,
            'artist': artist_list or '',
            'title': response.xpath('//h1/text()').extract_first(),
            'image': response.urljoin(response.xpath('//img/@src').extract_first()),
            'height': '',
            'width': '',
            'description': response.xpath('//div[@itemprop = "description"]/p/text()').extract_first(),
            'path': response.meta['path'].split('/')[4:]
        }

