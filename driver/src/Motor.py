from adafruit_crickit import crickit

class Motor:
    leftMotor, rightMotor = crickit.dc_motor_1, crickit.dc_motor_2

    def stopAll(self):
        self.leftMotor.throttle = self.rightMotor.throttle = 0
        
    def setBoth(self, left, right):
        self.leftMotor.throttle = left
        self.rightMotor.throttle = right
        
    def setLeft(self, value):
        self.leftMotor.throttle = value
        
    def setRight(self, value):
        self.leftMotor.throttle = value