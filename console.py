from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore

class Console(QDockWidget):
    """docstring for Console."""

    def __init__(self):
        super(Console, self).__init__()
        self.setWindowTitle("Console")
        self.setMinimumHeight(150)

        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
