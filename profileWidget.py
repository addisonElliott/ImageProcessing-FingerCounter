import scipy.misc
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

import constants


class ProfileWidget(FigureCanvas):
    def __init__(self, parent=None, dpi=100):
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        fig.tight_layout()

        self.mpl_connect('button_press_event', self.mousePressed)
        self.mpl_connect('button_release_event', self.mouseReleased)
        self.mpl_connect('motion_notify_event', self.mouseMoved)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.image = None
        self.patches = list()

    def updateFigure(self):
        self.axes.cla()

        if self.image is not None:
            self.axes.imshow(self.image)

        for patch in self.patches:
            self.axes.add_patch(patch)

        self.draw()

    def mousePressed(self, event):
        pass
        # if event.button == 1:
        #     if self.currentPatch:
        #         self.currentPatch = None
        #     else:
        #         if not event.inaxes:
        #             return
        #
        #         self.currentPatch = Rectangle((event.xdata, event.ydata), 1, 1, linewidth=1,
        #                                       edgecolor='r', fill=False)
        #         self.patches.append(self.currentPatch)

    def mouseReleased(self, event):
        if not event.inaxes:
            return

        if event.button == 1:
            x, y = event.xdata, event.ydata
            w, h = constants.patchesSize, constants.patchesSize

            # Move clicked point to center
            x, y = x - w // 2, y - h // 2

            patch = Rectangle((x, y), w, h, linewidth=1, edgecolor='r', fill=False)
            self.patches.append(patch)
            self.updateFigure()
        elif event.button == 3:
            for patch in self.patches:
                x, y = patch.xy
                w, h = patch.get_width(), patch.get_height()
                x2, y2 = x + w, y + h

                if (event.xdata >= x and event.xdata <= x2) and (event.ydata >= y and event.ydata <= y2):
                    self.patches.remove(patch)
                    break

            self.updateFigure()

    def mouseMoved(self, event):
        pass
        # if self.currentPatch is None or not event.inaxes:
        #     return
        #
        # self.currentPatch.set_width(event.xdata - self.currentPatch.get_x())
        # self.currentPatch.set_height(event.ydata - self.currentPatch.get_y())
        #
        # self.updateFigure()

    def loadProfile(self, imagePath, patches):
        self.image = scipy.misc.imread(imagePath)
        self.patches.clear()

        for patch in patches:
            x, y = patch[0], patch[1]
            w, h = patch[2], patch[3]

            patch = Rectangle((x, y), w, h, linewidth=1, edgecolor='r', fill=False)
            self.patches.append(patch)

        self.updateFigure()

    def getPatches(self):
        patches = list()

        for patch in self.patches:
            patches.append((int(patch.get_x()), int(patch.get_y()), int(patch.get_width()), int(patch.get_height())))

        return patches