# -*- coding: utf-8 -*-
# Created by WIN10 on 2020/10/9
# Copyright (c) 2020 WIN10. All rights reserved.




# -*- coding: utf-8 -*-
# Created by WIN10 on 2020/10/9
# Copyright (c) 2020 WIN10. All rights reserved.
from resource.picture_ui import Ui_Picture
from camera.camera_utils import Camera_Utils
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.Qt import QImage
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QMainWindow
class Picture_logic(QMainWindow, Ui_Picture):

    def __init__(self):
        super(Picture_logic, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.connect()
        self.cu = Camera_Utils()
        self.path='image'
        self.status=False
        self.m_green_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:green"
        self.m_red_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:red"

    def connect(self):

        self.pushButton.clicked.connect(self.comera_link)
        self.pushButton_2.clicked.connect(self.image_path)
        self.pushButton_3.clicked.connect(self.click_save)



    def click_save(self):
        if self.status==True:
            b, distanceData, numRows, numCols, img_bgr,frameData=self.cu.click_save(self.path)
            self.read_camera_image(img_bgr)
        else:
            QtWidgets.QMessageBox.critical(self, "错误", "连接相机")

    def comera_link(self,status):
        _translate = QtCore.QCoreApplication.translate
        if status==True:
            self.cu.Comera_link()
            self.label_2.setStyleSheet(self.m_green_SheetStyle)
            self.status=True
            self.pushButton.setText(_translate("Form", "断开相机"))
        else:
            self.cu.close()
            self.label_2.setStyleSheet(self.m_red_SheetStyle)
            self.status=False
            self.pushButton.setText(_translate("Form", "连接相机"))


    def image_path(self):
        fname = QFileDialog.getExistingDirectory(self, 'open file', '/')
        if fname:
            try:
                self.path=fname
            except:
                QtWidgets.QMessageBox.critical(self, "错误", "打开文件失败，可能是文件内型错误")


    # 相机图片展示
    def read_camera_image(self, cvimg):
        # 在QgraphicsScene上呈现检测结果图
        height, width, depth = cvimg.shape
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(cvimg)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)  # 将场景添加至视图
