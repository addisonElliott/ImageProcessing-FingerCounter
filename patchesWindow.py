from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import patchesWindow_ui


class PatchesWindow(QMainWindow, patchesWindow_ui.Ui_PatchesWindow):
    def __init__(self, parent=None):
        super(PatchesWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_newButton_clicked(self):
        i = 4

    @pyqtSlot()
    def on_openButton_clicked(self):
        i = 4

    @pyqtSlot()
    def on_saveButton_clicked(self):
        i = 4
