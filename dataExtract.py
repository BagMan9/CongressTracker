import os
import glob
import re
from bs4 import BeautifulSoup


def extractTransactions():
    houseRecords = glob.iglob("./HouseReps/*/TO-PARSE/*")
    senateRecords = glob.iglob("./SenateReps/*/TO-PARSE/*")
    for record in senateRecords:
        if os.path.basename(record).startswith("_ptr_"):
            with open(record, "r") as file:
                data = BeautifulSoup(file, "html.parser")
                data_tree = data.tbody.find_all("tr")
                for item in data_tree:
                    index = 0
                    for child in item.children:
                        formatted = re.sub(
                            "(?s)\\s(?!\\w)|<.*?>|<a.*?>",
                            "",
                            str(child),
                        )
                        formatted = formatted.strip(" ")
                        print(formatted)


if __name__ == "__main__":
    extractTransactions()
