import json_lines

def extractNumberPage(obj):
	return obj["numberPage"]

def readJL(file, sortByNumberPage=False):
    aux = []
    #with open('diario-oficial-da-uniao.jl', 'rb') as f:
    with open(file, "rb") as f:
        for item in json_lines.reader(f):
            aux.append(item)

    if sortByNumberPage:
        aux = sorted(aux, key = extractNumberPage)

    return aux