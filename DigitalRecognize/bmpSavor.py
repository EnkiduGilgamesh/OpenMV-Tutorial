# -*- python 3.8.10 -*-
# -*- coding:utf-8 -*-
####################################################################################################
 #File: \bmpSavor.py                                                                              #
 #Project: DigitalRecognize                                                                       #
 #Created Date: Friday Mar 31st 2023, 3:18:19 pm                                                  #
 #Author: Wenren Muyan                                                                            #
 #Comments:                                                                                       #
 #--------------------------------------------------------------------------------                #
 #Last Modified: 31/07/2023 02:20:0                                                               #
 #Modified By: Wenren Muyan                                                                       #
 #--------------------------------------------------------------------------------                #
 #Copyright (c) 2023 - future Wenren Muyan                                                        #
 #--------------------------------------------------------------------------------                #
 #HISTORY:                                                                                        #
 #Date				By				Comments                                                      #
 #--------------------------------------------------------------------------------                #
####################################################################################################


# 注意：请在运行此脚本后重置摄像头以查看新文件。
import sensor, time, image

# 重置传感器
sensor.reset()

# 传感器设置
sensor.set_contrast(1)
sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing((320, 240))
sensor.set_pixformat(sensor.RGB565)

##垂直翻转
#sensor.set_vflip(True)
##水平镜像
#sensor.set_hmirror(True)

sensor.skip_frames(time = 2500)

FILE_NAME = "1-3"
time.sleep_ms(15000)
img = sensor.snapshot()
# 注意：请参阅文档查看其他参数
img.save("/%s.bmp"%(FILE_NAME))

time.sleep_ms(100)
raise(Exception("Done! Please reset the camera"))
