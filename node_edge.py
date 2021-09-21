from node_graphics_edge import *


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False

class Edge:
    def __init__(self, scene, start_socket, end_socket, edge_type=EDGE_TYPE_DIRECT):

        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.grEdge = QDFGraphicsEdgeDirect(self) if edge_type==EDGE_TYPE_DIRECT else QDFGraphicsEdgeBezier(self)

        self.updatePositions()
        if DEBUG: print("Edge: ", self.grEdge.posSource, "to", self.grEdge.posDestination)
        self.scene.grScene.addItem(self.grEdge)

    def updatePositions(self):
        # we will need to add node pos to edge pos
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        if DEBUG: print("SS:", self.start_socket)
        if DEBUG: print("ES:", self.end_socket)
        self.grEdge.update()

    def remove_from_sockets(self):
        """ will be called when we will want to delete an edge
            will delete any references to the socket and edges itself"""
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket = None
        self.start_socket = None

    def remove():
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        # we delete the reference to QDFGraphicsEdge
        self.grEdge = None
        self.scene.removeEdge(self)
