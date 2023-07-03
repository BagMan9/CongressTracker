import os
import json
from operator import itemgetter


def isDownloaded(record):
    # Returns True if the file is downloaded, False otherwise
    if record["Role"] == "H":
        location = "HouseReps"
        filetype = "pdf"
        pathstring = f'./{location}/{record["Name"]}/TO-PARSE/{record["Document"]}-{record["FilingDate"]}.{filetype}'  # noqa: E501
        filestored = os.path.exists(pathstring)
    elif record["Role"] == "S":
        location = "SenateReps"
        filetype = "html"
        pathstring = f'./{location}/{record["Name"]}/TO-PARSE/{record["Document"]}-{record["FilingDate"]}.{filetype}'  # noqa: E501
        filestored = os.path.exists(pathstring)
    if filestored:
        return True
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
