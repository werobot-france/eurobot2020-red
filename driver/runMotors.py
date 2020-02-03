import time
import sys
from sys import exit
from os import _exit
from adafruit_crickit import crickit

motor1, motor2 = crickit.dc_motor_1, crickit.dc_motor_2

def main():
    print("main")
    motor1.throttle = -1
    motor2.throttle = 1
    while True:
        time.sleep(1)

try:
    main()

except KeyboardInterrupt:
    print('Interrupted')
    motor1.throttle = 0
    motor2.throttle = 0

    try:
        exit(0)
    except SystemExit:
        _exit(0)

