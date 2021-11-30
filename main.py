import secrets #separate file to store api key and secret
import requests
import json
import base64
import hmac
import hashlib
import datetime, time

'''
Make request to gemini to get trades. Ref: https://docs.gemini.com/rest-api/#private-api-invocation 
'''
def get_trades(symbol):
  #import and assign api key and secret here
  api_key = secrets.API_KEY
  api_secret = secrets.API_SECRET

  url = "https://api.gemini.com/v1/mytrades"
  gemini_api_key = api_key
  gemini_api_secret = api_secret.encode()

  t = datetime.datetime.now()
  payload_nonce =  str(int(time.mktime(t.timetuple())*1000))
  payload =  {
    "request": "/v1/mytrades",
    "nonce": payload_nonce,
    "symbol": symbol
  }
  encoded_payload = json.dumps(payload).encode()
  b64 = base64.b64encode(encoded_payload)
  signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

  request_headers = {
    'Content-Type': "text/plain",
    'Content-Length': "0",
    'X-GEMINI-APIKEY': gemini_api_key,
    'X-GEMINI-PAYLOAD': b64,
    'X-GEMINI-SIGNATURE': signature,
    'Cache-Control': "no-cache"
  }

  response = requests.post(url, headers=request_headers)
  return response.json()


my_trades = get_trades("btcusd")
print(my_trades[0])
