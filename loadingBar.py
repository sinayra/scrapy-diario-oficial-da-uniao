import sys
from queue import Queue

def loadingBar(_sentinel, count, consumer_queue, prefix="", size=60):

    while True:
        j = consumer_queue.get()

        if j is _sentinel: 
            consumer_queue.put(_sentinel) 
            break
        x = int(size*j/count) + 1
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size - x), j, count + 1))
        sys.stdout.flush()
    print('\n')
