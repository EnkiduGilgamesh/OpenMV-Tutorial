import sensor, image, time


black_thresholds = (250, 255, 250, 255, 250, 255)
white_thresholds = (0, 5, 0, 5, 0, 5)
sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565. 也可考虑使用灰度
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(2000)            # 跳过10帧，使新设置生效
sensor.set_auto_whitebal(False)     # 关闭自动白平衡
sensor.set_auto_gain(False)         # 关闭自动曝光


while(True):
    img = sensor.snapshot()         # Take a picture and return the image.

    spot_blobs = img.find_blobs([black_thresholds])

    # 过滤边界线

    # 过滤掉多个

