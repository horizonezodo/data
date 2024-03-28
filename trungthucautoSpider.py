from datetime import datetime, timedelta
import scrapy

class otoSpider(scrapy.Spider):
    name = "test1"
    allowed_domains = ['trungthucauto.vn']
    start_urls = ['https://trungthucauto.vn/tim-xe/?tinh-trang=used']

    custom_settings = {
        'FEEDS': {
            '/home/dev/Downloads/result/encode.json': {'format': 'json', 'overwrite': True}
        }
    }

    def __init__(self, pass_date_str='', *args, **kwargs):
        super(otoSpider, self).__init__(*args, **kwargs)
        try:
            self.pass_date = datetime.strptime(pass_date_str, "%d/%m/%Y")
        except ValueError:
            self.pass_date = None
        self.stop_extraction = False
        self.i = 1

    @staticmethod
    def cleanData(String):
        String = String.replace("\n", "")
        String = String.replace("\t", "")
        String = String.replace("\r", "")
        String = String.strip()
        return String

    def parse(self, response):
        listCar = response.css('div.vehica-inventory-v1__results div.vehica-inventory-v1__results__card')

        for car in listCar:
            item_url = car.css('div.vehica-car-card__inner a.vehica-car-card-link::attr(href)').get()
            yield response.follow(item_url, callback=self.parse_car_response)
        if not self.stop_extraction:
            try:
                self.i += 1
                if self.i < 23:
                    next_page = "https://trungthucauto.vn/tim-xe/?tinh-trang=used&trang-hientai={}&sapxep-theo=moi-nhat".format(self.i)
                    yield response.follow(next_page, callback=self.parse)
            except ValueError:
                print("End of list page navigation")

    def parse_car_response(self, response):

        url_value = (''.join(str(e) for e in response.url)).strip()
        title_value = response.css('div.elementor-widget-container div.vehica-car-name::text').get()
        price_value = response.css('div.elementor-widget-container div.vehica-car-price::text').get()
        gear_value = response.css('div.vehica-grid div.vehica-car-attributes__values::text').getall()[4]
        tyle_value = response.css('div.vehica-car-features a::attr(title)').get()
        #date_value = response.css('div.vehica-car-feature span::text').get()
        detail_value = (' '.join(str(e) for e in response.css('div.elementor-widget-container ol li strong::text').getall())).strip()
        now_date = datetime.now().date()
        difference = timedelta(days=(self.i - 1))
        date_posting = now_date - difference
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
