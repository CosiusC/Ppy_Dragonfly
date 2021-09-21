from node_graphics_node import QDFGraphicsNode
from node_content_widget import QDFNodeContentWidget
from node_socket import Socket, LEFT_BOTTOM, LEFT_TOP, RIGHT_TOP, RIGHT_BOTTOM


class Node():
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        self.scene = scene

        self.title = title

        self.content = QDFNodeContentWidget()
        self.grNode = QDFGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22


        # create sockets for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position= LEFT_BOTTOM)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

    @property
    def pos(self):
        return self.grNode.pos()        # will return QPointF class pos.x()
    def setPos(self, x, y):
        self.grNode.setPos(x, y)


    def getSocketPosition(self, index, position):

        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.grNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding *2 - index * self.socket_spacing
        else:
            # start from top
            # index * 20 -> for space between sockets
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing

        return x, y
