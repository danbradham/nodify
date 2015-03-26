from PySide import QtCore, QtGui


class Connection(QtGui.QGraphicsPathItem):


    def __init__(self, parent_a, parent_b=None, w=2, color=None):
        super(NodeSlot, self).__init__()

        self.parent_a = parent_a
        self.parent_b = parent_b

    def boundingBox(self):
        pass

    def paint(self):
        pass
