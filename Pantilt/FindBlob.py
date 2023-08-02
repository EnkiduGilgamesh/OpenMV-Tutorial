import sensor, image, time

from pid import PID
from pyb import Servo

pan_servo=Servo(1)
tilt_servo=Servo(2)

pan_servo.calibration(500,2500,500)
tilt_servo.calibration(500,2500,500)

red_threshold  = (13, 49, 18, 61, 6, 47)
green_threshold = (98, 100, -8, 127, -2, 127)

#pan_pid = PID(p=0.07, i=0, imax=90) #脱机运行或者禁用图像传输，使用这个PID
#tilt_pid = PID(p=0.05, i=0, imax=90) #脱机运行或者禁用图像传输，使用这个PID
pan_pid = PID(p=0.1, i=0, imax=90)#在线调试使用这个PID
tilt_pid = PID(p=0.1, i=0, imax=90)#在线调试使用这个PID

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.

def find_min(blobs):
    min_size=9999
    for blob in blobs:
        if blob[2]*blob[3] < min_size:
            min_blob=blob
            min_size = blob[2]*blob[3]
    return min_blob


while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    blobs = img.find_blobs([green_threshold])
    if blobs:
        min_blob = find_min(blobs)
        pan_error = min_blob.cx()-img.width()/2
        tilt_error = min_blob.cy()-img.height()/2

        print("pan_error: ", pan_error)

        img.draw_rectangle(min_blob.rect()) # rect
        img.draw_cross(min_blob.cx(), min_blob.cy()) # cx, cy

        pan_output=pan_pid.get_pid(pan_error,1)/2
        tilt_output=tilt_pid.get_pid(tilt_error,1)
        print("pan_output",pan_output)
        pan_servo.angle(pan_servo.angle()+pan_output)
        tilt_servo.angle(tilt_servo.angle()-tilt_output)
