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
import threading

app = Flask(__name__)
def createSession():
  engine = create_engine('sqlite:///coins_db.db')
  Base.metadata.bind = engine

  DBSession = sessionmaker(bind=engine)
  return DBSession()

def init():
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
  numTimesUpdated = 0
  def update(index):
    updateTimer = threading.Timer(60.0, update, [index+1])
    updateTimer.start()
    print (index)
    if index >= 5:
      print("cancelled thread")
      updateTimer.cancel()
    
    print("\nupdated",flush=True)

    response = apiSession.get(url, params=parameters)
    apiData = json.loads(response.text)
    session = createSession()

    for c in apiData['data']:
      newItem = Coins(
        name=c['name'],
        symbol=c['symbol'],
        price=math.floor(c['quote']['CAD']['price']*100)/100,
        marketCap=math.floor((c['quote']['CAD']['market_cap']) *100)/100,
        id=c['id']
      )
      exists = session.query(Coins).filter_by(id = c['id']).first()
      if exists is not None:
        coin = session.query(Coins).filter_by(id = c['id']).one()
        print("updated " + coin.name + " from " + str(coin.price) + " to " + str(newItem.price))
        coin.price = newItem.price
        coin.marketCap = newItem.marketCap
      else:
        session.add(newItem)
        print("created" + coin.name + "at")
    session.commit()
  update(numTimesUpdated)

init()

@app.template_filter()
def currencyFormat(value):
    v = float(value)
    return "${:,.2f} CAD".format(value)

@app.template_filter()
def marketCapFormat(value):
    v = float(value)
    lenVal = len("{:,.0f}".format(value))
    if lenVal >= 15: #trillions
      return "${:,.2f}T CAD".format(value/100_000_000_000)
    if lenVal > 9: #billions
      return "${:,.2f}B CAD".format(value/100_000_000)
    if lenVal > 6: #millions
      return "${:,.2f}M CAD".format(value/100_000)
    if lenVal > 3: #thousands
      val = math.floor(v/100)*100 
      return "${:,.2f}K CAD".format(value/100)
    return "{:,.2f}".format(value)
app.add_template_filter(currencyFormat)
app.add_template_filter(marketCapFormat)
@app.route('/')
@app.route('/coins')
def coinsHome(): 
    try:
      apiCoins = []
      cSession = createSession()
      coinQueries = cSession.query(Coins).all()
      coinHeader =  Coin("Coin", "Name","Price", "Market Cap")
      for c in coinQueries:
        coinData = Coin(
          c.name,
          c.symbol,
          math.floor(c.price*100)/100,
          math.floor((c.marketCap)*100)/100
        )
        apiCoins.append(coinData)
      return render_template('coin.html', data=apiCoins, header=coinHeader)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)

