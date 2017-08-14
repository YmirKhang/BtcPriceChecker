import time
import PriceFetcher

import DataHandler
import threading
from OrderMaker import OrderMaker

class Runner:
    #mode as in backtest, realtime trading etc.
    def __init__(self, mode, ):
        self.workbook = DataHandler.initialize()
        self.worksheet = DataHandler.initializeWS(self.workbook)
        self.tick_count = 0
        self.gave_order = False

    def tick(self):
        self.tick_count+=1
        try:
            tickdata=PriceFetcher.Report()
            DataHandler.appendData(tickdata, self.worksheet)
        except Exception as e:
            self.stop(exception=e)


    def start(self,  sleep=5, duration=25):

        start = time.time()
        last_tick = start - sleep
        while (time.time() - start < duration ):
            delta = time.time() - last_tick
            if (delta < sleep):
                # sleep for the remaining seconds

                if OrderMaker.active_threads > 0:
                    print "Order in progress, stopping the main loop. Order Count: ", OrderMaker.active_threads
                    time.sleep(10)

                time.sleep(sleep-delta)
                self.tick() # calls Bot's update functions

            last_tick = time.time()
        self.stop(None)


    def stop(self, exception):
        DataHandler.savedata(self.workbook)

r = Runner(mode="test")
r.start()