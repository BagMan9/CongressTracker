from validation import updateMerge


def newTransaction():
    manual_data = {}
    manual_data["Name"] = input("Name: ")
    manual_data["Filing Date"] = input("Filing Date: ")
    manual_data["ID"] = input("ID: ")
    manual_data["Date"] = input("Date: ")
    manual_data["Owner"] = input("Owner: ")
    manual_data["Ticker"] = input("Ticker: ")
    manual_data["Asset"] = input("Asset: ")
    manual_data["Security Type"] = input("Security Type: ")
    manual_data["Sale Type"] = input("Sale Type: ")
    manual_data["Amount"] = input("Amount: ")
    return manual_data


if __name__ == "__main__":
    new = newTransaction()
    updateMerge("./DataWork/Transactions.json", [new], "Date")
