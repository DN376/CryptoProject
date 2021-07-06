@app.template_filter()
def currencyFormat(value):
    v = float(value)
    return "${:,.2f} CAD".format(value)

@app.template_filter()
def marketCapFormat(value):
    v = float(value)
    lenVal = len("{:,.0f}".format(value))
    if lenVal > 12: #trillions
      return "${:,.2f}T CAD".format(value/100_000_000_000)
    if lenVal > 9: #billions
      return "${:,.2f}B CAD".format(value/100_000_000)
    if lenVal > 6: #millions
      return "${:,.2f}M CAD".format(value/100_000)
    if lenVal > 3: #thousands
      val = math.floor(v/100)*100 
      return "${:,.2f}K CAD".format(value/100)
    return "{:,.2f}".format(value)


    # <td>{{coin.price | currencyFormat }}</td>
    # <td>{{coin.marketCap | marketCapFormat }}</td>