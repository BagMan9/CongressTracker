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
                                f"{formatted}-{os.path.basename(record)[:-5]}"
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
                    if transaction_Data["Security Type"] == "Stock":
                        Extracted_Records.append(transaction_Data)
    Extracted_Records = json.loads(json.dumps(Extracted_Records))
    return Extracted_Records


def extractHouse():
    houseRecords = glob.iglob("./HouseReps/*/TO-PARSE/*")

    Extracted_Records = []
    for record in houseRecords:
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
                        )[-14:-4]
                        transaction_Data["ID"] = (
                            f"{pg_num}-{ID}-{os.path.basename(record)[:-4]}"
                        )
                        data = parseTable(item, pg_num, ID)
                        if data and data != "NEEDS OVERRIDE":
                            transaction_Data["Date"] = data[0]
                            transaction_Data["Owner"] = data[1]
                            transaction_Data["Ticker"] = data[2]
                            transaction_Data["Asset"] = data[3]
                            transaction_Data["Security Type"] = data[4]
                            transaction_Data["Sale Type"] = data[5]
                            transaction_Data["Amount"] = data[6]
                            Extracted_Records.append(transaction_Data)
                        elif data == "NEEDS OVERRIDE":
                            transaction_Data["Date"] = data
                            transaction_Data["Owner"] = data
                            transaction_Data["Ticker"] = data
                            transaction_Data["Asset"] = data
                            transaction_Data["Security Type"] = data
                            transaction_Data["Sale Type"] = data
                            transaction_Data["Amount"] = data
                            Extracted_Records.append(transaction_Data)
                        ID += 1

                pg_num += 1
    Extracted_Records = json.loads(json.dumps(Extracted_Records))
    return Extracted_Records


def parseTable(item, pg, row):
    pg = pg
    row = row
    ownerDict = {
        "SP": "Spouse",
        "JT": "Joint",
        "DC": "Child",
    }
    saleDict = {
        "S": "Sale(Full)",
        "S(partial)": "Sale(Partial)",
        "P": "Purchase",
        "E": "Exchange",
    }
    amtDict = {
        "1001": "$1,001-$15,000",
        "15001": "$15,001-$50,000",
        "50001": "$50,001-$100,000",
        "100001": "$100,001-$250,000",
        "250001": "$250,001-$500,000",
        "500001": "$500,001-$1,000,000",
        "1000001": "$1,000,001-$5,000,000",
        "5000001": "$5,000,001-$25,000,000",
        "25000001": "$25,000,001-$50,000,000",
        "50000001": "$50,000,001-$100,000,000",
        "100115000": "$1,001 - $15,000",
    }
    if item[0] != "ID":
        if item[1] is None:
            cell = str(item[0])
            cell = cell.replace("\n", "").replace("\x00", "")
            cell = re.split(r"(?<!T)F S", cell)
            cell = cell[0]
            try:
                if re.search(r"(?<=\[).*(?=\])", item[0]).group() != "ST":
                    return False
            except AttributeError:
                return False
            if len(cell) <= 50:  # Bandaid, fix later
                if pg > 0 and row == 1:
                    return "NEEDS OVERRIDE"
                else:
                    return False
            owner = ownerDict.get(cell[:2], "Self")
            date = datetime.datetime.strptime(
                re.search(r"\d{2}/\d{2}/\d{4}", cell).group(), "%m/%d/%Y"
            ).date()
            date = str(date.isoformat())
            ticker = re.search(r"(?<=\().{1,6}(?=\))", cell).group()
            sale_type = re.search(r" P | S \(partial\)| S | E ", cell).group()
            sale_type = sale_type.replace(" ", "")
            sale_type = saleDict.get(sale_type, "Error")
            amount = re.search(
                r"\$.*(?= -)|\$\d{1,3}(,)?(?(1)\d+\.\d{,2}|\.\d{,2})", cell
            ).group()
            amount = re.sub(r"\D", "", amount)
            amount_map = amtDict.get(amount, amount)
            asset = "--"
            security = "Stock"
            return [
                date,
                owner,
                ticker,
                asset,
                security,
                sale_type,
                amount_map,
            ]
        else:
            actualData = []
            for cell in item:
                if cell is not None and cell != "":
                    cell = cell.replace("\n", "").replace("\x00", "")
                    actualData.append(cell)
            if len(actualData) > 4:
                for i in range(0, 3):
                    try:
                        isStock = re.search(
                            r"(?<=\[).*(?=\])", actualData[i]
                        ).group()
                    except AttributeError:
                        isStock = None
                    if isStock is not None:
                        break
                if isStock != "ST":
                    return False
                else:
                    offset = i - 1
                    if offset == -1:
                        owner = "Self"
                    else:
                        owner = ownerDict.get(actualData[0 + offset], "Self")
                    date = datetime.datetime.strptime(
                        actualData[3 + offset], "%m/%d/%Y"
                    ).date()
                    date = str(date.isoformat())
                    ticker = re.search(
                        r"(?<=\().{1,6}(?=\))", actualData[1 + offset]
                    ).group()
                    asset = "--"
                    security = "Stock"
                    sale_type = saleDict.get(
                        actualData[2 + offset].replace(" ", ""), "Error"
                    )
                    amount = actualData[5 + offset]
                    return [
                        date,
                        owner,
                        ticker,
                        asset,
                        security,
                        sale_type,
                        amount,
                    ]
            else:
                return False


if __name__ == "__main__":
    print(json.dumps(extractHouse(), indent=4))
    print(json.dumps(extractSenate(), indent=4))
