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
            "33a5c6d97f299a223cb6fc3925909ef7",
            "54d8050c2e30225d042b07c8b7a2bce2",
        )
        r = s.get(f"https://efdsearch.senate.gov/search/view{document}/")
        return r.content
