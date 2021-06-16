from flask import Flask, render_template
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
<<<<<<< HEAD
import math
=======
>>>>>>> e4b690b (unified data, made coin class.)
from coin import Coin

app = Flask(__name__)

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
apiCoins = []
<<<<<<< HEAD

response = session.get(url, params=parameters)
apiData = json.loads(response.text)
coinHeader =  Coin("Coin", "Name","Price", "Market Cap")
for c in apiData['data']:
  coinData = Coin(
    c['name'],
    c['symbol'],
    math.floor(c['quote']['CAD']['price']*100)/100,
    math.floor( (c['quote']['CAD']['market_cap']) *100)/100)
  apiCoins.append(coinData)
=======
>>>>>>> e4b690b (unified data, made coin class.)

@app.route('/')
@app.route('/coins')
def coinsHome():
    try:
<<<<<<< HEAD
=======
        response = session.get(url, params=parameters)
        apiData = json.loads(response.text)
        coinHeader =  Coin("Coin", "Name","Price", "Market Cap")
        for c in apiData['data']:
          coinData = Coin(c['name'],
          c['symbol'],
          c['quote']['CAD']['price'],
          c['quote']['CAD']['market_cap'])
          apiCoins.append(coinData)
>>>>>>> e4b690b (unified data, made coin class.)
        return render_template('coin.html', data=apiCoins, header=coinHeader)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)