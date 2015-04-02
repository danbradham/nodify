from PySide import QtCore, QtGui
from .node import Slot
from .connection import MousePath, Connection


class Scene(QtGui.QGraphicsScene):

    def __init__(self, color=None, parent=None):
        super(Scene, self).__init__(parent)
        self.set_color(color or QtGui.QColor.fromRgb(45, 45, 45))
        self._mouse_path = None
        self._mouse_path_slot = None

    def set_color(self, color):
        self.color = color
        brush = QtGui.QBrush(self.color, QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(brush)
        self.update()

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos())
        if isinstance(item, Slot):
            if not self._mouse_path:
                self._mouse_path_slot = item
                self._mouse_path = MousePath(scene=self)
                self._mouse_path.pen.setColor(item.color.darker(120))
                event.accept()
                return

        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._mouse_path:
            path = QtGui.QPainterPath(self._mouse_path_slot.center())
            path.lineTo(event.scenePos())
            self._mouse_path.setPath(path)

        super(Scene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        item = self.itemAt(event.scenePos())

        if self._mouse_path:
            if isinstance(item, Slot):
                print 'Adding connection'
                c = Connection(self._mouse_path_slot, item)
                self.addItem(c)
                self._mouse_path_slot.connect(item, c)
                item.connect(self._mouse_path_slot, c)
                self._mouse_path_slot.update()
                item.update()
            self.removeItem(self._mouse_path)
            self._mouse_path = None
            self._mouse_path_slot = None

        super(Scene, self).mouseReleaseEvent(event)
