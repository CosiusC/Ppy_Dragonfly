from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore
import sys, json

from df_mainWindow import mainWindow

def enforceCssStyle(window):
    """set overall Dragonfly style sheet"""
    with open("./style.css", "r+") as cssFile:
        style = cssFile.read()
        window.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication([])
    window = mainWindow()
    enforceCssStyle(window)
    sys.exit(app.exec_())
