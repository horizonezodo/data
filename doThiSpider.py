from datetime import datetime, timedelta
import scrapy

class doThiSpider(scrapy.Spider):
    name = "dothi"
    allowed_domains = ['dothi.net']
    start_urls = ['https://dothi.net/nha-dat-ban-ha-noi.htm']

    custom_settings = {
        'FEEDS': {
            '/home/dev/Downloads/result/encode.json': {'format': 'json', 'overwrite': True}
        }
    }
    def __init__(self, pass_date_str='', *args, **kwargs):
        super(doThiSpider, self).__init__(*args, **kwargs)
        try:
            self.pass_date = datetime.strptime(pass_date_str, "%d/%m/%Y %H:%M:%S")
        except ValueError:
            self.pass_date = None
        self.stop_extraction = False
        self.last_data_time = datetime.now()

    def parse(self, response):
        now_date = datetime.now()
        listbds = response.css('div.listProduct ul li')

        for bds in listbds:
            url_value = "https://dothi.net" + bds.css('div.desc h3 a::attr(href)').get()
            title_value = bds.css('h3 a.vip2::text').get()
            detail_value = bds.css('div.location strong::text').get()
            price_value = bds.css('div.other div.price::text').getall()[1]
            square_value = bds.css('div.other div.area::text').getall()[1]
            date = bds.css('span.date::text').get()

            if "Hôm nay" in date:
                date_posting = now_date
                print("today")
            elif "Hôm qua" in date:
                difference = timedelta(hours=1)
                date_posting = now_date - difference
            else:
                date = date.strip("\r\n")
                date = date + " 00:00:00"
                date = date.strip()
                date_posting = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
                print("other")
            if self.pass_date is None or date_posting > self.pass_date:
                print(True)
                self.last_data_time = datetime.now()
                yield {
                    'url': url_value,
                    'title': title_value,
                    'detail': detail_value,
                    'price': price_value,
                    'square': square_value,
                    'date': date_posting
                }
            else:
                if (datetime.now() - self.last_data_time).total_seconds() > 600:
                    self.logger.info("No new data found in 10 minutes. Stopping the crawler.")
                    return
                self.stop_extraction = True
                break
        if not self.stop_extraction:
            next_page = response.css('div.pager_controls a::attr(href)').getall()[
                len(response.css('div.pager_controls a::attr(href)').getall()) - 1]
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

