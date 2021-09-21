from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from node_graphics_socket import QDFGraphicsSocket

# mode no operation
MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10.0


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

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def edgeDragEnd(self, item):
        """ return True if we wanna skip the rest of the code """
        self.mode = MODE_NOOP
        print("End dragging edge")

        if type(item) is QDFGraphicsSocket:
            print("   assign End Socket")
            return True
        return False


    def edgeDragStart(self, event):
        print('Start dragging edge')
        print("   assign Start Socket")


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


    def getItemAtclicked(self, event):
        """ return the object on which we've clicked/release the mouse button"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
