# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from picture_logic import Picture_logic
from train_logic import Train_logic
from show_logic import Show_logic
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_Main(object):

    def setupUi(self, Version3D):
        picture = Picture_logic()
        train = Train_logic()
        show = Show_logic()
        Version3D.setObjectName("Version3D")
        Version3D.resize(1000, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Version3D.sizePolicy().hasHeightForWidth())
        Version3D.setSizePolicy(sizePolicy)
        Version3D.setMinimumSize(QtCore.QSize(1000, 800))
        Version3D.setMaximumSize(QtCore.QSize(1000, 800))
        self.centralwidget = QtWidgets.QWidget(Version3D)
        self.centralwidget.setObjectName("centralwidget")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(0, 0, 100, 800))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(100, 800))
        self.label_5.setMaximumSize(QtCore.QSize(100, 800))
        self.label_5.setAutoFillBackground(False)
        self.label_5.setStyleSheet("background-color:rgb(40, 231, 252)")
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(0, 30, 100, 100))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMaximumSize(QtCore.QSize(100, 100))
        self.label_6.setPixmap(QtGui.QPixmap('SICK-logo.png'))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 200, 100, 25))
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setChecked(True)
        self.pushButton_2.setAutoExclusive(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(0, 250, 100, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton.setAutoExclusive(True)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 300, 100, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setAutoExclusive(True)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(100, 0, 900, 800))
        self.stackedWidget.setObjectName("stackedWidget")
        # 将三个面板，加入stackedWidget
        self.stackedWidget.addWidget(picture)
        self.stackedWidget.addWidget(train)
        self.stackedWidget.addWidget(show)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 350, 100, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setCheckable(True)
        self.pushButton_4.setAutoExclusive(True)

        Version3D.setCentralWidget(self.centralwidget)


        self.retranslateUi(Version3D)
        QtCore.QMetaObject.connectSlotsByName(Version3D)

    def retranslateUi(self, Version3D):

        _translate = QtCore.QCoreApplication.translate
        Version3D.setWindowTitle(_translate("Version3D", "Version3D"))
        Version3D.setWindowIcon(QIcon('SICK-logo.png'))
        self.pushButton_2.setText(_translate("Version3D", "采图"))
        self.pushButton.setText(_translate("Version3D", "标定"))
        self.pushButton_3.setText(_translate("Version3D", "训练"))
        self.pushButton_4.setText(_translate("Version3D", "演示"))

