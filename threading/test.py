import threading
from threading import Thread
import time

check = threading.Condition()

def func1():
    print ("funn1 started")
    check.acquire()
    check.wait()
    print ("got permission")
    print ("funn1 finished")


def func2():
    print ("func2 started")
    check.acquire()
    time.sleep(2)
    check.notify()
    check.release()
    time.sleep(2)
    print ("func2 finished")

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()