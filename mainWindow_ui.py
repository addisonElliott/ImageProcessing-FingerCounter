# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 136)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.setupPatchesButton = QtWidgets.QPushButton(self.centralwidget)
        self.setupPatchesButton.setObjectName("setupPatchesButton")
        self.verticalLayout.addWidget(self.setupPatchesButton)
        self.runTestingButton = QtWidgets.QPushButton(self.centralwidget)
        self.runTestingButton.setObjectName("runTestingButton")
        self.verticalLayout.addWidget(self.runTestingButton)
        self.runTrainingButton = QtWidgets.QPushButton(self.centralwidget)
        self.runTrainingButton.setObjectName("runTrainingButton")
        self.verticalLayout.addWidget(self.runTrainingButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SIUE Finger Detector"))
        self.setupPatchesButton.setText(_translate("MainWindow", "Setup Patches"))
        self.runTestingButton.setText(_translate("MainWindow", "Run Testing"))
        self.runTrainingButton.setText(_translate("MainWindow", "Run Training"))

