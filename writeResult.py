import os
import json

from readJL import readJL

def writeResult(result, fromFile, tmpFiles):
    douSection = readJL(fromFile, True)

    for tmp in tmpFiles:
        os.remove(tmp)

    f = open(file=result, mode="w", encoding="utf-8")
    f.write(json.dumps(douSection, ensure_ascii=False, indent=4))