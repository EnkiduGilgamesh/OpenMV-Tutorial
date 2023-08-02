import time
from pyb import Servo

pan_servo=Servo(1)
tilt_servo=Servo(2)

pan_servo.calibration(500,2500,500)
tilt_servo.calibration(500,2500,500)
angle = 15;

while(True):
    time.sleep_ms(100)
    pan_servo.angle(angle)
    tilt_servo.angle(angle)
    angle += 15
