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


def cmpPtX(pt1, pt2):
    return pt1[0] < pt2[0]


def cmpPtY(pt1, pt2):
    return pt1[1] < pt2[1]


def sortPtsX(pts, cmp):
    for i in range(1, len(pts)):
        key = pts[i]

        j = i-1
        while j >=0 and cmp(key, pts[j]):
            pts[j+1] = pts[j]
            j -= 1
        pts[j+1] = key


def sortPtsCCW(pts, sort1, cmp1):
    sort1(pts, cmp1)

    # left group
    if cmpPtY(pts[0], pts[1]):
        key = pts[0]
        pts[0] = pts[1]
        pts[1] = key

    # right group
    if not cmpPtY(pts[2], pts[3]):
        key = pts[2]
        pts[2] = pts[3]
        pts[3] = key


lineThreshold = [(0, 27, -128, 127, -128, 127)]
blackThreshold = [(0, 27, -128, 127, -128, 127)]
QVGAscreenROI = [60, 20, 200, 200]                  # 320*240, roi = 200*200
QQVGAscreenROI = [30, 10, 100, 100]                 # 160*120, roi = 100*100
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
LM = 40

sensorSet()

while(True):
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)

    #line_segments = img.find_line_segments(QVGAscreenROI, merge_distance = 10, max_theta_difference=30)

    rects = img.find_rects(QQVGAscreenROI, threshold = 5000)

    print("%d"%(len(rects)))

    if len(rects) == 1:
        corners = list(rects[0].corners())
        print(corners)
        sortPtsCCW(corners, sortPtsX, cmpPtX)
        print(corners)
        for i in range(4):
            img.draw_cross(corners[i][0], corners[i][1])
            img.draw_string(corners[i][0], corners[i][1], '%s'%(chr(ord('A') + i)))


    img.draw_rectangle(QQVGAscreenROI[0], QQVGAscreenROI[1], QQVGAscreenROI[2], QQVGAscreenROI[3], color = blue, thickness = 2)


