import json_lines
import os

def extractNumberPage(obj):
	return obj["numberPage"]

def readDouJLFile(filename, sortByNumberPage=False):
    aux = []
    
    with open(filename, "rb") as f:
        for item in json_lines.reader(f):
            aux.append(item)

    if sortByNumberPage:
        aux = sorted(aux, key = extractNumberPage)

    open(filename, 'w').close()

    return aux