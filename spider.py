import scrapy
from scrapy.selector import Selector
import json

# your spider
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'https://www.in.gov.br/leiturajornal?data=06-08-2020&secao=do3'

        yield scrapy.Request(url, self.parse)


    def parse(self, response):
        pass
        sel = Selector(response)
        results  = sel.xpath("//script[@type='application/json']/text()").extract_first()
        json_data = json.loads(results)
        jsonArray = json_data["jsonArray"]
        for item in jsonArray:
            yield {
                "artType" : item["artType"],
                "url" : "https://www.in.gov.br/web/dou/-/" + item["urlTitle"],
                "title" : item["title"],
                "numberPage" : int(item["numberPage"])
            }