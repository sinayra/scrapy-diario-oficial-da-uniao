import sys
import time
from queue import Queue

def loadingBar(consumer_queue, count, prefix="", size=60):   
    time.sleep(1)
    j = 0
    while True:
        if not consumer_queue.empty():
            data = consumer_queue.get(block = False)
            if data < 0:
                data *= -1

            if data > j:
                j = data
                x = int(size*j/(count))
                sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size - x), j, count))
                sys.stdout.flush()

            if data >= count: 
                sys.stdout.write('\n')
                sys.stdout.flush()
                break
        else:
            time.sleep(1)

    
