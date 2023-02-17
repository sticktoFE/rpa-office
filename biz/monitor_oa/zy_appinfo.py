# spider.py
import scrapy
from mytools.general_spider.general_spider.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/js/'
        meta = dict(page_num=1)
        yield scrapy.Request(url=url, meta=meta, callback=self.parse)

    def parse(self, response):
        quote_item = QuoteItem()
        for quote in response.css('div.quote'):
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item
        # 翻页
        meta = response.meta
        meta.update(
            {'usedSelenium': True, 'dont_redirect': True, 'purpose': 'content'})
