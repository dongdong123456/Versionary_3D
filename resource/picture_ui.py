# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'picture.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_Picture(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 800)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 200, 75, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 300, 75, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setCheckable(True)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(200, 60, 640, 512))
        self.graphicsView.setMinimumSize(QtCore.QSize(640, 512))
        self.graphicsView.setMaximumSize(QtCore.QSize(640, 512))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 250, 75, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setCheckable(True)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(800, 750, 35, 20))
        self.label.setMinimumSize(QtCore.QSize(35, 20))
        self.label.setMaximumSize(QtCore.QSize(35, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(830, 750, 16, 16))
        self.label_2.setMaximumSize(QtCore.QSize(16, 16))
        self.label_2.setSizeIncrement(QtCore.QSize(16, 16))
        self.label_2.setObjectName("label_2")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        m_red_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:red"

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "连接相机"))
        self.pushButton_3.setText(_translate("Form", "单次采集"))
        self.pushButton_2.setText(_translate("Form", "图片路径"))
        self.label.setText(_translate("MainWindow", "相机"))
        self.label_2.setStyleSheet(m_red_SheetStyle)
