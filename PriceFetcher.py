import json
from urllib2 import Request, urlopen, URLError
from threading import Timer
import DataHandler

from time import sleep
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
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

def Report():
    #threading._Timer(5.0,Report).start()
    datas =[]
    turkPrice = btcTurk()
    datas.append(turkPrice)
    print 'BTCTurk fiyat: ' , turkPrice
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
    print datas
    DataHandler.appendData(datas)



#Execute the above function every 5 seconds from another thread
DataHandler.initialize()
rt= RepeatedTimer(5, Report)
sleep(17)

print 'multithreading'
#Stop the other thread
rt.stop()
DataHandler.savedata()