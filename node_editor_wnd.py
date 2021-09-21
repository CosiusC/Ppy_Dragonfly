from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from node_graphics_view import QDFGraphicsView
from node_node import Node
from node_edge import Edge
from node_scene import Scene


class NodeEditorWnd(QWidget):
    """NodeEditorWnd --> the node editor main window. all is appened from here."""

    def __init__(self):
        super(NodeEditorWnd, self).__init__()

        self.initUI()


    def initUI(self):
        self.setWindowTitle("Node editor")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # create graphics scene
        self.scene = Scene()
        # self.grScene = self.scene.grScene

        self.addNodes()

        # create a graphics view
        self.view = QDFGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)


        # self.addDebugContent()

    def addNodes(self):
        node1 = Node(self.scene, "My Awesome Node 1", inputs=[1, 2, 3], outputs = [1])
        node2 = Node(self.scene, "My Awesome Node 2", inputs=[1, 2, 3], outputs = [1])
        node3 = Node(self.scene, "My Awesome Node 3", inputs=[1, 2, 3], outputs = [1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0])
        edge1 = Edge(self.scene, node2.outputs[0], node3.inputs[0], type=2)

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)


        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("this is my awesome text", QFont("Ubuntu"))
        text.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello world")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
