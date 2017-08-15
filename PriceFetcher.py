import json
from urllib2 import Request, urlopen, URLError
from threading import Timer
import datetime
from socket import timeout
from OrderMaker import OrderMaker
from multiprocessing.pool import ThreadPool

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

# MultiThreaded version of the Report function
def ReportMulti():

    pool = ThreadPool(processes=3)

    btcturk_result = pool.apply_async(btcTurk,)
    usd_try_result = pool.apply_async(USDrate, )
    poloniex_result = pool.apply_async(polo, )


    p = PriceTick()
    p.btcturk_price = btcturk_result.get()
    p.polo_usd = poloniex_result.get()
    p.usd_try_rate = usd_try_result.get()
    p.polo_try = p.polo_usd * p.usd_try_rate
    p.chooseAction()
    print p.toList()
    return p.toList()


