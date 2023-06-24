import os
import glob
import re
from bs4 import BeautifulSoup
from pathlib import Path
import datetime
import json


def extractTransactions():
    Extracted_Records = []
    test_list = []
    houseRecords = glob.iglob("./HouseReps/*/TO-PARSE/*")
    senateRecords = glob.iglob("./SenateReps/*/TO-PARSE/*")
    for record in senateRecords:
        if os.path.basename(record).startswith("_ptr_"):
            with open(record, "r") as file:
                data = BeautifulSoup(file, "html.parser")
                data_tree = data.tbody.find_all("tr")
                for item in data_tree:
                    index = 0
                    transaction_Data = {}
                    transaction_Data["Name"] = os.path.basename(
                        Path(record).parents[1]
                    )
                    for child in item.children:
                        formatted = re.sub(
                            "(?s)\\s(?!\\w)|<.*?>|<a.*?>",
                            "",
                            str(child),
                        )
                        formatted = formatted.strip(" ")
                        formatted = re.sub(r"\n", "", formatted)
                        test_list.append(formatted)
                        if index == 0.5:
                            transaction_Data["ID"] = (
                                f"{formatted}-{os.path.basename(record)}"
                            )
                        if index == 1.5:
                            formatted = datetime.datetime.strptime(
                                formatted, "%m/%d/%Y"
                            ).date()
                            transaction_Data["Date"] = formatted.isoformat()
                        if index == 2.5:
                            transaction_Data["Owner"] = formatted
                        if index == 3.5:
                            transaction_Data["Ticker"] = formatted
                        if index == 4.5:
                            transaction_Data["Asset"] = formatted
                        if index == 5.5:
                            transaction_Data["Security Type"] = formatted
                        if index == 6.5:
                            transaction_Data["Sale Type"] = formatted
                        if index == 7.5:
                            transaction_Data["Amount"] = formatted
                        index += 0.5
                    Extracted_Records.append(transaction_Data)
    for record in houseRecords:
        pass
    Raw_Extracted_Records = json.loads(json.dumps(Extracted_Records))


if __name__ == "__main__":
    extractTransactions()
