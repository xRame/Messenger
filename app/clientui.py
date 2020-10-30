# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'messenger.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Messenger(object):
    def setupUi(self, Messenger):
        Messenger.setObjectName("Messenger")
        Messenger.resize(395, 497)
        self.centralwidget = QtWidgets.QWidget(Messenger)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.chat = QtWidgets.QTextBrowser(self.centralwidget)
        self.chat.setGeometry(QtCore.QRect(20, 50, 351, 381))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chat.setFont(font)
        self.chat.setObjectName("chat")
        self.messageinput = QtWidgets.QTextEdit(self.centralwidget)
        self.messageinput.setGeometry(QtCore.QRect(20, 440, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.messageinput.setFont(font)
        self.messageinput.setObjectName("messageinput")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(330, 440, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.sendButton.setFont(font)
        self.sendButton.setObjectName("sendButton")
        self.nickinput = QtWidgets.QLineEdit(self.centralwidget)
        self.nickinput.setGeometry(QtCore.QRect(260, 20, 113, 20))
        self.nickinput.setObjectName("nickinput")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(220, 20, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        Messenger.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Messenger)
        self.statusbar.setObjectName("statusbar")
        Messenger.setStatusBar(self.statusbar)

        self.retranslateUi(Messenger)
        QtCore.QMetaObject.connectSlotsByName(Messenger)

    def retranslateUi(self, Messenger):
        _translate = QtCore.QCoreApplication.translate
        Messenger.setWindowTitle(_translate("Messenger", "MainWindow"))
        self.label.setText(_translate("Messenger", "VMessenger"))
        self.messageinput.setPlaceholderText(_translate("Messenger", "Enter text..."))
        self.sendButton.setText(_translate("Messenger", ">"))
        self.label_2.setText(_translate("Messenger", "name:"))
