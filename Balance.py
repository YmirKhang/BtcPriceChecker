from threading import Thread
import time
import Queue

class Balance:

    def __init__(self):
        pass



def f1(arg):
    time.sleep(2)
    return arg + ' f1'


def f2(arg):
    time.sleep(5)
    return arg + ' f2'


def f3(arg):
    return arg + ' f3'


from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=3)

async_result = pool.apply_async(f1, ('ilk',))
async_result2 = pool.apply_async(f2, ('ilk',))
async_result3 = pool.apply_async(f3, ('ilk',))

print async_result.get(), async_result2.get() , async_result3.get()

