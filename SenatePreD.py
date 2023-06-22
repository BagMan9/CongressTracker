import re
import requests
import subprocess
import json
import datetime


def senCookiesGrab():
    csrfGrab = requests.get(
        "https://efdsearch.senate.gov/search/home/",
    )
    permCSRF = csrfGrab.cookies["csrftoken"]
    tempCSRF = re.search('"\\S{64}"', csrfGrab.text).group()
    tempCSRF = tempCSRF.strip('"')
    curlOut = subprocess.check_output(
        ["sh", "sessionGrab.sh", f"{permCSRF}", f"{tempCSRF}"],
        stderr=subprocess.STDOUT,
    ).decode()
    sessionID = re.search("\\S{47}:\\S{6}:\\S{27}", curlOut).group()
    return permCSRF, sessionID


def scrapeSenate():
    permCSRF, sessionID = senCookiesGrab()
    cookies = {
        "csrftoken": permCSRF,
        "4dd8606008541c48d75e8c09ec4bea1b": "b640d74ff4e588a9a8d4d0b626bf4bf6",
        "sessionid": sessionID,
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "DNT": "1",
        "Origin": "https://efdsearch.senate.gov",
        "Referer": "https://efdsearch.senate.gov/search/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0"
            " Safari/537.36"
        ),
        "X-CSRFToken": f"{permCSRF}",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": (
            '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'
        ),
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    data = {
        "draw": "3",
        "columns[0][data]": "0",
        "columns[0][name]": "",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "true",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "columns[1][data]": "1",
        "columns[1][name]": "",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "2",
        "columns[2][name]": "",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "true",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "columns[3][data]": "3",
        "columns[3][name]": "",
        "columns[3][searchable]": "true",
        "columns[3][orderable]": "true",
        "columns[3][search][value]": "",
        "columns[3][search][regex]": "false",
        "columns[4][data]": "4",
        "columns[4][name]": "",
        "columns[4][searchable]": "true",
        "columns[4][orderable]": "true",
        "columns[4][search][value]": "",
        "columns[4][search][regex]": "false",
        "order[0][column]": "4",
        "order[0][dir]": "desc",
        "start": "0",
        "length": "50",
        "search[value]": "",
        "search[regex]": "false",
        "report_types": "[11]",
        "filer_types": "[1]",
        "submitted_start_date": "01/01/2012 00:00:00",
        "submitted_end_date": "",
        "candidate_state": "",
        "senator_state": "",
        "office_id": "",
        "first_name": "",
        "last_name": "",
    }

    PTRTable = requests.post(
        "https://efdsearch.senate.gov/search/report/data/",
        cookies=cookies,
        headers=headers,
        data=data,
    )
    PreDownSen = []
    data_json = json.loads(PTRTable.text)
    for member in data_json["data"]:
        member_data = {}
        member_data["Name"] = f"{member[1]}-{member[0]}"
        member_data["Role"] = "S"
        doc_link = re.search(
            "\\S{8}-\\S{4}-\\S{4}-\\S{4}-\\S{12}", member[3]
        ).group()
        doc_format = re.search("/ptr/|/paper/", member[3]).group()
        doc_format = doc_format.replace("/", "_")
        member_data["Document"] = f"{doc_format}{doc_link}"
        date_string = member[4]
        date = datetime.datetime.strptime(date_string, "%m/%d/%Y").date()
        member_data["FilingDate"] = date.isoformat()
        PreDownSen.append(member_data)
    PreDownSen = json.dumps(PreDownSen)
    return PreDownSen


if __name__ == "__main__":
    output = scrapeSenate()
    print(json.dumps(output, indent=4))
