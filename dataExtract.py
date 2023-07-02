import os
import glob
import re
from bs4 import BeautifulSoup
from pathlib import Path
import datetime
import json
import pdfplumber


def extractSenate():
    Extracted_Records = []
    test_list = []
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
                    transaction_Data["Filing Date"] = os.path.basename(record)[
                        -15:-5
                    ]
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
    Extracted_Records = json.loads(json.dumps(Extracted_Records))
    return Extracted_Records


def extractHouse():
    houseRecords = glob.iglob("./HouseReps/*/TO-PARSE/*")

    Extracted_Records = []
    for record in houseRecords:
        print(record)
        with pdfplumber.open(record) as pdf:
            pg_num = 0
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    ID = 0
                    for item in table:
                        transaction_Data = {}
                        transaction_Data["Name"] = os.path.basename(
                            Path(record).parents[1]
                        )
                        transaction_Data["Filing Date"] = os.path.basename(
                            record
                        )[-15:-5]
                        transaction_Data["ID"] = (
                            f"{pg_num}-{ID}-{os.path.basename(record)}"
                        )
                        ID += 1
                        print(transaction_Data["ID"])
                        parseTable(item, transaction_Data["ID"])

                pg_num += 1


def parseTable(item, ID):
    ID = str(ID)
    pg = int(re.search(r"(?<!.)\d{1,2}", ID).group())
    row = int(re.search(r"(?<=-)\d{1,2}(?!-\d{2}\.pdf|\.pdf|\d)", ID).group())
    ownerDict = {
        "SP": "Spouse",
        "JT": "Joint",
        "DC": "Child",
    }
    if item[0] != "ID":
        if item[1] is None:
            cell = str(item[0])
            cell = cell.replace("\n", "").replace("\x00", "")
            cell = re.split(r"(?<!T)F S", cell)
            cell = cell[0]
            print(cell)
            try:
                if re.search(r"(?<=\[).*(?=\])", item[0]).group() != "ST":
                    return False
            except AttributeError:
                return False
            if len(cell) <= 50:  # Bandaid, fix later
                if pg > 0 and row == 1:
                    print("Expected Error")
                    print(item)
                    return False
                else:
                    print("Unexpected Error")
                    exit(1)
            owner = ownerDict.get(cell[:2], "Self")
            date = datetime.datetime.strptime(
                re.search(r"\d{2}/\d{2}/\d{4}", cell).group(), "%m/%d/%Y"
            ).date()
            date = date.isoformat()
            ticker = re.search(r"(?<=\().{1,6}(?=\))", cell).group()
            print("Date: ", date)
            print("Owner: ", owner)
            print("Ticker: ", ticker)
            print("Security Type: Stock")
            print("Amount: ", re.search(r"\$.*(?= -)", cell).group())
        else:
            for cell in item:
                pass


if __name__ == "__main__":
    extractHouse()
