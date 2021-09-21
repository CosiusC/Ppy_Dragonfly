from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from node_graphics_socket import QDFGraphicsSocket
from node_graphics_edge import QDFGraphicsEdge
from node_edge import Edge, EDGE_TYPE_BEZIER

# mode no operation
MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10.0

DEBUG = True


class QDFGraphicsView(QGraphicsView):
    def __init__(self, grScene, scene, parent=None):
        super(QDFGraphicsView, self).__init__(parent)
        self.grScene = grScene

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        self.initUI()
        self.setScene(self.grScene)

    def initUI(self):
        self.setRenderHints(
            QPainter.Antialiasing |
            QPainter.HighQualityAntialiasing |
            QPainter.TextAntialiasing |
            QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # scroll to the mouse position
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        # we will fake the event: make python thing it is LMB that is pressed
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                    Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

        print("MMB pressed")

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)
        print("MMB released")

    def leftMouseButtonPress(self, event):
        # we check on what we click to make something different depending on the widget clicked
        item = self.getItemAtclicked(event)

        # we store the potition of last LMB click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # logic
        if type(item) is QDFGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            result = self.edgeDragEnd(item)
            if result: return


        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get item which we release mouse button on
        item = self.getItemAtclicked(event)

        # logic
        if self.mode == MODE_EDGE_DRAG:

            if self.distanceBetweenClickAndReleaseIsOff(event):
                result = self.edgeDragEnd(item)
                if result: return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtclicked(event)

        if DEBUG:
            if isinstance(item, QDFGraphicsEdge):print('RMB DEBUG:', item.edge, ' connecting sockets:', item.edge.start_socket, '<-->', item.edge.end_socket)
            if type(item) is QDFGraphicsSocket: print('RMB DEBUG:', item.socket, 'has edge:', item.socket.edge)

            if item is None:
                print('SCENE:')
                print('  Nodes:')
                for node in self.grScene.scene.nodes: print('    ', node)
                print('  Edges:')
                for edges in self.grScene.scene.edges: print('    ', edges)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def edgeDragEnd(self, item):
        """ return True if we wanna skip the rest of the code """
        self.mode = MODE_NOOP

        if type(item) is QDFGraphicsSocket:
            if DEBUG: print('View::edgeDragEnd ~   previous edge:', self.previousEdge)
            if item.socket.hasEdge():
                item.socket.edge.remove()
            if DEBUG: print('View::edgeDragEnd ~   assign End Socket', item.socket)
            if self.previousEdge is not None: self.previousEdge.remove()
            if DEBUG: print('View::edgeDragEnd ~  previous edge removed')
            self.dragEdge.start_socket = self.last_start_socket
            self.dragEdge.end_socket = item.socket
            self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
            self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
            if DEBUG: print('View::edgeDragEnd ~  reassigned start & end sockets to drag edge')
            self.dragEdge.updatePositions()
            return True

        if DEBUG: print('View::edgeDragEnd ~ End dragging edge')
        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG: print('View::edgeDragEnd ~ about to set socket to previous edge:', self.previousEdge)
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        if DEBUG: print('View::edgeDragEnd ~ everything done.')

        return False



    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart ~ Start dragging edge')
        if DEBUG: print("View::edgeDragStart ~   assign Start Socket to:", item.socket)
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print('View::edgeDragStart ~', self.dragEdge)


    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ this measures is we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sqarre = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        # we return a condition (so true or false)
        return (dist_scene.x()*dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sqarre


    def wheelEvent(self, event):
        # calculate zoom factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        super().mouseMoveEvent(event)

    def getItemAtclicked(self, event):
        """ return the object on which we've clicked/release the mouse button"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
