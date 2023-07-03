import os
import json
from operator import itemgetter
import pickle


def isDownloaded(record):
    # Returns True if the file is downloaded, False otherwise
    if record["Role"] == "H":
        location = "HouseReps"
        filetype = "pdf"
    elif record["Role"] == "S":
        location = "SenateReps"
        filetype = "html"
    pathstring = f'./{location}/{record["Name"]}/TO-PARSE/{record["Document"]}-{record["FilingDate"]}.{filetype}'  # noqa: E501
    filestored = os.path.exists(pathstring)
    parsed = isParsed(record["Document"])
    if filestored and parsed:
        if not os.path.exists(f"./{location}/{record['Name']}/PARSED"):
            os.makedirs(f'./{location}/{record["Name"]}/PARSED')
        os.replace(pathstring, pathstring.replace("TO-PARSE", "PARSED"))
    if filestored or parsed:
        return True
    else:
        return False


def updateParsed():
    old_json = json.loads(open("./DataWork/Record_Map.json", "r").read())
    newParsedList = []
    for entry in old_json:
        newParsedList.append(entry["Document"])
    if not os.path.exists("./DataWork/Parsed.p"):
        with open("./DataWork/Parsed.p", "wb") as output:
            pickle.dump(newParsedList, output)

    with open("./DataWork/Parsed.p", "rb") as input:
        parsedList = pickle.load(input)
    parsedList = parsedList + newParsedList
    parsedList = list(set(parsedList))
    with open("./DataWork/Parsed.p", "wb") as output:
        pickle.dump(parsedList, output)


def isParsed(docID):
    if os.path.exists("./DataWork/Parsed.p"):
        with open("./DataWork/Parsed.p", "rb") as input:
            parsedList = pickle.load(input)
        if docID in parsedList:
            return True
        else:
            return False
    else:
        return False


def dataCheck(record):
    if record["Date"] == "NEEDS OVERRIDE":
        return False
    else:
        return True


def updateMerge(dataPath, newData, sortKey):
    if not os.path.exists(dataPath):
        with open(dataPath, "w") as output:
            output.write(json.dumps(newData, indent=4))

    Data = json.loads(open(dataPath, "r").read())
    Data = Data + newData
    Data = [dict(t) for t in set(tuple(d.items()) for d in Data)]
    Data = sorted(Data, key=itemgetter(sortKey), reverse=True)
    with open(dataPath, "w") as output:
        output.write(json.dumps(Data, indent=4))
    return Data
