# Crypto Tracker

#### This is script to help automoate the tracking of my cryptocurrency cost basis by fetching my trade data from Gemini and writing to a personal google sheet.

`main.py` - entrypoint of script, executed with `python main.py`

`trades.py` - fetches and returns trade data from gemini

`sheets.py` - wraps logic used for reading/writing to google sheet

`last-indices.json` - includes the last row that was written to on the previous run. This is used because the google sheets api doesn't include (to my knowledge) a great way of getting the last row with data without loading the whole sheet into memory. So I opted to used a separate file to store the last indices of each sheet. This file will be updated on each successful run.

### Not Included

`secrets.py` - where I stored gemini api keys and google spreadsheet ID's/sheet names

`sheets-keys.json` - contains api key data for accessing google sheets api. Was generated using Google Cloud Platform

### References
[Gemini API](https://docs.gemini.com/rest-api/)

[Sheets API](https://developers.google.com/sheets/api)
