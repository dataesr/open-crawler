# open-crawler

## Description
(TODO)

## Installation
(TODO)

## Environment variables
# This is an environment variable to set with the path of the scrappy settings.py file as value in order for scrapy to use the custom settings 
SCRAPY_SETTINGS_MODULE=open_crawler.crawler.settings

# Careful of the order of the middlewares !

## Usage
Launch open_crawler.api.main and open_crawler.celery_broker.main
Execute a POST request to http://127.0.0.1:9000/crawl with a body
{
    "url": "https://www.unistra.fr",
    "depth": 2,
    "limit": 20,
    "headers": {"foo":"bar"}
}
url: Url from which to start the crawl
depth: Maximum allowed depth for the crawler
limit: Maximum allowed pages to scrape (value of 0 is not handled yet)
headers: Dictionary containing key/value pairs to add in the headers of each requests