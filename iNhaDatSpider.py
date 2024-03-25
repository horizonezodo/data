from datetime import datetime, timedelta
import scrapy

class iNhaDatSpider(scrapy.Spider):
    name = "test1"
    allowed_domains = ['i-nhadat.com']
    start_urls = ['https://i-nhadat.com/can-ban-nha-dat.htm']

    custom_settings = {
        'FEEDS': {
            '/home/dev/Downloads/result/encode.json': {'format': 'json', 'overwrite': True}
        }
    }
    def __init__(self, pass_date_str='', *args, **kwargs):
        super(iNhaDatSpider, self).__init__(*args, **kwargs)
        try:
            self.pass_date = datetime.strptime(pass_date_str, "%d/%m/%Y %H:%M:%S")
        except ValueError:
            self.pass_date = None
        self.stop_extraction = False


    def parse(self, response):
        now_date = datetime.now()
        listbds = response.css('div#left div.content-items div.content-item')

        for bds in listbds:
            url_value = "https://i-nhadat.com" + bds.css('div.ct_title a::attr(href)').get()
            title_value = bds.css('div.ct_title a::text').get()
            detail_value = bds.css('div.ct_brief::text').get()
            price_value = bds.css('div.ct_price::text').get()
            square_value = bds.css('div.ct_dt::text').get()
            date = bds.css('div.ct_date::text').get().strip()

            if "Hôm nay" in date:
                date_posting = now_date
                print("today")
            elif "Hôm qua" in date:
                difference = timedelta(hours=1)
                date_posting = now_date - difference
            else:
                date = date + " 00:00:00"
                date = date.strip()
                date_posting = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
                print("other")
            if self.pass_date is None or date_posting > self.pass_date:
                print(True)
                yield {
                    'url': url_value,
                    'title': title_value,
                    'detail': detail_value,
                    'price': price_value,
                    'square': square_value,
                    'date': date_posting
                }
            else:
                self.stop_extraction = True
                break
        if not self.stop_extraction:
            next_page = response.css('div.page a::attr(href)').getall()
            try:
                current_index_page = next_page.index("#")
                if current_index_page != (len(next_page) - 1):
                    next_page_url = "https://i-nhadat.com" + next_page[current_index_page + 1]
                    yield response.follow(next_page_url, callback=self.parse)
            except ValueError:
                print("End of list page navigation")

