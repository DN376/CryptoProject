from flask import Flask, render_template
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import math
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from coin import Coin
from coin_database import Base, Coins
from sqlalchemy import exists

app = Flask(__name__)
engine = create_engine('sqlite:///coins_db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'10',
  'convert':'CAD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '57b0aad8-c20d-4c66-84f6-29a84f550a17',
}

apiSession = Session()
apiSession.headers.update(headers)


response = apiSession.get(url, params=parameters)
apiData = json.loads(response.text)
coinHeader =  Coin("Coin", "Name","Price", "Market Cap")

for c in apiData['data']:
  newItem = Coins(
    name=c['name'],
    symbol=c['symbol'],
    price=math.floor(c['quote']['CAD']['price']*100)/100,
    marketCap=math.floor( (c['quote']['CAD']['market_cap']) *100)/100,
    id=c['id']
  )
  exists = session.query(Coins).filter_by(id = c['id']).one()
  if exists is not None:
    coin = session.query(Coins).filter_by(id = c['id']).one()
    coin.price = newItem.price
    coin.marketCap = newItem.marketCap
  else:
    session.add(newItem)
session.commit()

@app.route('/')
@app.route('/coins')
def coinsHome(): 
    try:
      apiCoins = []
      cEngine = create_engine('sqlite:///coins_db.db')
      Base.metadata.bind = cEngine
      cDBSession = sessionmaker(bind=cEngine)
      cSession = cDBSession()
      coinQueries = cSession.query(Coins).all()
      for c in coinQueries:
        coinData = Coin(
          c.name,
          c.price,
          math.floor(c.price*100)/100,
          math.floor( (c.marketCap)*100)/100
        )
        apiCoins.append(coinData)
      return render_template('coin.html', data=apiCoins, header=coinHeader)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)

