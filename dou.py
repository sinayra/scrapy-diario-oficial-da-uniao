import scrapy
from scrapy.selector import Selector
import logging
import json

# your spider
class Dou(scrapy.Spider):
    name = "quotes"
    base_url="https://www.in.gov.br/leiturajornal"
    data=""
    secao=""

    def __init__(self, data, secao):
        self.data = data
        self.secao = secao
        logging.getLogger('scrapy.core.scraper').addFilter(lambda x: not x.getMessage().startswith('Scraped from'))

    def __str__(self):
        return ""

    def start_requests(self):
        url = self.base_url + "?data=" + self.data + "&secao=" + self.secao
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        results = []
        sel = Selector(response)
        extracted  = sel.xpath("//script[@type='application/json']/text()").extract_first()
        json_data = json.loads(extracted)
        jsonArray = json_data["jsonArray"]
        for item in jsonArray:
            results.append({
                "artType" : item["artType"],
                "url" : "https://www.in.gov.br/web/dou/-/" + item["urlTitle"],
                "title" : item["title"],
                "numberPage" : int(item["numberPage"])
            })
        return results