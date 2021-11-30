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
  f = open("last-indices.json")
  last_indices = json.load(f)
  last_index = last_indices[config["index_key"]]
  last_timestamp = sheets.get_last_timestamp(sheet, config["sheet_name"], last_index)
  print(last_timestamp)

# f = open("last-indices.json")
# last_indices = json.load(f)
# f.close()


# f = open("last-indices.json", "w")
# json.dump(last_indices, f)


my_trades = get_trades("btcusd")
print(my_trades[0])
