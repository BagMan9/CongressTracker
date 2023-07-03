from SenatePreD import scrapeSenate
from HousePreD import scrapeHouse
from DataGet import houseDataDownload, senateDataDownload
from dataExtract import extractHouse, extractSenate
from validation import isDownloaded, dataCheck, updateMerge, updateParsed
from sqldata import addToDB
import json
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


if os.path.exists("./DataWork/Record_Map.json"):
    updateParsed()


merge = json.loads(scrapeSenate()) + json.loads(scrapeHouse())
Record_JSON = updateMerge("./DataWork/Record_Map.json", merge, "FilingDate")


for record in Record_JSON:
    recordParse(record)

new_raw_transactions = extractSenate() + extractHouse()

raw_transactions = updateMerge(
    "./DataWork/Transactions.json", new_raw_transactions, "Date"
)
raw_transactions = [item for item in raw_transactions if dataCheck(item)]
with open("./DataWork/Transactions.json", "w") as output:
    output.write(json.dumps(raw_transactions, indent=4))
new_to_fix = []
for entry in new_raw_transactions:
    if not dataCheck(entry):
        new_to_fix.append(entry)


to_fix = updateMerge("./DataWork/to_fix.json", new_to_fix, "Filing Date")

addToDB("./DataWork/Transactions.json")
