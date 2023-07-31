import sensor, image, time
from pyb import UART, LED
import json, math


# 垂直方向和水平方向的ROI区域数量
roiHorNum = 10
roiVerNum = 8
# 线的阈值，默认为黑色
lineThreshold = [(0, 27, -128, 127, -128, 127)]
blackThreshold = [(0, 27, -128, 127, -128, 127)]


def sensorSet():
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.skip_frames(time = 200)
    sensor.set_contrast(1)
    sensor.set_auto_gain(False)
    sensor.set_auto_whitebal(False)


def genROIhor(n):
    uWidth = math.ceil(320 / n)
    _roiHor = []

    for i in range(n):
        _roiHor.append([i*uWidth, 100, uWidth, 40])

    return _roiHor


def genROIver(n):
    uHeight = math.ceil(240 / n)
    _roiVer = []

    for i in range(n):
        _roiVer.append([280, i*uHeight, 40, uHeight])

    return _roiVer


def maxBlob(blobs):
    curPixel = 0;
    maxB = 0
    for b in blobs:
        if curPixel < b.pixels():
            curPixel = b.pixels()
            maxB = b

    return maxB


def drawRoiRects(img, rois, color, thickness):
    for roi in rois:
        img.draw_rectangle(roi, color = color, thickness = thickness)


def getDir(img, rois, thresholds):
    for i in range(len(rois)):
        tgtBlobs = img.find_blobs(thresholds, roi = rois[i], pixels_threshold = 100, area_threshold = 20, merge = True)
        if(tgtBlobs):
            img.draw_cross(tgtBlobs[0][5], tgtBlobs[0][6], color = (0, 0, 255))
            return i
    return -1


def findLine(img, rois, thresholds, beginPos):
    for i in range(beginPos, len(rois)):
        tgtBlobs = img.find_blobs(thresholds, roi = rois[i], pixels_threshold = 100, area_threshold = 20, merge = True)
        if(not tgtBlobs):
            return False
        img.draw_cross(tgtBlobs[0][5], tgtBlobs[0][6])
    return True


roisX=genROIhor(roiHorNum)
roisY=genROIver(roiVerNum)
sensorSet()
clock = time.clock()

curX = 4
curY = 0
preY = -1
fwdFG = 1
lineMark = 0

while(True):
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
    #img = sensor.snapshot()
    verLines = []
    horLines = []

    # 画轮廓
    drawRoiRects(img, roisX, (255, 0, 0), 2)
    drawRoiRects(img, roisY, (0, 255, 0), 3)

    # 获取左右，前后信息
    curX = getDir(img, roisX, blackThreshold)
    preY = curY
    curY = getDir(img, roisY, blackThreshold)

    # 获取前进后退，如果preY>curY，说明小车在后退
    if preY > curY:
        fwdFG = 0
    elif preY < curY:
        fwdFG = 1
    print("preY: %d, curY: %d, FLAG: %d"%(preY, curY, fwdFG))

    # 当X轴方向的线从正方向经过中间位置，标记一次
    if(findLine(img, roisX, blackThreshold, curX) and fwdFG):
        lineMark += 1

    # Draw FPS
    img.draw_string(0, 0, "FPS:%.2f"%(clock.fps()))
    img.draw_string(0, 0, "\nDir:%d"%(getDir(img, roisX, blackThreshold)))
    img.draw_string(0, 0, "\nForward Flag:%d"%(fwdFG))

