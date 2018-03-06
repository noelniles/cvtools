import os
import sys

import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import (QEvent)
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow)
import cv2

from gui import Ui_MainWindow


class Lab(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Lab, self).__init__()
        QMainWindow.__init__(self, parent=None)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.image_view.setAcceptDrops(True)
        self.image_view.installEventFilter(self)
        self.image_view.getImageItem().setOpts(axisOrder='row-major')

    def eventFilter(self, obj, ev):
        if obj is self.image_view:
            ev.accept()
            print(ev.type())
            if ev.type() == QEvent.Drop:
                if ev.mimeData().hasUrls():
                    url = ev.mimeData().urls()[0]
                    img = cv2.imread(url.path())
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    #img = img.T
                    self.image_view.setImage(img)
        return False


def cli():
    pass

def main():
    args = cli()
    app = QApplication(sys.argv)
    lab = Lab()
    lab.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()