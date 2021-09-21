from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore

from node_scene import Scene
from node_graphics_view import QDFGraphicsView


class RenderView(QDockWidget):
    """docstring for RenderView."""

    def __init__(self):
        super(RenderView, self).__init__()
        self.setWindowTitle("RenderView")
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)

        self.menu_lyt = QHBoxLayout()
        self.layout.addLayout(self.menu_lyt)

        self.startRender_btn = QPushButton("Start render")
        self.startRender_btn.setFixedHeight(22)
        self.startRender_btn.clicked.connect(self.startRenderPressEvent)
        self.menu_lyt.addWidget(self.startRender_btn)

        # SCENE
        self.scene = Scene()
        self.grScene = self.scene.grScene

        self.view = QDFGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)


    def startRenderPressEvent(self):
        print("Starting render")
