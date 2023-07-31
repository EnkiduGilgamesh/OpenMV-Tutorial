import time, sensor, image
from image import SEARCH_EX, SEARCH_DS
from pyb import UART

# 重置传感器
sensor.reset()

# 传感器设置
sensor.set_contrast(5)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.QQVGA)
sensor.set_windowing((320, 240))
sensor.set_pixformat(sensor.GRAYSCALE)

sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False, value=100)

sensor.set_vflip(True)
sensor.set_hmirror(True)

clock = time.clock()
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

black_thresholds = (0, 40, -5, 5, -5, 5)
templates = []

for i in range(9):
    for j in range(9):
        templates.append("%s-%s"%(i,j))

pos = []
car_statu = 0
max_wait_time = 0
max_detect_time = 0

def judgeRectSize(rectangle):
    if rectangle.w() > 115 or rectangle.w() < 75:
        return False
    if rectangle.h() > 115 or rectangle.h() < 75:
        return False
    return True

def isRectInCenter(rectangle):
    centerX = rectangle.x() + rectangle.w() / 2
    centerY = rectangle.y() + rectangle.h() / 2
    if centerX > 65 and centerX < 85 and centerY > 45 and centerY < 65:
        return True
    return False

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)

    if car_statu == 0:
        rects = img.find_rects(threshold = 200)
        if len(rects) == 1 and judgeRectSize(rects[0]) and isRectInCenter(rects[0]):
            print("Find!!")
            # give points large enough, otherwise we cannot recognize them.
            img.draw_rectangle(rects[0].rect(), color=(255,0,0))
            spot_blobs = img.find_blobs([black_thresholds], roi = rects[0][0:4])#x_stride = 2, y_stride = 2, area_threshold=4, pixels_threshold=4,
            print(len(spot_blobs))
            for b in spot_blobs:
                if b.w() / b.h() > 0.9 and b.w() / b.h() < 1.1:
                    img.draw_rectangle(b.rect(), color=(255,0,0))
            if len(spot_blobs) == 4:
                car_statu = 1
                for s in spot_blobs:
                    x = s.x()+s.w()/2
                    y = s.y()+s.h()/2
                    print(x, y)
                    pos.append([x, y])
                    uart.write(chr(round((x - rects[0].x()) / rects[0].w() * 100)))
                    time.sleep_ms(100)
                    uart.write(chr(round((y - rects[0].y()) / rects[0].h() * 100)))
                    time.sleep_ms(100)

        max_wait_time += 1
        if max_wait_time < 1000:
            continue
        else:
            car_statu = 1
            uart.write(chr(25))
            time.sleep_ms(100)
            uart.write(chr(25))
            time.sleep_ms(100)
            uart.write(chr(75))
            time.sleep_ms(100)
            uart.write(chr(25))
            time.sleep_ms(100)
            uart.write(chr(75))
            time.sleep_ms(100)
            uart.write(chr(25))
            time.sleep_ms(100)
            uart.write(chr(75))
            time.sleep_ms(100)
            uart.write(chr(75))
            time.sleep_ms(100)

    elif car_statu == 1:
        #print("Change to 1")
        mark_blobs = img.find_blobs([black_thresholds], x_stride = 2, y_stride = 2, area_threshold=4, pixels_threshold=4)
        for m in mark_blobs:
            if m.w() < 20:
                if m.y() + m.h()/2 > 90:
                    car_statu = 2
                    uart.write("s")
                if m.x() + m.w()/2 > 80:
                    uart.write("l")
                else:
                    suart.write("r")
                break

    else:
        print("Change to 2")
        num = "0"
        for t in templates:
            template = image.Image(t)
            r = img.find_template(template, 0.66, step=4, search=SEARCH_EX)
            if r:
                num = t[0]
                img.draw_rectangle(r)
                uart.write(num)
                max_detect_time = 0
                car_statu = 1
                print(t)
                break
        max_detect_time += 1
        if max_detect_time > 100:
            uart.write(num)
            max_detect_time = 0
            car_statu = 1
