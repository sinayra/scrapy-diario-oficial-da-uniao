import scrapy
from scrapy.selector import Selector
import logging

# your spider
class DouSection(scrapy.Spider):
    name = "secoes-diario-oficial-da-uniao"

    def parse(self, response):
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