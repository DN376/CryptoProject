import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5',
  'convert':'CAD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '57b0aad8-c20d-4c66-84f6-29a84f550a17',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)