import scrapy
from crawler.items import StartupUrlItem
from scrapy import Selector

class StartupUrlsChemaSpider(scrapy.Spider):
    name ='startup_urls_sitemap'
    start_urls = [
        "https://e27.co/startup_sitemap_index.xml"
        ]
    custom_settings = {
        'FEEDS': {'startup_urls_sitemap.csv': {'format': 'csv', 'overwrite': True}}
    }


    def parse(self, response):
        sel = Selector(response)
        sel.register_namespace("g", "http://www.sitemaps.org/schemas/sitemap/0.9")
        page_links = sel.xpath("//g:loc//text()").getall()
       
        for link in page_links:
            yield scrapy.Request(link, callback=self.parse_startup_urls)      
    
    

    def parse_startup_urls(self, response):
        startup_link_item = StartupUrlItem()
        sel = Selector(response)
        sel.register_namespace("g", "http://www.sitemaps.org/schemas/sitemap/0.9")
        links = sel.xpath("//g:loc/text()").getall()
        for link in links:
            startup_link_item['link'] = link
            yield startup_link_item
