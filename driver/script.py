
from threading import Thread
from time import sleep

class Something:
    def __init__(self):
        #dqdsqds
        self.x = 1
        
    def lel(self):
        print('lel')

class InputManager(Thread):
    def __init__(self, x, y):
        Thread.__init__(self)

    def run(self):
        while True:
            print(input())
        
inputManager = InputManager(Something(), 4)
inputManager.start()

print('main...')

i= 0
while True:
    i += 1
    print(i)
    sleep(0.5)
    