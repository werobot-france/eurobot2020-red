
from threading import Thread
from time import sleep

class InputManager(Thread):
    def __init__(self):
        Thread.__init__(self)
 
 
    def run(self):
        while True:
            print(input())
        
inputManager = InputManager()
inputManager.start()

print('main...')

i= 0
while True:
    i += 1
    print(i)
    sleep(0.5)
    