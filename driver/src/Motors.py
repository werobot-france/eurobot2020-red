from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice

class Motors:
    
    def __init__(self):
        #///////////////// Define Motor Driver GPIO Pins /////////////////
        # Motor A, Left Side GPIO CONSTANTS
        PWM_DRIVE_LEFT = 12     # ENA - H-Bridge enable pin
        FORWARD_LEFT_PIN = 8   # INA1 - Forward Drive
        REVERSE_LEFT_PIN = 7   # INA2 - Reverse Drive
        # Motor B, Right Side GPIO CONSTANTS
        PWM_DRIVE_RIGHT = 18    # ENB - H-Bridge enable pin
        FORWARD_RIGHT_PIN = 24  # INB1 - Forward Drive
        REVERSE_RIGHT_PIN = 23   # INB2 - Reverse Drive
        
        STANDBY_PIN = 25
        
        self.driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)
        self.driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 1000)

        self.forwardLeft = DigitalOutputDevice(FORWARD_LEFT_PIN)
        self.reverseLeft = DigitalOutputDevice(REVERSE_LEFT_PIN)

        self.forwardRight = DigitalOutputDevice(REVERSE_RIGHT_PIN)
        self.reverseRight = DigitalOutputDevice(FORWARD_RIGHT_PIN)

        # self.driveLeft = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 1000)
        # self.driveRight = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)

        # self.forwardLeft = DigitalOutputDevice(FORWARD_RIGHT_PIN)
        # self.reverseLeft = DigitalOutputDevice(REVERSE_RIGHT_PIN)

        # self.forwardRight = DigitalOutputDevice(FORWARD_LEFT_PIN)
        # self.reverseRight = DigitalOutputDevice(REVERSE_LEFT_PIN)
        
        self.standBy = DigitalOutputDevice(STANDBY_PIN) 
        self.standBy.value = True

    
    def setLeft(self, value):
        if value < 0:
            value = -value
            self.reverseLeft.value = True
            self.forwardLeft.value = False
        else:
            self.reverseLeft.value = False
            self.forwardLeft.value = True
        print('Left', value)
        self.driveLeft.value = value
    
    def setRight(self, value):
        if value < 0:
            value = -value
            self.reverseRight.value = True
            self.forwardRight.value = False
        else:
            self.reverseRight.value = False
            self.forwardRight.value = True
        print('Right', value)
        self.driveRight.value = value
        
    def setBoth(self, value):
        self.setLeft(value)
        self.setRight(value)

    def stop(self):
        print('MOTORS: Stop Called')
        self.reverseLeft.value = False
        self.forwardLeft.value = False
        self.forwardRight.value = False
        self.reverseRight.value = False
        self.driveRight.value = 0
        self.driveLeft.value = 0
        