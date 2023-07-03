import json
import sqlite3


def addToDB(filePath):
    conn = sqlite3.connect("./DataWork/transactions.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        Name TEXT,
        FilingDate TEXT,
        ID TEXT UNIQUE,
        Date TEXT,
        Owner TEXT,
        Ticker TEXT,
        Asset TEXT,
        SecurityType TEXT,
        SaleType TEXT,
        Amount TEXT
    )
    """)

    with open(filePath, "r") as input:
        transactions = json.load(input)

    for item in transactions:
        c.execute(
            """
    INSERT OR IGNORE INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                item["Name"],
                item["Filing Date"],
                item["ID"],
                item["Date"],
                item["Owner"],
                item["Ticker"],
                item["Asset"],
                item["Security Type"],
                item["Sale Type"],
                item["Amount"],
            ),
        )

    conn.commit()
    conn.close()
