from __future__ import print_function
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from secrets import SPREADSHEET_ID

'''
handles authentication and returns sheet object from which we can read and write
'''
def get_sheet():
  # generate credentials to access spreadsheet
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
  SERVICE_ACCOUNT_FILE = 'sheets-keys.json' #contains private key data, generated in Google Cloud Platform
  creds = None
  creds = service_account.Credentials.from_service_account_file(
          SERVICE_ACCOUNT_FILE, scopes=SCOPES)

  service = build('sheets', 'v4', credentials=creds)


  # Call the Sheets API and return sheet object
  sheet = service.spreadsheets()
  return sheet

'''
gets the last-entered timestamp in the spreadsheet. This timestamp is used 
in the Gemini api call to serve as a starting point for querying trades
'''
def get_last_timestamp(sheet, sheet_name, last_index):
  range_query = "{}!A{}".format(sheet_name, last_index)
  result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_query).execute()
  values = result.get("values", [])
  if len(values) and len(values[0]) == 1:
    return values[0][0]
  else:
    return 0

'''
writes newly fetched trade data to sheet
'''
def write_to_sheet(sheet, sheet_name, last_index, trades):
  trade_count = len(trades)
  range_row_start = last_index + 1
  range_row_end = last_index + trade_count

  range_query = "{}!A{}:E{}".format(sheet_name, range_row_start, range_row_end)

  values = []
  for trade in trades:
    d = datetime.fromtimestamp(trade["timestampms"] / 1000)
    timestamp = trade["timestampms"]
    date_string = d.strftime("%m/%d/%Y")
    cost = float(trade["price"]) * float(trade["amount"]) + float(trade["fee_amount"])
    amount = float(trade["amount"])
    cost_per_coin = cost / amount

    row = [timestamp, date_string, cost, amount, cost_per_coin]
    values.append(row)

  body = {
    "values": values
  }

  result = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID, range=range_query,
    valueInputOption="USER_ENTERED", body=body).execute()
  print('{0} cells updated.'.format(result.get('updatedCells')))


