from node_graphics_socket import QDFGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

DEBUG = False

class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=1):

        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        if DEBUG: print("socket -- creating with", self.index, self.position, "for node", self.node)

        self.grSocket = QDFGraphicsSocket(self, self.socket_type)

        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        # is there an edge connected or not
        self.edge = None

    def __str__(self):
        """ simplifying the debug """
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])


    def getSocketPosition(self):
        if DEBUG: print("   GSP: ", self.index, self.position, "node:", self.node)
        result = self.node.getSocketPosition(self.index, self.position)
        if DEBUG: print("   res", result)
        return result

    def setConnectedEdge(self, edge=None):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None
