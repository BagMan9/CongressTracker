from SenatePreD import scrapeSenate
from HousePreD import scrapeHouse
from DataGet import houseDataDownload, senateDataDownload
from validation import isDownloaded
import json
from operator import itemgetter
import os


def recordParse(data):
    downloaded = isDownloaded(data)
    if not downloaded:
        if data["Role"] == "H":
            location = "HouseReps"
            filetype = "pdf"
            recordData = houseDataDownload(
                data["Document"], data["FilingDate"][:4]
            )
        if data["Role"] == "S":
            location = "SenateReps"
            filetype = "html"
            recordData = senateDataDownload(data["Document"])

        if not os.path.exists(f"./{location}/{data['Name']}"):
            os.makedirs(f'./{location}/{data["Name"]}')
            os.makedirs(f'./{location}/{data["Name"]}/TO-PARSE')
        pathstring = f'./{location}/{data["Name"]}/TO-PARSE/{data["Document"]}-{data["FilingDate"]}.{filetype}'  # noqa: E501
        with open(
            pathstring,
            "wb",
        ) as output:
            output.write(recordData)


Record_Map = open("./DataWork/Record_Map.json", "r+")


merge = json.loads(scrapeSenate()) + json.loads(scrapeHouse())


if not os.path.exists("./DataWork/Record_Map.json"):
    with Record_Map as output:
        output.write(json.dumps(merge))

Record_Map = json.loads(Record_Map.read())

New_Record_Map = merge + Record_Map

New_Record_Map = [
    dict(t) for t in set(tuple(d.items()) for d in New_Record_Map)
]

New_Record_Map = sorted(
    New_Record_Map, key=itemgetter("FilingDate"), reverse=True
)

with open("./DataWork/Record_Map.json", "w") as output:
    output.write(json.dumps(New_Record_Map, indent=4))

for record in New_Record_Map:
    recordParse(record)
