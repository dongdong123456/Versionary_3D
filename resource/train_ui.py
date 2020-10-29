# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'train.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtWidgets import  QProgressBar

class Ui_Train(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 800)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 200, 75, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 350, 75, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setCheckable(True)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 300, 75, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 250, 75, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setCheckable(True)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(300, 200, 250, 200))
        self.textBrowser.setObjectName("textBrowser")
        self.pb22 = QProgressBar(Form)
        # self.pb22.setInvertedAppearance(True)
        self.pb22.setGeometry(QtCore.QRect(300, 500, 250, 25))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "选择模型"))
        self.pushButton_4.setText(_translate("Form", "训练"))
        self.pushButton_2.setText(_translate("Form", "图片路径"))
