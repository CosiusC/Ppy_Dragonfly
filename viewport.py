from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore

class Viewport(QDockWidget):
    """docstring for Viewport."""

    def __init__(self):
        super(Viewport, self).__init__()
        self.setWindowTitle("Viewport")
        self.setMinimumHeight(300)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
