from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore

class AttributeEditor(QDockWidget):
    """docstring for AttributeEditor."""

    def __init__(self):
        super(AttributeEditor, self).__init__()
        self.setWindowTitle("AttributeEditor")
        self.setMinimumWidth(200)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
