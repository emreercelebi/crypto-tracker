import requests
import json
import base64
import hmac
import hashlib
import time

#import gemini api key and secret
from secrets import API_KEY, API_SECRET

'''
Make request to gemini to get trades. Ref: https://docs.gemini.com/rest-api/#private-api-invocation 
'''
def get_trades(symbol, timestamp):
  url = "https://api.gemini.com/v1/mytrades"
  gemini_api_key = API_KEY
  gemini_api_secret = API_SECRET.encode()

  payload_nonce =  str(round(time.time() * 1000))
  payload =  {
    "request": "/v1/mytrades",
    "nonce": payload_nonce,
    "timestamp": timestamp,
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