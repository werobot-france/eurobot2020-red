from adafruit_crickit import crickit
from math import *
from time import sleep
from gpiozero import DigitalInputDevice

class Robot:
    leftMotor, rightMotor = crickit.dc_motor_1, crickit.dc_motor_2
    positionWatcher = None
    xR = yR = orientation = erreurPre = differenceErreurs = 0
    sommeErreurs = 0
    leftEndSwitch = DigitalInputDevice(13, True)
    rightEndSwitch = DigitalInputDevice(21, True)
    running = False

    def __init__(self, positionWatcher):
        self.positionWatcher = positionWatcher

    def fetch(self):
        self.xR = self.positionWatcher.getPos()[0]
        self.yR = self.positionWatcher.getPos()[1]
        self.orientation = self.positionWatcher.getOrientation()

    def goToOrientation(self, targetTheta):
        seuilOrientation = pi/10
        self.running = True
        while self.running:
            self.fetch()
            deltaTheta = targetTheta - self.orientation
            if abs(deltaTheta) > pi:
                deltaTheta = (2*pi - abs(deltaTheta)) * (-deltaTheta / abs(deltaTheta))
            if abs(deltaTheta) > seuilOrientation:
                self.setBoth(0.8 * deltaTheta/abs(deltaTheta) + (0.2/pi/(deltaTheta)))
            else:
                self.running = False
                self.stopMotors()

    def goToPath(self, path, threehold):
        inc = 0
        for point in path:
            print("\n\n Goto: ", point)
            mustStop = len(path)==inc+1
            t = 30
            if mustStop: t = threehold
            self.goTo(point[0], point[1], t, mustStop)
            inc += 1
        print('ALL COMPLETED')
  
    def setLeft(self, pwm):
        self.leftMotor.throttle = pwm
          
    def setRight(self, pwm):
        self.rightMotor.throttle = pwm
          
    def setBoth(self, pwm):
        self.setLeft(-pwm)
        self.setRight(pwm)

    def goTo(self, targetX, targetY, threehold, mustStop= False, backward = False):
        self.fetch()
        a = 0
        p, i, d = 190, 4, 550
        #p, i, d = 190, 2, 400
        vitesseC, vitesseR = 0.7 , 0.4
        self.running = True
        self.sommeErreurs = 0
        distanceCibleI = sqrt((targetX-self.xR)*(targetX-self.xR)+(targetY-self.yR)*(targetY-self.yR))

        while self.running:
            self.fetch()
            distanceCible = sqrt((targetX-self.xR)*(targetX-self.xR)+(targetY-self.yR)*(targetY-self.yR))
            targetTheta = atan2((targetY - self.yR), (targetX - self.xR))
            if (not backward):
                erreurOrientation = (targetTheta - self.orientation)
            else:
                erreurOrientation = (targetTheta - (self.orientation-pi))

            if mustStop: cmdG = cmdD = distanceCible
            else: cmdG = cmdD = distanceCibleI

            if cmdD > 255: cmdG = cmdD = 255
            
            cmdD *= vitesseC
            cmdG *= vitesseC

            if a == 0: self.erreurPre = (targetTheta - self.orientation)

            while abs(erreurOrientation) > pi:
                erreurOrientation += (-2*pi) * (erreurOrientation/abs(erreurOrientation))
                
            cmd = (erreurOrientation*p) + (self.sommeErreurs*i) + (self.differenceErreurs*d)
            cmdD += cmd
            cmdG -= cmd
            
            if cmdD > 255: cmdD = 255
            if cmdG > 255: cmdG = 255
            if cmdD < -255: cmdD = -255
            if cmdG < -255: cmdG = -255
            if abs(cmdG)<vitesseR*255 and cmdG != 0:cmdG = 255*vitesseR * cmdG/abs(cmdG)
            if abs(cmdD)<vitesseR*255 and cmdD != 0:cmdD = 255*vitesseR * cmdD/abs(cmdD)
            cmdD /= 255
            cmdG /= 255

            if a == 0:
                a+=1
                print('position Cible: ', (targetX, targetY))
                print('position Robot: ', (self.xR, self.yR, self.orientation))
                print('targetTheta: ', targetTheta)
                print('erreur actuelle', erreurOrientation)
                print('erreur précédente',self.erreurPre)
                print('distance à la cible',distanceCible)
                print((('CMD', cmd), ('G', cmdG), ('D', cmdD)))
                print('Coeffs PID: ', (p, i, d))

            self.differenceErreurs = erreurOrientation - self.erreurPre
            self.sommeErreurs += erreurOrientation
            self.erreurPre = erreurOrientation
            
            try:
                if (not backward):
                    self.leftMotor.throttle = cmdG
                    self.rightMotor.throttle = cmdD
                else:
                    self.leftMotor.throttle = -cmdD
                    self.rightMotor.throttle = -cmdG
            except ValueError:
                print('_____________________ERREUR________________________')
                print(-cmdG, cmdD)
            if distanceCible < threehold:
                self.running = False

            print('arrivé !  position:', (self.xR, self.yR, degrees(self.orientation)))
            
        print('exit of the loop')
        if mustStop:
            self.stopMotors()
            self.goToOrientation(pi/2)

    def stopMotors(self):
        self.leftMotor.throttle = self.rightMotor.throttle = 0
        
    def cancelOperations(self):
        self.running = False

    def stopThreads(self):
        self.positionWatcher.stop()

    def logState(self):
        self.fetch()
        print(self.xR, self.yR, degrees(self.orientation))
            
    def logStateLoop(self):
        while True:
            self.fetch()
            print(self.xR, self.yR, degrees(self.orientation))
            sleep(0.1)

    def goUntilTouched(self):
        self.leftMotor.throttle = -0.5
        self.rightMotor.throttle = -0.5
        while not(self.leftEndSwitch.value and self.rightEndSwitch.value):
            sleep(0)
        self.stopMotors()

