from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from secrets import SPREADSHEET_ID, BTC_SHEET_NAME, ETH_SHEET_NAME

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

  range_test = "{}!A1:E1".format(BTC_SHEET_NAME)

  # Call the Sheets API and return sheet object
  sheet = service.spreadsheets()
  return sheet

def get_last_timestamp(sheet, sheet_name, last_index):
  range_query = "{}!A{}".format(sheet_name, last_index)
  result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_query).execute()
  values = result.get("values", [])
  if len(values) and len(values[0]) == 1:
    return values[0][0]
  else:
    return 0

# result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                             range=range_test).execute()
# values = result.get('values', [])

# print(result)

