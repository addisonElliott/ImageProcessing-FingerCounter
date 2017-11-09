from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import constants
import mainWindow_ui
from algorithm import *
from patchesWindow import *


class MainWindow(QMainWindow, mainWindow_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_setupPatchesButton_clicked(self):
        self.patchesWindow = PatchesWindow(parent=self)
        self.patchesWindow.show()

    @pyqtSlot()
    def on_runTrainingButton_clicked(self):
        runAlgorithm(constants.trainingDir)

    @pyqtSlot()
    def on_runTestingButton_clicked(self):
        runAlgorithm(constants.testingDir)
