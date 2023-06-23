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
                data_tree = data.tbody.tr.children
                index = 0
                for child in data_tree:
                    for string in child.stripped_strings:
                        print(child.parent.name)
                        if index > 8:
                            index = 0
                        if index == 0:
                            print("ID")
                        if index == 1:
                            print("Date: ", string)
                        if index == 2:
                            print("Owner: ", string)
                        if index == 3:
                            print("Ticker: ", string)
                        if index == 4:
                            print("Asset: ", string)
                        if index == 5:
                            print("Type: ", string)
                        if index == 6:
                            print("Sale Type: ", string)
                        if index == 7:
                            print("Amount: ", string)
                        if index == 8:
                            print("Comments: ", string)
                        index += 1


if __name__ == "__main__":
    extractTransactions()
