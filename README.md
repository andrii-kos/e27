# E27 Scrapy Startup Scraper

### Getting Started

1. Run the following command to scrape all startup URLs and save them in the "startup_urls.csv" file:
    ```scrapy crawl startup_urls```
2. To scrape startup details for a random number of URLs from the "startup_urls.csv" file, use the following command:
    ```scrapy crawl startup_detail```
    
    - To adjust the number of URLs to be scraped, modify the "number_urls_to_choice" variable in the "startup_details_spider.py" file.

3. The results will be saved in the "startup_detail.csv" file.