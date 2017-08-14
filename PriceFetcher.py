import json
from urllib2 import Request, urlopen, URLError
from threading import Timer
from threading import Thread
import datetime
from socket import timeout
from OrderMaker import OrderMaker

class PriceTick:
    def __init__(self ):
        self.timestamp = None
        self.btcturk_price = None
        self.polo_usd = None
        self.usd_try_rate = None
        self.polo_try = None
        self.difference = None
        self.diff_real = None
        self.decision = None

    def __str__(self):
        return "Reel Fark: " + self.diff_real + " TRY"

    def toList(self):
        datas = []
        datas.append(self.btcturk_price)
        datas.append(self.polo_usd)
        datas.append(self.usd_try_rate)
        datas.append(self.polo_try)
        datas.append(self.difference)
        datas.append(self.diff_real)
        datas.append(self.decision)
        datas.append(datetime.datetime.now().strftime('%m-%d-%Y-%H:%M:%S'))
        return datas

    def chooseAction(self):
        if self.polo_try > self.btcturk_price:
            self.difference = self.polo_try - self.btcturk_price
            self.decision = "Buy from BtcTurk"


        elif self.polo_try < self.btcturk_price:
            self.decision = "Buy from Poloniex"
            self.difference = self.btcturk_price - self.polo_try
        else:
            self.difference = None
            self.diff_real = None
            self.decision = None
            return

        self.diff_real = self.difference - (self.btcturk_price * 0.005 + self.polo_try * 0.0025)
        if self.diff_real < 30:
            self.decision = "No Action"
        else:
            OrderMaker(name=self.decision).start()
            OrderMaker(name=self.decision + ": sell from opposite website ").start()


def btcTurk():
    request = Request('https://www.btcturk.com/api/ticker')

    try:
        response = urlopen(request, timeout=2)
        data = json.loads(response.read())
        return data['last']
    except URLError as e:
        return ("UrlError in btcTurk")
    except timeout as e:
        return ("TimeOut in btcTurk")

def polo():
    request = Request('https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_BTC&depth=5')

    try:
        response = urlopen(request, timeout=2)
        data = json.loads(response.read())
        total =0
        for value in data['asks']:
            total = total + float(value[0])
        return total/5
    except URLError as e:
        return ("UrlError in Poloniex")
    except timeout as e:
        return ("TimeOut in Poloniex")


def USDrate():
    request = Request('http://api.fixer.io/latest?base=USD')

    try:
        response = urlopen(request, timeout=2)
        data = json.loads(response.read())
        return data['rates']['TRY']
    except URLError as e:
        return ("UrlError in Parity")
    except timeout as e:
        return ("TimeOut in Parity")

def Report():
    p = PriceTick()
    p.btcturk_price = btcTurk()
    p.polo_usd = polo()
    p.usd_try_rate = USDrate()
    p.polo_try = p.polo_usd * p.usd_try_rate
    p.chooseAction()
    print p.toList()
    return p.toList()

def Report2():
    datas =[]
    turkPrice = btcTurk()
    datas.append(turkPrice)
    print 'BtcTurk fiyat: ' , turkPrice
    poloPriceUSD = polo()
    datas.append(poloPriceUSD)
    print 'Poloniex fiyat: ' , poloPriceUSD
    UsdTryRate = USDrate()
    datas.append(USDrate())
    print 'Dolar kuru: ' , UsdTryRate
    poloPriceTRY = poloPriceUSD *UsdTryRate
    datas.append(poloPriceTRY)
    print 'Polo TRY fiyat: ' , poloPriceTRY
    fark = poloPriceTRY - turkPrice
    choice=0
    if fark < 0:
        fark = fark * -1
        choice =1
        print 'POLONIEXTEN ALMAK MANTIKLI'
    else:
        choice =2
        print 'BTCTURKTEN ALMAK MANTIKLI'
    print 'FARK: ' , fark
    datas.append(fark)
    reelfark = fark -(turkPrice*0.005 +poloPriceTRY*0.0025)
    datas.append(reelfark)
    print 'REEL FARK: ' , reelfark
    if reelfark < 0:
        datas.append('No Action')
    else:
        if choice == 1:
            datas.append('Poloniex Buy')
        else:
            datas.append('BtcTurk Buy')

    datas.append(datetime.datetime.now().strftime('%m-%d-%Y-%H:%M:%S'))
    print datas
    return datas