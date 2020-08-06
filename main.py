from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from ItemCollectorPipeline import ItemCollectorPipeline
from datetime import datetime
import logging
import sys, getopt
import json_lines

from dou import Dou
from douSection import DouSection

try:
    opts, args = getopt.getopt(sys.argv[1:], "l:", ["log="])
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

levelLogging = getattr(logging, opts[0][1].upper()) if opts and opts[0][0] in ("-l", "--log") else logging.INFO

logName = "log/log-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
logging.basicConfig(filename=logName, level=levelLogging, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

# create a crawler process with the specified settings
runner  = CrawlerRunner(
    {
        'USER_AGENT': 'scrapy',
        'LOG_LEVEL': 'INFO',
        'LOG_STDOUT': False,
        'LOG_ENABLED': False,
        'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 }
    }
)
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(Dou, data="06-08-2020", secao="do3")
    urls = []
    with open('tmp/diario-oficial-da-uniao.jl', 'rb') as f:
        for item in json_lines.reader(f):
            urls.append(item['url'])
    yield runner.crawl(DouSection, start_urls=urls)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished