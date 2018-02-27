
#! /usr/bin/env python
"""
Demonstrates very basic use of ImageItem to display image data inside a ViewBox.
"""
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from PyQt5 import QtWidgets
import cv2

import ui

app = QtGui.QApplication([])

## Create window with GraphicsView widget
#win = pg.GraphicsLayoutWidget()
#win.show()  ## show widget alone in its own window
#win.setWindowTitle('pyqtgraph example: ImageItem')
#view = win.addViewBox()

## lock the aspect ratio so pixels are always square
#view.setAspectLocked(True)
mainwindow = QtWidgets.QMainWindow()
mainwindow.setWindowTitle('VideoPig Result Viewer')
win = ui.Ui_MainWindow()
win.setupUi(mainwindow)
mainwindow.show()

vb = pg.ViewBox()
win.original_view.setCentralItem(vb)
vb.setAspectLocked()
## Create image item
img = pg.ImageItem(border='w')
img.setOpts(axisOrder='row-major')
vb.addItem(img)
vb.autoRange()

## Set initial view bounds
#view.setRange(QtCore.QRectF(0, 0, 600, 600))

## Create random image
stream = cv2.VideoCapture('/home/me/data/videopig/results/dragx-GOPR9919.MP4')
data = np.random.normal(size=(15, 600, 600), loc=1024, scale=64).astype(np.uint16)
i = 0

updateTime = ptime.time()
fps = 0

def updateData():
    global img, data, i, updateTime, fps

    if stream.isOpened():
        success, frame = stream.read()

        if success:
            img.setImage(frame)



    QtCore.QTimer.singleShot(1, updateData)

updateData()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()