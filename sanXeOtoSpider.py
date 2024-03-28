from datetime import datetime, timedelta
import scrapy

class sanXeOtoSpider(scrapy.Spider):
    name = "sanxeoto"
    allowed_domains = ['sanxeoto.com']
    start_urls = ['https://sanxeoto.com/mua-ban-oto']

    custom_settings = {
        'FEEDS': {
            '/home/dev/Downloads/result/encode.json': {'format': 'json', 'overwrite': True}
        }
    }

    def __init__(self, pass_date_str='', *args, **kwargs):
        super(sanXeOtoSpider, self).__init__(*args, **kwargs)
        try:
            self.pass_date = datetime.strptime(pass_date_str, "%d/%m/%y %H:%M")
        except ValueError:
            self.pass_date = None
        self.stop_extraction = False
        self.date = ""

    @staticmethod
    def cleanData(String):
        String = String.replace("\n", "")
        String = String.replace("\t", "")
        String = String.replace("\r", "")
        String = String.strip()
        return String

    def parse(self, response):
        listCar = response.css('div.list_car_1 div.b-items__cars-one')

        for car in listCar:
            self.date = response.css('div.info_car_1 p.time_car::text').get()
            item_url = car.css('header h3.title_list_car a::attr(href)').get()
            yield response.follow(item_url, callback=self.parse_car_response)
        if not self.stop_extraction:
            try:
                next_page = response.css('a[rel="next"]::attr(href)').get()
                if next_page is not None:
                    yield response.follow(next_page, callback=self.parse)
            except ValueError:
                print("End of list page navigation")

    def parse_car_response(self, response):
        now_date = datetime.now()
        url_value = ''.join(str(e) for e in response.url),
        title_value = response.css('div.b-detail__head-title h1::text').get()
        price_value = response.css('div.b-detail__head-price div.b-detail__head-price-num::text').get()
        gear_value = response.css('div.b-detail__main-info-characteristics-one div.b-detail__main-info-characteristics-one-bottom::text').getall()[2]
        tyle_value = response.css('div.b-detail__main-info-characteristics-one div.b-detail__main-info-characteristics-one-bottom::text').getall()[3]
        date_value = self.date
        detail_value = (' '.join(str(e) for e in response.css('div#info1::text').getall())).strip()
        date_posting_value = date_value.strip()
        count = date_posting_value.count("/")
        if count == 2:
            date_posting = datetime.strptime(date_posting_value, "%d/%m/%y %H:%M")
            print("hours")
        elif count == 1:
            date_str = f"{datetime.now().year}/{date_posting_value}"
            ngay_gio = datetime.strptime(date_str, "%Y/%d/%m %H:%M")
            date_posting = ngay_gio.strftime("%d/%m/%Y %H:%M")
            print("days")
        else:
            ngay_hom_nay = datetime.now().date()
            time_obj = datetime.strptime(date_posting_value, "%H:%M").time()
            date_posting = datetime.combine(ngay_hom_nay, time_obj)
            print("other")
        if self.pass_date is None:
            yield {
                'url': url_value,
                'title': self.cleanData(title_value),
                'detail': self.cleanData(detail_value),
                'price': self.cleanData(price_value),
                'gear': self.cleanData(gear_value),
                'type': self.cleanData(tyle_value),
                'date': date_posting
            }
        elif date_posting >= self.pass_date:
            yield {
                'url': url_value,
                'title': self.cleanData(title_value),
                'detail': self.cleanData(detail_value),
                'price': self.cleanData(price_value),
                'gear': self.cleanData(gear_value),
                'type': self.cleanData(tyle_value),
                'date': date_posting
            }
        else:
             self.stop_extraction = True
             return

