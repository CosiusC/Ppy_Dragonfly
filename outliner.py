from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore

class Outliner(QDockWidget):
    """docstring for Outliner."""

    def __init__(self):
        super(Outliner, self).__init__()
        self.setWindowTitle("Outliner")
        self.setMinimumHeight(300)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
