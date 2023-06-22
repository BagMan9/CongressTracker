from SenatePreD import scrapeSenate
from HousePreD import scrapeHouse
from DataGet import houseDataDownload, senateDataDownload
import json
from operator import itemgetter
import os


def recordParse(data):
    if data["Role"] == "H":
        location = "HouseReps"
        filetype = "pdf"
        downloaded = False
        pathstring = f'./{location}/{data["Name"]}/TO-PARSE/{data["Document"]}-{data["FilingDate"]}.{filetype}'  # noqa: E501
        if not os.path.exists(pathstring):
            recordData = houseDataDownload(
                data["Document"], data["FilingDate"][:4]
            )
            downloaded = True
    if data["Role"] == "S":
        location = "SenateReps"
        filetype = "html"
        downloaded = False
        pathstring = f'./{location}/{data["Name"]}/TO-PARSE/{data["Document"]}-{data["FilingDate"]}.{filetype}'  # noqa: E501
        if not os.path.exists(pathstring):
            recordData = senateDataDownload(data["Document"])
            downloaded = True

    if not os.path.exists(f"./{location}/{data['Name']}"):
        os.makedirs(f'./{location}/{data["Name"]}')
        os.makedirs(f'./{location}/{data["Name"]}/TO-PARSE')
    if downloaded:
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
