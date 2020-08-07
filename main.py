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
        'USER_AGENT': 'scrapy',
        'LOG_STDOUT': False,
        'LOG_ENABLED': True,
        'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 }
    }
)

crawlDou(runner, "07-08-2020", "dou3")
reactor.run()  # the script will block here until the last crawl call is finished

if (os.path.exists("secoes-diario-oficial-da-uniao.jl") and os.path.exists("diario-oficial-da-uniao.jl")):
    writeResult("result.json", "secoes-diario-oficial-da-uniao.jl", ["secoes-diario-oficial-da-uniao.jl", "diario-oficial-da-uniao.jl"])
else:
    raise FileNotFoundError("Required files not found. Try again later")
