import os
import sys

from PyQt5.QtCore import QEvent
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
import pyqtgraph as pg
from skimage import draw
from skimage import io
from skimage.color import rgb2gray
from skimage.feature import match_descriptors
from skimage.feature import corner_harris
from skimage.feature import corner_peaks
from skimage.feature import hog
from skimage.feature import plot_matches

from skimage.feature import ORB
from skimage.feature import BRIEF
from skimage import transform as tf

from aligner_interface import Ui_MainWindow
from alignment_methods import keypoints_and_descriptors_brief
from alignment_methods import keypoints_censure

class Aligner(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.ref_imitem = pg.ImageItem()
        self.ref_imitem.setOpts(axisOrder='row-major')
        self.ref_viewbox = pg.ViewBox()
        self.reference_image_view.setCentralWidget(self.ref_viewbox)
        self.ref_viewbox.addItem(self.ref_imitem)
        self.ref_viewbox.invertY()
        self.ref_viewbox.setAspectLocked()

        self.offset_imitem = pg.ImageItem()
        self.offset_imitem.setOpts(axisOrder='row-major')
        self.offset_viewbox = pg.ViewBox()
        self.offset_image_view.setCentralWidget(self.offset_viewbox)
        self.offset_viewbox.addItem(self.offset_imitem)
        self.offset_viewbox.invertY()
        self.offset_viewbox.setAspectLocked()

        self.setAcceptDrops(True)
        self.installEventFilter(self)

        self.has_reference_image = False
        self.has_offset_image = False

        self.ref_img = None
        self.offset_img = None

        self.detect_features_btn.clicked.connect(self.process)

        self.algorithm_name = None

        self.control_points = []

        self.mouse_offset = QPoint(35, 32)


    def get_form_values(self):
        self.algorithm_name = str(self.algorithm_selection.currentText())

    def get_event_location(self, event):
        try:
            if self.reference_image_view.geometry().contains(event.pos()):
                return self.ref_imitem
            if self.offset_image_view.geometry().contains(event.pos()):
                return self.offset_imitem
        except AttributeError:
            pass

    def paintEvent(self, event):
        for point in self.control_points:
            self.reference_image_view.addItem(pg.CircleROI(point, 5))
            print('drawing ellipse at ', point)

    def eventFilter(self, obj, event):
        event.accept()
        event_type = event.type()
        location = self.get_event_location(event)

        if event_type == QEvent.Drop:
            links = []
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                links.append(path)

            self.open_images(links, location=location)

        elif event_type == QEvent.MouseButtonDblClick:
            if location == self.ref_imitem:
                self.control_points.append(event.pos() - self.mouse_offset)
                self.update()

            print('got a double click at ', event.pos())

        return False

    def open_images(self, links, location=None):
        """Open one or more files.

        Args
            links (list): a list of filenames to open
        """
        # We only have room for two images.
        assert len(links) <= 2, 'Only 2 images can be opened at a time'

        for url in links:
            img = io.imread(url)
            assert img is not None, 'Image is empty'
            location.setImage(img)
            if location == self.ref_imitem:
                self.ref_img = img
            elif location == self.offset_imitem:
                self.offset_img = img

    def draw_points(self, viewbox, pointlist):
        for point in pointlist:
            viewbox.addItem(pg.CircleROI(point, 5))

    def process(self):
        assert self.ref_img is not None, 'Reference image is empty'
        assert self.offset_img is not None, 'Offset image is empty'

        self.get_form_values()

        if self.algorithm_name == 'BRIEF':
            kps1, descs1 = keypoints_and_descriptors_brief(self.ref_img)
            kps2, descs2 = keypoints_and_descriptors_brief(self.offset_img)
            self.draw_points(self.ref_viewbox, kps1)
            self.draw_points(self.offset_viewbox, kps2)
        elif self.algorithm_name == 'CENSURE':
            kps1 = keypoints_censure(self.ref_img)
            kps2 = keypoints_censure(self.offset_img)
            self.draw_points(self.ref_viewbox, kps1)
            self.draw_points(self.offset_viewbox, kps2)

def main():
    qapp = QApplication(sys.argv)

    aligner = Aligner()
    aligner.show()

    sys.exit(qapp.exec_())
if __name__ == '__main__':
    main()
