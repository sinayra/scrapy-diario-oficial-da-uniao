import sys, getopt
import logging
from datetime import datetime

try:
    opts, args = getopt.getopt(sys.argv[1:], "l:", ["log="])
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

levelLogging = getattr(logging, opts[0][1].upper()) if opts and opts[0][0] in ("-l", "--log") else logging.DEBUG

root = logging.getLogger()
root.setLevel(levelLogging)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)ss')
handler.setFormatter(formatter)
root.addHandler(handler)
