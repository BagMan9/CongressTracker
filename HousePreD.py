import datetime
import urllib.request
import zipfile
import os
import xml.etree.ElementTree as ET
import json


def xmlParse(xmlFile):
    root = ET.parse(xmlFile).getroot()
    data = []
    for member in root.findall("Member"):
        member_data = {}
        date_string = member.find("FilingDate").text

        # Skip this Member if it doesn't have a Date
        if date_string is None:
            continue

        member_data["Last"] = member.find("Last").text
        member_data["First"] = member.find("First").text
        member_data["FilingType"] = member.find("FilingType").text
        member_data["StateDst"] = member.find("StateDst").text
        member_data["Year"] = member.find("Year").text
        member_data["DocID"] = member.find("DocID").text

        date_string = member.find("FilingDate").text
        date = datetime.datetime.strptime(date_string, "%m/%d/%Y").date()
        member_data["FilingDate"] = date.isoformat()

        data.append(member_data)
    return data


def scrapeHouse():
    year = datetime.datetime.now().year
    # Downloading ZIP
    urllib.request.urlretrieve(
        f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.ZIP",  # noqa: E501
        "PreFilter.zip",
    )

    # Unzipping & Deleting ZIP
    with zipfile.ZipFile("PreFilter.zip", "r") as zip_ref:
        zip_ref.extract(f"{year}FD.xml", "./PreProcess/")
    os.remove("PreFilter.zip")

    if os.path.exists("FilteredXML.xml"):
        os.remove("FilteredXML.xml")

    # Filtering XML
    HouseXML = open(f"./PreProcess/{year}FD.xml", "r")
    FilteredXML = open("FilteredXML.xml", "w")
    with HouseXML as input:
        with FilteredXML as output:
            for line in input:
                if "Prefix" not in line and "Suffix" not in line:
                    output.write(line)
    os.remove(f"PreProcess/{year}FD.xml")

    temp_json = xmlParse("FilteredXML.xml")

    PreDownReps = []

    for member in temp_json:
        if member["FilingType"] == "P":
            member_data = {}
            member_data["Name"] = f"{member['Last']}-{member['First']}"
            member_data["Role"] = "H"
            member_data["Document"] = member["DocID"]
            member_data["FilingDate"] = member["FilingDate"]
            PreDownReps.append(member_data)
            print(member["FilingType"])
    PreDownReps = json.dumps(PreDownReps)
    os.remove("FilteredXML.xml")
    return PreDownReps


if __name__ == "__main__":
    print(scrapeHouse())
