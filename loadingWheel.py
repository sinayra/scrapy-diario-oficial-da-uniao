import sys
import time
from queue import Queue

def loadingWheel(consumer_queue, _sentinel, message) :
    chars = "/—\|" 

    while True :

        for char in chars:
            sys.stdout.write('\r' + message + char)
            time.sleep(.1)
            sys.stdout.flush()
        
        if not consumer_queue.empty():
            data = consumer_queue.get(block = False)
            if data is _sentinel: 
                consumer_queue.put(_sentinel) 
                break
    sys.stdout.flush()
    sys.stdout.write('\r' + message + ': complete!\n')