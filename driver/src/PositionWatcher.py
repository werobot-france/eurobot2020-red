from gpiozero import DigitalInputDevice
from threading import Thread
from time import sleep
from math import *

class PositionWatcher:
    perimeter = 205
    axialDistance = 233.5
    initialTheta = pi/2
    theta = 0
    x = 0
    y = 0

    # left
    phaseA = DigitalInputDevice(15, True)
    phaseB = DigitalInputDevice(14, True)

    # right
    phaseC = DigitalInputDevice(17, True)
    phaseD = DigitalInputDevice(27, True)

    leftTicks = 0
    rightTicks = 0

    leftState = (0, 0)
    leftOldState = (0, 0)

    rightState = (0, 0)
    rightOldState = (0, 0)

    watchPositionThread = None
    watchTicksThread = None
    enabled = True

    oldTicks = (0, 0)

    onPositionChangedHandler = None
    
    websocketManager = None
    
    def __init__(self, websocketManager):
        self.websocketManager = websocketManager
        self.theta = self.initialTheta
           
    def watchTicks(self):
        while self.enabled:
            leftFetchedState = (self.phaseA.value, self.phaseB.value)
            rightFetchedState = (self.phaseC.value, self.phaseD.value)
            if leftFetchedState != self.leftState:
                self.leftState = leftFetchedState

                if self.leftState[0] == self.leftOldState[1]:
                    self.leftTicks -= 1
                else:
                    self.leftTicks += 1

                self.leftOldState = self.leftState

            if rightFetchedState != self.rightState:
                self.rightState = rightFetchedState

                if self.rightState[0] == self.rightOldState[1]:
                    self.rightTicks -= 1
                else:
                    self.rightTicks += 1

                self.rightOldState = self.rightState

    def watchPosition(self):
        while self.enabled:
            newTicks = (self.leftTicks, self.rightTicks)
            if (newTicks != self.oldTicks):
                deltaTicks = (newTicks[0] - self.oldTicks[0],
                              newTicks[1] - self.oldTicks[1])
                self.oldTicks = newTicks
                leftDistance = deltaTicks[0] / 2400 * self.perimeter
                rightDistance = deltaTicks[1] / 2400 * self.perimeter
                t1 = (leftDistance + rightDistance) / 2
                alpha = (rightDistance - leftDistance) / self.axialDistance
                self.theta = self.theta + alpha
                if self.theta > pi:
                    self.theta -= 2 * pi
                elif self.theta < -pi:
                    self.theta += 2 * pi
                self.x = self.x + t1 * cos(self.theta)
                self.y = self.y + t1 * sin(self.theta)
                
                if self.websocketManager != None and self.websocketManager.isOnline():
                    self.websocketManager.emit('updatePosition', [round(self.x, 2), round(self.y, 2), round(self.theta, 2)])
                # if self.eelOnline:
                #     self.eel.updatePosition(round(self.x, 2), round(self.y, 2), round(self.theta, 2))
                # if self.onPositionChangedHandler != None:
                #     self.onPositionChangedHandler(round(self.x, 2), round(self.y, 2), round(self.theta, 2))
            sleep(0.01)

    def start(self):
        self.enabled = True
        self.watchTicksThread = Thread(target=self.watchTicks)
        self.watchTicksThread.start()
        self.watchPositionThread = Thread(target=self.watchPosition)
        self.watchPositionThread.start()

    def stop(self):
        self.enabled = False

    def getPos(self):
        return (self.x, self.y)

    def getOrientation(self):
        return (self.theta)

    def getOrientationDeg(self):
        return (self.theta * 180/pi)

    def setOnPositionChangedHandler(self, handler):
        self.onPositionChangedHandler = handler

    def reset(self):
        self.x = self.y = self.leftTicks = self.rightTicks = 0
        self.theta = self.initialTheta
        self.leftState = self.leftOldState = self.rightState = self.rightOldState = self.oldTicks = (0, 0)