import threading
import time


class OrderMaker(threading.Thread):
    active_threads = 0
    def __init__(self, name):
        super(OrderMaker, self).__init__()
        self.name = name

    def run(self):
        OrderMaker.active_threads +=1
        print "Starting thread: " + self.name
        time.sleep(2)
        print "Making orders"
        time.sleep(4)
        print "successfully placed order"
        OrderMaker.active_threads -= 1


class Order:
    pass