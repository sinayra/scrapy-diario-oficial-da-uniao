import scrapy
from scrapy.selector import Selector
import logging
import json

class spiderDou(scrapy.Spider):
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
        logger = logging.getLogger(__name__)
        
        sel = Selector(response)
        extracted  = sel.xpath("//script[@id='params']/text()").extract_first()
        json_data = json.loads(extracted)
        jsonArray = json_data["jsonArray"]
        for item in jsonArray:
            url = "https://www.in.gov.br/en/web/dou/-/" + item["urlTitle"]
            yield scrapy.Request(url, self.parse_section)

    def parse_section(self, response):
        logger = logging.getLogger(__name__)

        sel = Selector(response)
        douElem = sel.xpath("//article[@id='materia']")
        
        artType = douElem.xpath("//span[@class='orgao-dou-data']/text()").extract_first()
        
        title = douElem.xpath("//p[@class='identifica']/text()").extract_first()
        if not title:
            logger.debug("Title from " + url + " is different")
            title = douElem.xpath("//h3[@class='titulo-dou']//span/text()").extract_first() 

        paragraphs = douElem.xpath("//p[@class='dou-paragraph']/text()").extract()

        numberPage = douElem.xpath("//span[@class='secao-dou-data']/text()").extract_first()

        yield {
            "numberPage": int(numberPage),
            "artType": artType,
            "title": title,
            "paragraphs": '\n'.join(paragraphs),
            "url": response.url
        }
