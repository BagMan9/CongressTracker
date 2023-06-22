import requests
from SenatePreD import senCookiesGrab


def houseDataDownload(document, year):
    r = requests.get(
        f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{document}.pdf",  # noqa: E501
        allow_redirects=True,
    )
    return r.content


def senateDataDownload(document):
    document = document.replace("_", "/")
    with requests.Session() as s:
        csrf, sessionID = senCookiesGrab()
        s.cookies.set("csrftoken", csrf)
        s.cookies.set("sessionid", sessionID)
        s.cookies.set(
            "4dd8606008541c48d75e8c09ec4bea1b",
            "b640d74ff4e588a9a8d4d0b626bf4bf6",
        )
        r = s.get(f"https://efdsearch.senate.gov/search/view{document}/")
        return r.content
