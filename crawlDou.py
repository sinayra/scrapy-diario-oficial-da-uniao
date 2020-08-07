import queue
import threading
from twisted.internet import reactor, defer

from dou import Dou
from douSection import DouSection
from readJL import readJL
from loadingWheel import loadingWheel
from loadingBar import loadingBar

@defer.inlineCallbacks
def crawlDou(runner, data, secao):

    # get sections urls
    queueData1 = queue.Queue()
    queueData1.put(True)
    t1 = threading.Thread(target=loadingWheel, args=(queueData1, "Fetching DOU from " + data + "  "))
    t1.start()
    yield runner.crawl(Dou, data=data, secao=secao)
    queueData1.put(False)
    yield t1.join()

    urls = []
    aux = readJL("diario-oficial-da-uniao.jl")
    for item in aux:
        urls.append(item["url"])

    # get sections content
    queueData2 = queue.PriorityQueue()
    queueData2.put(0)
    t2 = threading.Thread(target=loadingBar, args=(queueData2, len(urls), "Building sections "))
    t2.start()
    yield runner.crawl(DouSection, queue=queueData2, start_urls=urls)
    queueData2.put(len(urls) * -1)
    yield t2.join()
    reactor.stop()