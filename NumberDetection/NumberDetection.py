# -*- python 3.8.10 -*-
# -*- coding:utf-8 -*-
####################################################################################################
 #File: \NumberDetection.py                                                                       # 
 #Project: NumberDetection                                                                        # 
 #Created Date: Thursday Mar 30th 2023, 3:20:50 pm                                                #
 #Author: Wenren Muyan                                                                            #
 #Comments:                                                                                       #
 #--------------------------------------------------------------------------------                #
 #Last Modified: 30/03/2023 07:05:40                                                              # 
 #Modified By: Wenren Muyan                                                                       # 
 #--------------------------------------------------------------------------------                #
 #Copyright (c) 2023 - future Wenren Muyan                                                        #
 #--------------------------------------------------------------------------------                #
 #HISTORY:                                                                                        #
 #Date				By				Comments                                                      #
 #--------------------------------------------------------------------------------                #
####################################################################################################

# Object tracking with keypoints example.
# Show the camera an object and then run the script. A set of keypoints will be extracted
# once and then tracked in the following frames. If you want a new set of keypoints re-run
# the script. NOTE: see the docs for arguments to tune find_keypoints and match_keypoints.

import sensor, time, image


def draw_keypoints(img, kpts):
    if kpts:
        print(kpts)
        img.draw_keypoints(kpts)
        img = sensor.snapshot()
        time.sleep_ms(1000)


# Reset sensor
sensor.reset()
# Sensor settings
sensor.set_contrast(3)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((320, 240))
sensor.set_pixformat(sensor.GRAYSCALE)

sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False, value=100)


# NOTE: uncomment to load a keypoints descriptor from file
kptsModels = []

for i in range(1, 9):
    imgModel = image.Image("/NumModel/{}.png".format(i))
    kptsModels.append(imgModel.find_keypoints(max_keypoints=150, threshold=10, scale_factor=1.2))

clock = time.clock()

while (True):
    clock.tick()
    img = sensor.snapshot()
    # NOTE: By default find_keypoints returns multi-scale keypoints extracted from an image pyramid.
    kpts = img.find_keypoints(max_keypoints=150, threshold=10, normalized=True)
    m = 0
    tgt = 0

    for k in kptsModels:
        match = image.match_descriptor(k, kpts, threshold=50)
        if match.count() > 10 and m < match.count():
            m = match
            tgt = kptsModels.index(k)

    print(kpts, "matches {}".format(tgt))

    # Draw FPS
    img.draw_string(0, 0, "FPS:%.2f"%(clock.fps()))

