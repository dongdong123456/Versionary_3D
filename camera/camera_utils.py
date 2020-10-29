# -*- coding: utf-8 -*-
# Created by WIN10 on 2020/10/10
# Copyright (c) 2020 WIN10. All rights reserved.
import camera.Device as Device
import camera.Data as Data
import numpy as np
import cv2
import datetime
import os
class Camera_Utils():
    def __init__(self):
        # 相机链接初始化
        ipAddress = '192.168.1.10'
        # instanciate classes
        self.deviceControl = Device.Control(ipAddress)
        self.deviceStreaming = Device.Streaming(ipAddress)
        self.frameData = Data.Data()

    # 链接相机
    def Comera_link(self):
        self.deviceControl.open()
        self.deviceControl.stopStream()
        self.deviceStreaming.openStream()
        self.deviceStreaming.sendBlobRequest()

    def getFrameData(self):
        self.deviceStreaming.getFrame()
        self.frameData.read(self.deviceStreaming.frame)

    def click_save(self, path):
        self.deviceControl.singleStep()
        self.getFrameData()
        if self.frameData.hasDepthMap:
            distanceData = self.frameData.depthmap.distance
            numCols = self.frameData.cameraParams.width
            numRows = self.frameData.cameraParams.height
            rgbdata = self.frameData.depthmap.intensity
            rgbmap = np.array(rgbdata).reshape(numRows, numCols, 4).astype(np.uint8)

            b = rgbmap[:, :, 0:3]

            img_bgr = cv2.cvtColor(b, cv2.COLOR_RGB2BGR)
            filename = datetime.datetime.now().strftime('%d_%H_%M_%S') + ".jpg"
            if not os.path.exists(path):
                os.makedirs(path)
            filepahe = path + '/' + filename
            cv2.imwrite(filepahe, img_bgr)
            return b, distanceData, numRows, numCols, img_bgr,self.frameData



    def close(self):
        self.deviceStreaming.closeStream()
        self.deviceControl.close()