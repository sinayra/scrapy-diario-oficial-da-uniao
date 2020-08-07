import sys, getopt
import logging
from datetime import datetime

try:
    opts, args = getopt.getopt(sys.argv[1:], "l:", ["log="])
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)

levelLogging = getattr(logging, opts[0][1].upper()) if opts and opts[0][0] in ("-l", "--log") else logging.INFO

logName = "log/log-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
logging.basicConfig(handlers=[logging.FileHandler(logName, 'w', 'utf-8')], level=levelLogging, format='%(asctime)s %(levelname)s %(name)s %(message)s')