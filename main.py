# -*- encoding: utf-8 -*-
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

import loggerConfig

from spiderDou import spiderDou
import os.path

# create a crawler process with the specified settings
runner  = CrawlerRunner(
    {
        'USER_AGENT': 'Sinayra-meuCrawlerComScrapy/1.2 (sinayra@hotmail.com)',
        'LOG_STDOUT': False,
        'LOG_ENABLED': True,
        'ROBOTSTXT_OBEY' : True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 5,
        'RETRY_TIMES' : 5,
        'AUTOTHROTTLE_ENABLED' : True,
        'HTTPCACHE_ENABLED': True,  # for development
        'FEEDS':{
            'results.json': {
                'format': 'json',
                'encoding': 'utf8'
            }   
        },
    }
)

d = runner.crawl(spiderDou, data="07-08-2020", secao="dou3")
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the last crawl call is finished
