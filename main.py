# -*- encoding: utf-8 -*-
from scrapy.crawler import CrawlerRunner
from ItemCollectorPipeline import ItemCollectorPipeline
from twisted.internet import reactor

import loggerConfig

from crawlDou import crawlDou
from writeResult import writeResult
import os.path

# create a crawler process with the specified settings
runner  = CrawlerRunner(
    {
        'USER_AGENT': 'Sinayra-meuCrawlerComScrapy/1.0 (sinayra@hotmail.com)',
        'LOG_STDOUT': False,
        'LOG_ENABLED': True,
        'ROBOTSTXT_OBEY' : True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 5,
        'RETRY_TIMES' : 5,
        'AUTOTHROTTLE_ENABLED' : True,
        'HTTPCACHE_ENABLED': True,  # for development
        'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 }
    }
)

crawlDou(runner, "07-08-2020", "dou3")
reactor.run()  # the script will block here until the last crawl call is finished

if (os.path.exists("secoes-diario-oficial-da-uniao.jl") and os.path.exists("diario-oficial-da-uniao.jl")):
    writeResult("result.json", "secoes-diario-oficial-da-uniao.jl", ["secoes-diario-oficial-da-uniao.jl", "diario-oficial-da-uniao.jl"])
else:
    raise FileNotFoundError("Required files not found. Try again later")
