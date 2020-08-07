# -*- encoding: utf-8 -*-

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from ItemCollectorPipeline import ItemCollectorPipeline
from datetime import datetime
import logging
import sys, getopt
import json
import json_lines
import threading
import queue
import time
import os

from dou import Dou
from douSection import DouSection
from loadingWheel import loadingWheel
from loadingBar import loadingBar

try:
    opts, args = getopt.getopt(sys.argv[1:], "l:", ["log="])
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

levelLogging = getattr(logging, opts[0][1].upper()) if opts and opts[0][0] in ("-l", "--log") else logging.INFO

logName = "log/log-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
logging.basicConfig(handlers=[logging.FileHandler(logName, 'w', 'utf-8')], level=levelLogging, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

# create a crawler process with the specified settings
runner  = CrawlerRunner(
    {
        'USER_AGENT': 'scrapy',
        'LOG_STDOUT': False,
        'LOG_ENABLED': True,
        'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 }
    }
)

def extractNumberPage(obj):
	return obj["numberPage"]

def readUrls(urls):
    with open('diario-oficial-da-uniao.jl', 'rb') as f:
        for item in json_lines.reader(f):
            urls.append(item["url"])

def readSections():
    douSection = []
    with open('secoes-diario-oficial-da-uniao.jl', 'rb') as f:
        for item in json_lines.reader(f):
            douSection.append(item)
    return sorted(douSection, key = extractNumberPage)
    

@defer.inlineCallbacks
def crawl():

    queueData1 = queue.Queue()
    queueData1.put(True)
    t1 = threading.Thread(target=loadingWheel, args=(queueData1, "Fetching DOU from 06-08-2020 "))
    t1.start()
    yield runner.crawl(Dou, data="06-08-2020", secao="do3")
    queueData1.put(False)
    yield t1.join()

    urls = []
    yield readUrls(urls)

    queueData2 = queue.PriorityQueue()
    queueData2.put(0)
    t2 = threading.Thread(target=loadingBar, args=(queueData2, len(urls), "Building sections "))
    t2.start()
    yield runner.crawl(DouSection, queue=queueData2, start_urls=urls)
    queueData2.put(len(urls) * -1)
    yield t2.join()
    reactor.stop()

crawl()
reactor.run()  # the script will block here until the last crawl call is finished

douSection = readSections()

os.remove("secoes-diario-oficial-da-uniao.jl") 
os.remove("diario-oficial-da-uniao.jl")

f = open(file="result.json", mode="w", encoding="utf-8")
f.write(json.dumps(douSection, ensure_ascii=False, indent=4))