import json
from urllib2 import Request, urlopen, URLError

def btcTurk():
    request = Request('https://www.btcturk.com/api/ticker')

    try:
        response = urlopen(request)
        data = json.loads(response.read())
        return data['last']
    except URLError, e:
        print 'No price. Got an error code:', e

def polo():
    request = Request('https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_BTC&depth=5')

    try:
        response = urlopen(request)
        data = json.loads(response.read())
        total =0
        for value in data['asks']:
            total = total + float(value[0])
        return total/5
    except URLError, e:
        print 'No price. Got an error code:', e

def USDrate():
    request = Request('http://api.fixer.io/latest?base=USD')

    try:
        response = urlopen(request)
        data = json.loads(response.read())
        return data['rates']['TRY']
    except URLError, e:
        print 'No price. Got an error code:', e

turkPrice = btcTurk()
print 'BTCTurk fiyat: ' , turkPrice
poloPriceUSD = polo()
print 'Poloniex fiyat: ' , poloPriceUSD
UsdTryRate = USDrate()
print 'Dolar kuru: ' , UsdTryRate
poloPriceTRY = poloPriceUSD *UsdTryRate
print 'Polo TRY fiyat: ' , poloPriceTRY
fark = poloPriceTRY - turkPrice
print 'FARK: ' , fark
print 'REEL FARK: ' , fark -(turkPrice*0.005 +poloPriceTRY*0.0025)

#naber