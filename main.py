from trades import get_trades
from secrets import BTC_SHEET_NAME, ETH_SHEET_NAME
import sheets

import json

configs = [
  {
    "sheet_name": BTC_SHEET_NAME,
    "symbol": "btcusd",
    "index_key": "btc"
  },
  {
    "sheet_name": ETH_SHEET_NAME,
    "symbol": "ethusd",
    "index_key": "eth"
  }
]

sheet = sheets.get_sheet()

for config in configs:
  #get last indices data from local json file
  f = open("last-indices.json")
  last_indices = json.load(f)
  f.close()

  #get last timestamp to use as starting point in gemini api call
  last_index = last_indices[config["index_key"]]
  last_timestamp = sheets.get_last_timestamp(sheet, config["sheet_name"], last_index)

  my_trades = get_trades(config["symbol"], last_timestamp)
  if len(my_trades) <= 1:
    print("No {} transactions have occurred since the provided timestamp {}".format(config["symbol"], last_timestamp))
    continue
  #trades come back from newest to oldest. we want the opposite.
  my_trades.reverse()
  #since gemini api returns all transaction on or after provided timestamp, we remove the first so we only have transactions that occurred after the provided timestamp
  my_trades = my_trades[1:]

  #write data to spreadsheet
  sheets.write_to_sheet(sheet, config["sheet_name"], last_index, my_trades)

  #update last-indices.json with new values for the last indices
  last_indices[config["index_key"]] = last_index + len(my_trades)
  f = open("last-indices.json", "w")
  json.dump(last_indices, f)




