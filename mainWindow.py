import mainWindow_ui
from algorithm import *
from profileWindow import *


class MainWindow(QMainWindow, mainWindow_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_setupPatchesButton_clicked(self):
        self.profileWindow = ProfileWindow(self)
        self.profileWindow.show()

    @pyqtSlot()
    def on_runTrainingButton_clicked(self):
        runAlgorithm(constants.trainingDir)
        print('Finished!')

    @pyqtSlot()
    def on_runTestingButton_clicked(self):
        runAlgorithm(constants.testingDir)
        print('Finished!')
