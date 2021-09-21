from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class QDFGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._color = QColor("#c9c9c9")
        self._color_selected = QColor("#4b7aff")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)


        self.setFlag(QGraphicsItem.ItemIsSelectable)
        # put the edge to the background
        self.setZValue(-1)

        # where the edge will start
        self.posSource = [0, 0]
        # where the edge will end
        self.posDestination = [200, 100]

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()

        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        """ will handle drawing QPainterPath from Point A to B """
        # this class will be an abstract class so we have to instanciate it
        raise NotImplemented("This methods has to be overriden in a child class")


class QDFGraphicsEdgeDirect(QDFGraphicsEdge):
    def updatePath(self):
        """ will calculate QPainterPath for connecting point a to b """
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)


class QDFGraphicsEdgeBezier(QDFGraphicsEdge):
    def updatePath(self):
        """ will calculate QPainterPath for connecting point a to b """
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]: dist *= 0-1

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + dist, s[1], d[0] - dist, d[1], self.posDestination[0], self.posDestination[1])
        self.setPath(path)
