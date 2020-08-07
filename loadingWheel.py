import sys
import time
from queue import Queue

def loadingWheel(consumer_queue, _sentinel, message) :
    chars = "/—\|" 
    time.sleep(1)
    while True :

        for char in chars:
            sys.stdout.write('\r' + message + char)
            time.sleep(.1)
            sys.stdout.flush()
        
        if not consumer_queue.empty():
            data = consumer_queue.get(block = False)
            if data is _sentinel: 
                sys.stdout.write('\r' + message + ': complete!')
                sys.stdout.write('\n')
                sys.stdout.flush()
                break
        else:
            time.sleep(1)