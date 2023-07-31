import sensor, image, time
from pyb import UART, LED
import json
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 200)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
uart = UART(3, 115200)
control_val=0
roi_far=[40,100,240,30]
roi_near=[0,190,320,30]
frame_header=55
led=LED(1)
led.on()
while(True):
    x_far=0;
    x_near=0;
    target_far_pixels=0
    target_far=-2
    target_near_pixels=0
    target_near=-2
    img = sensor.snapshot(1.8)
    blobs_far = img.find_blobs([(0, 27, -128, 127, -128, 127)],roi=roi_far,pixels_threshold = 24,area_threshold = 5,merge = True)
    blobs_near = img.find_blobs([(0, 27, -128, 127, -128, 127)],roi=roi_near,pixels_threshold = 24,area_threshold = 5,merge = True)
    img.draw_rectangle(roi_far)
    img.draw_rectangle(roi_near)
    for b in blobs_far:
        if target_far_pixels<b.pixels():
            target_far_pixels=b.pixels()
            target_far=b

    for b in blobs_near:
        if target_near_pixels<b.pixels():
            target_near_pixels=b.pixels()
            target_near=b


    if target_far_pixels > 0:
        x = target_far[0]
        y = target_far[1]
        width = target_far[2]
        height = target_far[3]
        img.draw_rectangle(target_far[0:4])
        img.draw_cross(target_far[5],target_far[6])
        x_far=target_far[5]
    if target_near_pixels > 0:
        x = target_near[0]
        y = target_near[1]
        width = target_near[2]
        height = target_near[3]
        img.draw_rectangle(target_near[0:4])
        img.draw_cross(target_near[5], target_near[6])
        x_near=target_near[5]
    uart.write(frame_header.to_bytes(1,'int')+x_far.to_bytes(2,'int')+x_near.to_bytes(2,'int'))
    print(x_far,x_near)

    # Draw FPS
    img.draw_string(0, 0, "FPS:%.2f"%(clock.fps()))
