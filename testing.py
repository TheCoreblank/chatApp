from threading import *
import time

def TestThreadOne():
    while True:
        print("Hello")
        time.sleep(1)

def TestThreadTwo():
    while True:
        input("> ")

Thread(target=TestThreadOne, args=()).start()
Thread(target=TestThreadTwo, args=()).start()

