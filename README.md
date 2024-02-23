import scrapy

class homdySpider(scrapy.Spider):
    name = "homedy"
    allowed_domains = ['homedy.com']
    start_urls = ['https://homedy.com/ban-nha-dat-ha-noi']

    custom_settings = {
        'FEEDS': {
            '/home/dev/Downloads/result/encode.json': {'format': 'json', 'overwrite': True}
        }
    }
    def parse_item_page(self,response):
        yield {
            'url': response.url,
            'title': response.css('div.product-detail-top-left h1::text').get(),
            'seller_user': response.css('div.name a::text').get(),
            'seller_phone': response.css('div.option a::attr(data-mobile)').get(),
            'detail': response.css('div.description-content div.description p::text').getall(),
            'price':  response.css('div.short-item strong span::text').getall()[0] + "Triệu",
            'square': response.css('div.short-item strong span::text').getall()[1]
        }

    def parse(self, response):
        listbds = response.css('div.tab-content div.product-item')
        for bds in listbds:
            relative_url = bds.css('div.product-item-top a::attr(href)').get()
            item_url = 'https://homedy.com' + relative_url
            yield response.follow(item_url, callback=self.parse_item_page)

        list_page = response.css('div.page-nav ul li a::attr(href)').getall()
        current_page =  response.css('div.page-nav ul li.active a::attr(href)').get()
        index_i = list_page.index(current_page)
        if index_i < len(list_page) and (current_page.find('p2') == -1):
            next_page = list_page[index_i + 1]
            next_page_url = 'https://homedy.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)
        elif index_i == len(list_page):
            next_page = list_page[index_i]
            next_page_url = 'https://homedy.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)
