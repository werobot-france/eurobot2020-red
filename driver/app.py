import time
import sys
#import eel

'''
differents modes of operations:

- DEBUG (position watcher & end switch) & script launch
- MATCH (wait for light sensor)
'''

operationMode = 'DEBUG'


# time.sleep(1)

# print("Exit")

# print("ERR", file=sys.stderr)
from src.Robot import *
from sys import exit
from os import _exit
from math import pi
from adafruit_crickit import crickit
from src.InputManager import *
from src.PositionWatcher import PositionWatcher
from src.WebsocketManager import WebsocketManager


websocketManager = WebsocketManager()
websocketManager.start()

positionWatcher = PositionWatcher(websocketManager)
positionWatcher.start()

robot = Robot(positionWatcher)
websocketManager.setRobot(robot)

# inputManager = InputManager(robot)
# inputManager.start()

# @eel.expose
# def isReady():
#     print('Eel enabled!')
#     positionWatcher.enableEel()

def main():
    print('Initialization')
    while True:
        time.sleep(1)

try:
    main()
    
except KeyboardInterrupt:
    print('Interrupted')
    robot.stopMotors()
    try:
        exit(0)
    except SystemExit:
        _exit(0)
