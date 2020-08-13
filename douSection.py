import scrapy
from scrapy.selector import Selector
import logging

# your spider
class DouSection(scrapy.Spider):
    name = "secoes-diario-oficial-da-uniao"
    consumer_queue = None
    itemScrapped = 0

    def __init__(self, queue, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.consumer_queue = queue

    def parse(self, response):
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

        url = response.request.url
        yield {
            "numberPage": int(numberPage),
            "artType": artType,
            "title": title,
            "paragraphs": '\n'.join(paragraphs),
            "url": url
        }

        self.itemScrapped += 1
        self.consumer_queue.put(self.itemScrapped * -1)