# Measure the distance
#
# This example shows off how to measure the distance through the size in imgage
# This example in particular looks for yellow pingpong ball.

import sensor, image, time

# For color tracking to work really well you should ideally be in a very, very,
# very, controlled enviroment where the lighting is constant...
yellow_thresholds   = ( 56,   83,    5,   57,   63,   80)
black_thresholds = (0, 15, -5, 5, -5, 5)
# You may need to tweak the above settings for tracking green things...
# Select an area in the Framebuffer to copy the color settings.

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.

K=5000#the value should be measured

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    blobs = img.find_blobs([black_thresholds], x_stride = 2, y_stride = 2, area_threshold=4, pixels_threshold=4)
    if len(blobs) == 1:
        # Draw a rect around the blob.
        b = blobs[0]
        img.draw_rectangle(b[0:4]) # rect
        img.draw_cross(b[5], b[6]) # cx, cy
        Lm = (b[2]+b[3])/2
        length = K/Lm
        print(length)

    #print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
