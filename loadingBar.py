import sys
import time
from queue import Queue

def loadingBar(consumer_queue, _sentinel, count, prefix="", size=60):   
    time.sleep(1)
    j = 0
    while True:
        if not consumer_queue.empty():
            data = consumer_queue.get(block = False)
            if data < 0:
                data *= -1

            if data > j:
                j = data

            if data >= count: 
                x = int(size*j/(count - 1))
                sys.stdout.write("%s: complete!\r" % (prefix))
                sys.stdout.flush()
                sys.stdout.write('\n')
                break

            x = int(size*j/(count - 1))
            sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size - x), j, count - 1))
            sys.stdout.flush()
        else:
            time.sleep(1)

    
