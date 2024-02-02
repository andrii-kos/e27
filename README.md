# E27 Scrapy Startup Scraper

### Getting Started

1. Run the following command to scrape all startup URLs and save them in the "startup_urls.csv" file:
    ```scrapy crawl startup_urls```
    
    - Additionally you can scrap startup URLs by using sitemap files, to do this use the following command:
    ```scrapy crawl startup_urls_sitemap```
2. To scrape startup details for a random number of URLs from the "startup_urls.csv" file, use the following command:
    ```scrapy crawl startup_details```
    
    - To adjust the number of URLs to be scraped, modify the "NUM_URLS_TO_GRAB" variable in settings file.

3. The results will be saved in the "startup_details.csv" file.