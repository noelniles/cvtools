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
from skimage.feature import CENSURE
from skimage import transform as tf

from aligner_interface import Ui_MainWindow


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
            self.reference_image_view.clear()
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
        if event_type == QEvent.MouseButtonDblClick:
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

    def register_censure(self, src, dst):
        censure = CENSURE(mode='STAR')
        censure.detect(src)
        src_keypoints = censure.keypoints

        censure.detect(dst)
        dst_keypoints = censure.keypoints

        self.show_keypoints(self.ref_viewbox, src_keypoints)
        self.show_keypoints(self.offset_viewbox, dst_keypoints)

    def register_brief(self, src, dst):
        extractor = BRIEF(patch_size=5)
        src_gray, dst_gray = src, dst

        src_keypoints = corner_peaks(corner_harris(src_gray), min_distance=1)
        dst_keypoints = corner_peaks(corner_harris(dst_gray), min_distance=1)

        extractor.extract(src_gray, src_keypoints)
        src_keypoints = src_keypoints[extractor.mask]
        src_descriptors = extractor.descriptors

        # Get the offset keypoints.
        extractor.extract(dst_gray, dst_keypoints)
        dst_keypoints = dst_keypoints[extractor.mask]
        dst_descriptors = extractor.descriptors

        # Get the matches
        matches = match_descriptors(src_descriptors, dst_descriptors,
            metric='hamming', cross_check=True)

        src_matches = src_keypoints[matches[:, 0]]
        dst_matches = dst_keypoints[matches[:, 1]]

        self.show_matches(self.ref_viewbox, src_matches)
        self.show_matches(self.offset_viewbox, dst_matches)

    def show_keypoints(self, viewbox, keypoints):
        for k in keypoints:
            print(k)
            viewbox.addItem(pg.CircleROI(k, 5))

    def show_matches(self, viewbox, matches):
        for m in matches:
            viewbox.addItem(pg.CircleROI(m, 5))

    def process(self):
        assert self.ref_img is not None, 'Reference image is empty'
        assert self.offset_img is not None, 'Offset image is empty'

        self.get_form_values()

        src_gray = rgb2gray(self.ref_img)
        dst_gray = rgb2gray(self.offset_img)

        if self.algorithm_name == 'BRIEF':
            self.register_brief(src_gray, dst_gray)
        elif self.algorithm_name == 'CENSURE':
            self.register_censure(src_gray, dst_gray)

def main():
    qapp = QApplication(sys.argv)

    aligner = Aligner()
    aligner.show()

    sys.exit(qapp.exec_())
if __name__ == '__main__':
    main()
