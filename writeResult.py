import os
import json

from readDouJLFile import readDouJLFile

def writeResult(result, fromFile):
    douSection = readDouJLFile(fromFile, sortByNumberPage=True)

    f = open(file=result, mode="w", encoding="utf-8")
    f.write(json.dumps(douSection, ensure_ascii=False, indent=4))

    os.remove(fromFile)