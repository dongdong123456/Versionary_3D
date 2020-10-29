# -*- coding: utf-8 -*-
# Created by WIN10 on 2020/10/9
# Copyright (c) 2020 WIN10. All rights reserved.
from resource.main_ui import Ui_Main
from PyQt5.QtWidgets import QMainWindow
from  PyQt5 import  QtWidgets
import sys
import os
class Main_logic(QMainWindow, Ui_Main):

    def __init__(self):
        super(Main_logic, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.connect()

    def connect(self):
        ###### 三个按钮事件 ######
        self.pushButton_4.clicked.connect(self.on_pushButton1_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton2_clicked)
        self.pushButton_3.clicked.connect(self.on_pushButton3_clicked)
        self.pushButton.clicked.connect(self.open_app)

    # 按钮一：打开第一个面板
    def on_pushButton1_clicked(self):
        self.stackedWidget.setCurrentIndex(2)

    # 按钮二：打开第二个面板
    def on_pushButton2_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    # 按钮三：打开第三个面板
    def on_pushButton3_clicked(self):
        self.stackedWidget.setCurrentIndex(1)


    def open_app(self):
        os.startfile('Labelme.exe')  # os.startfile（）打开外部应该程序，与windows双击相同




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    the_mainwindow = Main_logic()
    the_mainwindow.show()
    sys.exit(app.exec_())
