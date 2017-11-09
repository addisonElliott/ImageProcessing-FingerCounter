from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PatchWidget(FigureCanvas):
    def __init__(self, parent=None, dpi=100):
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        fig.tight_layout()

        # self.toolbar = NavigationToolbar(self, self)
        # self.toolbar.hide()

        # self.mpl_connect('motion_notify_event', self.mouseMoved)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateFigure(self):
        self.axes.cla()

        self.draw()

        # def mouseMoved(self, event):
        #     if self.locationLabel is not None and event.inaxes:
        #         x, y, z = event.xdata, event.ydata, self.sliceNumber
        #     else:
        #         x, y, z = 0, 0, self.sliceNumber
        #
        #     self.locationLabel.setText("(%i, %i, %i)" % (x, y, z))
