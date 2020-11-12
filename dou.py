import scrapy
from scrapy.selector import Selector
import logging
import json

class Dou(scrapy.Spider):
    name = "diario-oficial-da-uniao"
    base_url="https://www.in.gov.br/leiturajornal"
    data=""
    secao=""

    def __init__(self, data, secao):
        self.data = data
        self.secao = secao

    def start_requests(self):
        url = self.base_url + "?data=" + self.data + "&secao=" + self.secao
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        urls = []
        sel = Selector(response)
        extracted  = sel.xpath("//script[@id='params']/text()").extract_first()
        json_data = json.loads(extracted)
        jsonArray = json_data["jsonArray"]
        for item in jsonArray:
            url = "https://www.in.gov.br/en/web/dou/-/" + item["urlTitle"]
            yield {
                "url" : url
            }
