
import scrapy


class nhadat24hSpider(scrapy.Spider):
    name = "123nhadatviet"
    allowed_domains = ['123nhadatviet.com']
    start_urls = ['https://123nhadatviet.com/rao-vat/can-ban/nha-dat/t1/ha-noi.html']

    custom_settings = {
        'FEEDS': {
            '/home/dev/Downloads/result/encode.json': {'format': 'json', 'overwrite': True}
        }
    }


    def parse(self, response):
        listbds = response.css('div.content-items div.content-item')
        for bds in listbds:
            yield {
                'url': "https://123nhadatviet.com" + bds.css('div.text div.ct_title a::attr(href)').get(),
                'title': response.css('div.text div.ct_title a::text').get(),
                'detail': response.css('div.text div.ct_brief::text').getall(),
                'price': response.css('div.text div div.ct_price::text').get(),
                'square': response.css('div.text div.ct_dt::text').get()
            }
