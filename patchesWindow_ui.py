# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'patchesWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PatchesWindow(object):
    def setupUi(self, PatchesWindow):
        PatchesWindow.setObjectName("PatchesWindow")
        PatchesWindow.resize(1024, 575)
        self.centralwidget = QtWidgets.QWidget(PatchesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout")
        self.patchWidget = PatchWidget(self.centralwidget)
        self.patchWidget.setObjectName("patchWidget")
        self.gridLayout.addWidget(self.patchWidget, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 376, 547))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.saveButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout_2.addWidget(self.saveButton, 4, 0, 1, 2)
        self.openButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.openButton.setObjectName("openButton")
        self.gridLayout_2.addWidget(self.openButton, 3, 0, 1, 2)
        self.handsListView = QtWidgets.QListView(self.scrollAreaWidgetContents)
        self.handsListView.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.handsListView.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.handsListView.setAlternatingRowColors(True)
        self.handsListView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.handsListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.handsListView.setObjectName("handsListView")
        self.gridLayout_2.addWidget(self.handsListView, 1, 0, 1, 1)
        self.newButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.newButton.setObjectName("newButton")
        self.gridLayout_2.addWidget(self.newButton, 2, 0, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 5)
        self.gridLayout.setColumnStretch(1, 3)
        PatchesWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PatchesWindow)
        QtCore.QMetaObject.connectSlotsByName(PatchesWindow)

    def retranslateUi(self, PatchesWindow):
        _translate = QtCore.QCoreApplication.translate
        PatchesWindow.setWindowTitle(_translate("PatchesWindow", "Setup Patches"))
        self.groupBox.setTitle(_translate("PatchesWindow", "Patches"))
        self.saveButton.setText(_translate("PatchesWindow", "Save"))
        self.openButton.setText(_translate("PatchesWindow", "Open"))
        self.newButton.setText(_translate("PatchesWindow", "New"))

from patchWidget import PatchWidget
