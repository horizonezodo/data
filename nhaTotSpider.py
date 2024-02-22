import scrapy


class BdsSpider(scrapy.Spider):
    name = "123nhadat"
    allowed_domains = ['123nhadatviet.com']
    start_urls = ['https://123nhadatviet.com/rao-vat/can-ban/nha-dat/t1/ha-noi.html']

    def parse_item_page(self, response):
        yield{
            'url': response.url,
            'title':  response.css('div.property div.title h1::text').get(),
            'seller_user': response.css('div.content div.name::text').get(),
            'seller_phone': response.css('div.fone a::text').getall()[0],
            'detail': response.css('div.property div.detail::text').getall(),
            'price': response.css('tr td.price::text').get(),
            'square': response.css('label#ContentPlaceHolder1_ctl00_lbGiaDienTich label.strong2::text').get(),
        }

    def parse(self, response):
        listbds = response.css('div.content-items div.content-item')
        for bds in listbds:
            relative_url = bds.css('div.ct_title a::attr(href)').get()
            item_url = 'https://123nhadatviet.com' + relative_url
            print(item_url)
            yield response.follow(item_url, callback=self.parse_item_page)

        list_page = response.css('div.page a::attr(href)').getall()
        current_page = response.css('div.page a.active::attr(href)').get()
        index_curren_page = list_page.index(current_page)
        if index_curren_page < len(list_page):
            next_page = list_page[index_curren_page + 1]
            next_page_url = 'https://123nhadatviet.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)
        elif index_curren_page == len(list_page):
            next_page = list_page[index_curren_page]
            next_page_url = 'https://123nhadatviet.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)
