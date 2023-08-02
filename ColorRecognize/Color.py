import sensor, image, time
from pyb import UART, LED
import json, math


def sensorSet():
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QQVGA)
    sensor.skip_frames(time = 200)
    sensor.set_contrast(1)
    sensor.set_auto_gain(False)
    sensor.set_auto_whitebal(False)
    #垂直翻转
    #sensor.set_vflip(True)
    #水平镜像
    #sensor.set_hmirror(True)


#[]
redThresholds = [(96, 100, -128, 127, -128, 127), (42, 100, 6, 127, -128, 127)]
greenThresholds = [(98, 100, -8, 127, -2, 127)]
QQVGAscreenROI = [30, 10, 100, 100]
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

sensorSet()

while(True):
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)

    redBlobs = img.find_blobs(redThresholds, roi = QQVGAscreenROI, x_stride = 2, y_stride = 2\
        ,  area_threshold=9, merge=False, merge=False)
    greenBlobs = img.find_blobs(greenThresholds, roi = QQVGAscreenROI, x_stride = 2, y_stride = 2\
        ,  area_threshold=9, merge=False, merge=False)

    if redBlobs == None:
        print(0)
    for rb in redBlobs:
        img.draw_rectangle(rb.rect(), color = green)
        print(rb.rect())
        pass

    for gb in greenBlobs:
        img.draw_rectangle(gb.rect(), color = green)
        pass
