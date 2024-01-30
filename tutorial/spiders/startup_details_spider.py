import scrapy
from tutorial.items import Startup, StartupLoader
from urllib.parse import urlparse
import json


class StartupDetails(scrapy.Spider):
    name = 'startup_details'   

    def start_requests(self):
        with open('test.json', encoding='utf-8') as file:
            for line in json.load(file):
                startup_id = urlparse(line['link']).query
                yield scrapy.Request(f'https://e27.co/api/startups/get/view/?{startup_id}', callback=self.parse_starup)
        


    def parse_starup(self, response):
        print(response.body)
        l = StartupLoader(item=Startup(), response=response)
        startups_details = json.loads(response.body).get('data')
        l.add_value('id', startups_details.get("id"))
        l.add_value('company_name', startups_details.get("name"))
        l.add_value('company_website', startups_details.get("website"))
        l.add_value('email', startups_details.get("email"))
        l.add_value('phone', startups_details.get("phone"))
        l.add_value('profile_url', startups_details.get("link"))
        l.add_value('location', startups_details.get("location"))
        l.add_value('market', startups_details.get("market"))
        l.add_value('founding_date', startups_details.get("found_year"))
        l.add_value('founding_date', startups_details.get("found_month"))
        l.add_value('founding_date', startups_details.get("found_day"))
        l.add_value('founders', startups_details.get("founders"))
        l.add_value('employee_range', startups_details.get("employee_range"))
        l.add_value('urls_social', startups_details.get("linkedin"))
        l.add_value('urls_social', startups_details.get("facebook"))
        l.add_value('urls_social', startups_details.get("twitter"))
        l.add_value('urls_social', startups_details.get("instagram"))
        l.add_value('urls_social', startups_details.get("youtube"))
        l.add_value('urls_social', startups_details.get("rss_feed"))
        l.add_value('description_short', startups_details.get("short_description"))
        l.add_value('description', startups_details.get("description"))
        return l.load_item()