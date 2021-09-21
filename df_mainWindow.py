from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore

from outliner import Outliner
from console import Console
from viewport import Viewport
from renderView import RenderView
from attributeEditor import AttributeEditor
from node_editor_wnd import NodeEditorWnd

class mainWindow(QMainWindow):
    """MainWindow, containing all windows."""

    def __init__(self):
        super(mainWindow, self).__init__()
        self.setWindowTitle("Dragonfly")
        screenRes = [1280, 720, 1920, 1080]
        self.setGeometry(1200, 100, screenRes[0], screenRes[1]) # x = 1200 / 600
        icon = QtGui.QIcon("./assets/images/DF_icon.jpg")
        self.setWindowIcon(icon)
        self.show()

        self.nodeEditorWnd = NodeEditorWnd()
        self.outliner = Outliner()
        self.console = Console()
        self.viewport = Viewport()
        self.renderView = RenderView()
        self.attributeEditor = AttributeEditor()

        self.addDockWidgets()


    def addDockWidgets(self):
        self.setCentralWidget(self.nodeEditorWnd)

        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.console)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.renderView)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.viewport)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.attributeEditor)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.outliner)
