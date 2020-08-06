from scrapy.crawler import CrawlerProcess
from ItemCollectorPipeline import ItemCollectorPipeline
from spider import QuotesSpider
from datetime import datetime
import sys, getopt
import logging
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
process = CrawlerProcess(
    {
        'USER_AGENT': 'scrapy',
        'LOG_LEVEL': 'INFO',
        'LOG_STDOUT': False,
        'LOG_ENABLED': False,
        'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 }
    }
)
process.crawl(QuotesSpider)
process.start()