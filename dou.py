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
        urls = []
        sel = Selector(response)
        extracted  = sel.xpath("//script[@type='application/json']/text()").extract_first()
        json_data = json.loads(extracted)
        jsonArray = json_data["jsonArray"]
        for item in jsonArray:
            url = "https://www.in.gov.br/en/web/dou/-/" + item["urlTitle"]
            yield scrapy.Request(url, callback=self.parseSection)

    def parseSection(self, response):
        sel = Selector(response)
        douElem = sel.xpath("//article[@id='materia']")
        
        artType = douElem.xpath("//span[@class='orgao-dou-data']/text()").extract_first()
        title = douElem.xpath("//p[@class='identifica']/text()").extract_first()
        paragraphs = douElem.xpath("//p[@class='dou-paragraph']/text()").extract()
        page = douElem.xpath("//span[@class='secao-dou-data']/text()").extract_first()
        url = response.request.url
        yield {
            "page": int(page),
            "artType": artType,
            "title": title,
            "paragraphs": '\n'.join(paragraphs),
            "url": url
        }