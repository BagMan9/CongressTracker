import os


def isDownloaded(record):
    # Returns True if the file is downloaded, False otherwise
    if record["Role"] == "H":
        location = "HouseReps"
        filetype = "pdf"
        pathstring = f'./{location}/{record["Name"]}/TO-PARSE/{record["Document"]}-{record["FilingDate"]}.{filetype}'  # noqa: E501
        filestored = os.path.exists(pathstring)
    elif record["Role"] == "S":
        location = "SenateReps"
        filetype = "html"
        pathstring = f'./{location}/{record["Name"]}/TO-PARSE/{record["Document"]}-{record["FilingDate"]}.{filetype}'  # noqa: E501
        filestored = os.path.exists(pathstring)
    if filestored:
        return True
    else:
        return False
