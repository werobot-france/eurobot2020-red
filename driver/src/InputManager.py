from threading import Thread
from time import sleep
import json
from src.Motor import Motor
from adafruit_crickit import crickit

class InputExecutor(Thread):
    def __init__(self, robot, params):
        print('hey1')
        self.robot = robot
        self.params = params
        Thread.__init__(self)

    def run(self):
        print('hey')
        self.robot.goTo(*self.params)

class InputManager(Thread):
    
    leftMotor, rightMotor = crickit.dc_motor_1, crickit.dc_motor_2
    
    def __init__(self, robot):
        self.robot = robot
        self.motors = Motor()
        Thread.__init__(self)

    def run(self):
        while True:
            got = input()
            data = json.loads(got)
            cmd = data["cmd"]
            args = data["args"]
            if cmd == 'goto':
                print('I will goto', data["args"]["x"], data["args"]["y"])
                executor = InputExecutor(self.robot, [data["args"]["x"], data["args"]["y"], 10, True])
                executor.start()
            elif cmd == 'motors':
                print('motors', args)
                self.leftMotor.throttle = args[0]
                self.rightMotor.throttle = args[1]
            elif cmd == 'stop':
                print('Stop command received')
                self.robot.cancelOperations()
                self.motors.stopAll()
            elif cmd == 'start_position_trace':
                print('LOG# > Enabled position trace')
            elif cmd == 'stop_position_trace':
                print('LOG# > Disabled position trace')
            else:
                print("Command not recognized")