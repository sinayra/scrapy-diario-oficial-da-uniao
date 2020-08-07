import sys
import time
from queue import Queue

def loadingWheel(consumer_queue, message) :
    chars = "/—\|" 
    time.sleep(1)
    while True :

        for char in chars:
            sys.stdout.write('\r' + message + char)
            time.sleep(.1)
            sys.stdout.flush()
        
        if not consumer_queue.empty():
            data = consumer_queue.get(block = False)
            if data == False: 
                sys.stdout.write('\r' + message + ': complete!')
                sys.stdout.write('\n')
                sys.stdout.flush()
                break
        else:
            time.sleep(.1)