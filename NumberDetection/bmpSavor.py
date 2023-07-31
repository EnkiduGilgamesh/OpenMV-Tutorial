# -*- python 3.8.10 -*-
# -*- coding:utf-8 -*-
####################################################################################################
 #File: \DescriptorSavor.py                                                                       #
 #Project: NumberDetection                                                                        #
 #Created Date: Friday Mar 31st 2023, 3:18:19 pm                                                  #
 #Author: Wenren Muyan                                                                            #
 #Comments:                                                                                       #
 #--------------------------------------------------------------------------------                #
 #Last Modified: 31/03/2023 03:18:43                                                              #
 #Modified By: Wenren Muyan                                                                       #
 #--------------------------------------------------------------------------------                #
 #Copyright (c) 2023 - future Wenren Muyan                                                        #
 #--------------------------------------------------------------------------------                #
 #HISTORY:                                                                                        #
 #Date				By				Comments                                                      #
 #--------------------------------------------------------------------------------                #
####################################################################################################


# 特征点保存例程
# 此示例显示如何将关键点描述符保存到文件。向相机显示一个对象，然后运行
# 该脚本。该脚本将提取并保存关键点描述符和图像。
# 您可以使用keypoints_editor.py 来删除不需要的关键点。
#
# 注意：请在运行此脚本后重置摄像头以查看新文件。
import sensor, time, image

# 重置传感器
sensor.reset()

# 传感器设置
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.QQVGA)
sensor.set_windowing((320, 240))
sensor.set_pixformat(sensor.GRAYSCALE)

sensor.set_vflip(True)
sensor.set_hmirror(True)

sensor.skip_frames(time = 2500)

FILE_NAME = "1-3"
time.sleep_ms(15000)
img = sensor.snapshot()
# 注意：请参阅文档查看其他参数
# 注：默认情况下，find_keypoints返回从图像中提取的多尺度关键点。
img.save("/%s.pgm"%(FILE_NAME))

time.sleep_ms(100)
raise(Exception("Done! Please reset the camera"))
