import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from lxml import etree

import constants
import profileWindow_ui


class ProfileWindow(QMainWindow, profileWindow_ui.Ui_ProfileWindow):
    def __init__(self, parent=None):
        super(ProfileWindow, self).__init__(parent)
        self.setupUi(self)

        self.handsModel = QStandardItemModel(self.handsListView)
        self.handsListView.setModel(self.handsModel)

        self.setupHandsList(constants.trainingDir)
        self.setupHandsList(constants.testingDir)

        if self.handsModel.rowCount() > 0:
            index = self.handsModel.createIndex(0, 0)
            self.handsListView.selectionModel().select(index, QItemSelectionModel.Select)

    def setupHandsList(self, dir):
        # Loop through each file in directory
        for name in os.listdir(dir):
            fullPath = os.path.join(dir, name)

            if not os.path.isdir(fullPath):
                continue

            self.handsModel.appendRow(QStandardItem(fullPath))

    def on_handsListView_clicked(self, index):
        self.currentPath = index.data()
        patchPath = os.path.join(self.currentPath, 'profile.xml')

        if os.path.exists(patchPath):
            self.config = etree.parse(patchPath)
        else:
            root = etree.Element('profile', SchemaVersion='1')
            imageTag = etree.SubElement(root, 'image')

            imageFilename = QFileDialog.getOpenFileName(self, 'Choose image to apply profile', self.currentPath,
                                        'Images (*.png *.jpg *.bmp)')
            imageFilename = imageFilename[0]
            pieces = imageFilename.split('/')
            imageFilename = pieces[-1]

            imageTag.text = imageFilename
            etree.SubElement(root, 'patches')

            self.config = etree.ElementTree(root)

        root = self.config.getroot()

        imageFilename = root.find('image').text
        imageFilename = os.path.join(self.currentPath, imageFilename)

        patchesXML = root.find('patches')
        patches = list()
        for patchXML in patchesXML:
            x, y = int(patchXML.attrib['x']), int(patchXML.attrib['y'])
            w, h = int(patchXML.attrib['w']), int(patchXML.attrib['h'])

            patches.append((x, y, w, h))

        self.profileWidget.loadProfile(imageFilename, patches)

    @pyqtSlot()
    def on_newButton_clicked(self):
        i = 4

    @pyqtSlot()
    def on_openButton_clicked(self):
        i = 4

    @pyqtSlot()
    def on_saveButton_clicked(self):
        if not self.config:
            return

        patchPath = os.path.join(self.currentPath, 'profile.xml')

        root = self.config.getroot()

        patchesXML = root.find('patches')
        # Remove existing patch lines and XML and write new ones
        for patchXML in patchesXML:
            patchesXML.remove(patchXML)

        patches = self.profileWidget.getPatches()
        for patch in patches:
            etree.SubElement(patchesXML, 'patch', x=str(patch[0]), y=str(patch[1]), w=str(patch[2]), h=str(patch[3]))

        self.config.write(patchPath, pretty_print=True)
