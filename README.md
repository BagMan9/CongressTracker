Downloads and automatically parses as much of the Periodic Transaction Reports as we can. Dumps to SQL database and JSON file.

Primary Limitations:
  - If submissions are made on paper, we cannot parse them. Records detected as such are recorded
  - Cannot "automatically" download files older than about ~one year or so, depending on the amount of records being parsed. By fiddling with the exact request arguments (SenatePreD.py) you can assemble the full transaction history.
  - To run, you must have poetry and python 3.11 or greater installed:

```bash
poetry install
poetry env activate

python app.py
```
