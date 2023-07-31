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
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((320, 240))
sensor.set_pixformat(sensor.GRAYSCALE)

sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False, value=100)


# NOTE: uncomment to load a keypoints descriptor from file
kptsModels = []

#imgModel = image.Image("NumModel/2.bmp")
#kptsModels.append(imgModel.find_keypoints(max_keypoints=150, threshold=10, scale_factor=1.2))

#kptsModels.append(image.load_descriptor("2.orb"))

for i in range(1, 5):
    #imgModel = image.Image("NumModel/%d.orb"%(i))
    kptsModels.append(image.load_descriptor("%d.orb"%(i)))
    #kptsModels.append(imgModel.find_keypoints(max_keypoints=150, threshold=10, scale_factor=1.2))

clock = time.clock()

while (True):
    clock.tick()
    img = sensor.snapshot()
    # NOTE: By default find_keypoints returns multi-scale keypoints extracted from an image pyramid.
    #kpts = img.find_keypoints(max_keypoints=150, threshold=10, normalized=True)
    kpts = img.find_keypoints(max_keypoints=150, threshold=10, normalized=True)
    m = 0
    tgt = 0

    for k in kptsModels:
        match = image.match_descriptor(k, kpts, threshold=85)
        if m < match.count():
            m = match.count()
            tgt = kptsModels.index(k) + 1


    time.sleep_ms(200)
    print(kpts, "matches %d"%(tgt))

    # Draw FPS
    img.draw_string(0, 0, "FPS:%.2f"%(clock.fps()))

