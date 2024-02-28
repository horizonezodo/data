import scrapy
import spiderConfig

class BdsSpider(scrapy.Spider):
    
    name = f"{spiderConfig.name}"
    allowed_domains = [f'{spiderConfig.allowed_domains}']
    start_urls = [spiderConfig.start_urls]

    custom_settings = {
        'FEEDS': {
            'E:/output.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
        listbds = response.css(f'{spiderConfig.listbds}')
        for bds in listbds:
            url_value = spiderConfig.url_value
            title_value = spiderConfig.title_value
            detail_value = spiderConfig.detail_value
            price_value = spiderConfig.price_value
            square_value = spiderConfig.square_value
            yield {
                'url': url_value,
                'title': title_value,
                'detail': detail_value,
                'price': price_value,
                'square': square_value
            }
