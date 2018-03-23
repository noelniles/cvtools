from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal


class AlignmentTask(QObject):
    finished_aligning = pyqtSignal()
    output = None

    def __init__(self, ref, off, func):
        self.func = func
        self.ref = ref
        self.off = off

    def run(self):
        self.output = self.func(self.ref, self.off)
        self.finished_aligning.emit()
        

