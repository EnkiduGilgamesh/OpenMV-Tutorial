import sensor, image, time

black_thresholds = (0, 15, -5, 5, -5, 5)
white_thresholds = (95, 100, -5, 5, -5, 5)
sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.GRAYSCALE) # 格式为 RGB565. 也可考虑使用灰度
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(2000)            # 跳过10帧，使新设置生效
sensor.set_auto_whitebal(False)     # 关闭自动白平衡
sensor.set_auto_gain(False)         # 关闭自动曝光

sensor.set_vflip(True)
sensor.set_hmirror(True)

def getLatestSpot(spot_blobs, begin_pos):
    # 获得离出发位置最近的黑点的索引
    dis = 9999
    spot_index = -1
    for b in spot_blobs:            # b[x, y, w, h]
        spot_dis = (b[0] + b[2] / 2 - begin_pos[0])**2 + (b[1] - b[3] / 2 - begin_pos[1])**2
        if dis**2 > spot_dis:
            dis = spot_dis
            spot_index = spot_blobs.index(b)

    return spot_index


def sortSpot(spot_blobs, begin_pos):
    dist = []
    for b in spot_blobs:
        dist.append((b[0] + b[2] / 2 - begin_pos[0])**2 + (b[1] - b[3] / 2 - begin_pos[1])**2)
    for i in range(len(dist)):
        for j in range(i + 1, len(dist)):
            if dist[i] > dist[j]:
                temp_spot = spot_blobs[i]
                spot_blobs[i] = spot_blob[j]
                spot_blobs[j] = temp_spot
                temp_dist = dist[i]
                dist[i] = dist[j]
                dist[j] = dist[i]

    return spot_blobs


while(True):
    img = sensor.snapshot()         # Take a picture and return the image.
    blobs = img.find_blobs([black_thresholds], x_stride = 2, y_stride = 2, area_threshold=4, pixels_threshold=4)

    for b in blobs:
        img.draw_rectangle(b.rect(), color = (255, 0, 0))


