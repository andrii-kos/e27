import scrapy
from crawler.items import Startup, StartupLoader, User
import csv
import random
from urllib.parse import urlparse


class StartupDetailsSpider(scrapy.Spider):
    name = 'startup_details'   
    custom_settings = {
        'FEEDS': {'startup_details.csv': {'format': 'csv', 'overwrite': True}}
    }


    def start_requests(self):
        with open('startup_urls.csv', encoding='utf-8', newline='') as file:
            print(self.settings)
            for line in random.choices(list(csv.DictReader(file)), k=self.settings.get('NUM_URLS_TO_GRAB')):
                id_query= urlparse(line['link']).query
                yield scrapy.Request(f'https://e27.co/api/startups/get/view/?{id_query}', callback=self.parse_starup)
        


    def parse_starup(self, response):
        l = StartupLoader(item=Startup(), response=response)
        startups_details = response.json()['data']
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
        yield scrapy.Request(
            f'https://e27.co/api/site_user_startups/site_users/?startup_id={startups_details.get("id")}', 
            callback=self.parse_users,
            meta={
                'loader': l, 
                'startup_id': startups_details.get("id"), 
                'startup_name': startups_details.get('name')
                }
            )

    

    def parse_users(self, response):
        l = response.meta.get('loader')
        startup_id = response.meta.get('startup_id')
        startup_name = response.meta.get('startup_name')
        users = response.json()['data']['site_users']
        l.add_value('employee_range', [
            User({
                'startup_id': startup_id,
                'startup_name': startup_name,
                'user_id': user.get('site_user_id'),
                'name': user.get('name'),
                'headline': user.get('headline'),
                'url': user.get('url')
            }) for user in users])
        l.add_value('founders', [
            User({
                'startup_id': startup_id,
                'startup_name': startup_name,
                'user_id': user.get('site_user_id'),
                'name': user.get('name'),
                'headline': user.get('headline'),
                'url': user.get('url')
            }) for user in users])
        yield l.load_item()
