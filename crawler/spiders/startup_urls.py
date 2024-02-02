import scrapy
from crawler.items import StartupUrlItem
import json


class StartupDetails(scrapy.Spider):
    name = 'startup_urls'
    custom_settings = {
        'FEEDS': {'startup_urls.csv': {'format': 'csv', 'overwrite': True}}
    }
    length = 500
    start_urls = [f'https://e27.co/api/startups/?length={length}&page=1']


    def parse(self, response):
        json_response = json.loads(response.body)['data']
        pages_count = round(json_response['totalstartupcount'] / self.length) 
        startups = json_response['list']

        yield from self.get_startup_urls(startups)

        for page in range(1, pages_count + 1):
            yield scrapy.Request(f'https://e27.co/api/startups/?length={self.length}&page={page}', callback=self.parse_pages)


    def parse_pages(self, response):
        startups = json.loads(response.body)['data']['list']
        yield from self.get_startup_urls(startups)


    def get_startup_urls(self, startups):
        for startup in startups:
            startup_url_item = StartupUrlItem()
            id = startup["id"]
            startup_url_item['id'] = id
            startup_url_item['link'] = f"{startup['link']}"
            yield startup_url_item


