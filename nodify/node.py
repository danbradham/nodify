'''
node
====
QGraphicItem subclass.
'''

from PySide import QtCore, QtGui
from .slot import Slot


class Side(object):
    '''Enum Representing the side of a Node'''

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3


class Node(QtGui.QGraphicsItem):

    node_slots = [Side.LEFT, Side.TOP, Side.RIGHT, Side.BOTTOM]

    def __init__(self, label, x, y, w, h, label_color=None,
                 color=None, parent=None, scene=None):

        super(Node, self).__init__(parent, scene)

        self._scaling = False
        self._font = QtGui.QFont("Helvetica", 12)
        self._label = label
        self.label_color = label_color or QtGui.QColor.fromRgb(255, 255, 255)
        self.color = color or QtGui.QColor.fromRgb(55, 55, 55)

        self.setFlags(
            QtGui.QGraphicsItem.ItemIsMovable |
            QtGui.QGraphicsItem.ItemIsSelectable |
            QtGui.QGraphicsItem.ItemIsFocusable)

        self.drop_shadow = QtGui.QGraphicsDropShadowEffect(
            blurRadius=12,
            color=QtGui.QColor(0, 0, 0, 145),
            offset=QtCore.QPointF(0, 2),
            )
        self.setGraphicsEffect(self.drop_shadow)
        self.set_bounds(self._label)
        self.set_rect(x, y, w, h)
        self.slots = [Slot(i, parent=self) for i in self.node_slots]

    def update_children(self):
        for item in self.childItems():
            if hasattr(item, 'reposition'):
                item.reposition()

    @property
    def scaling(self):
        return self._scaling

    @scaling.setter
    def scaling(self, value):
        self._scaling = value
        if not self._scaling:
            self.setFlags(
                QtGui.QGraphicsItem.ItemIsMovable |
                QtGui.QGraphicsItem.ItemIsSelectable |
                QtGui.QGraphicsItem.ItemIsFocusable)
        else:
            self.setFlags(
                QtGui.QGraphicsItem.ItemIsSelectable |
                QtGui.QGraphicsItem.ItemIsFocusable)

    def mousePressEvent(self, event):
        pos = event.pos()
        if pos.x() > self.rect.width()-10 and pos.y() > self.rect.height()-10:
            self.scaling = True
            self.start_pos = pos
            self.start_rect = self.rect

        z = 0
        items = self.scene().items()
        for item in items:
            if isinstance(item, self.__class__) and item.zValue() >= z:
                z = item.zValue() + 0.1
                item.setZValue(z - 0.1)
        self.setZValue(z)

        super(Node, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if not self.scaling:
            super(Node, self).mouseMoveEvent(event)
            return

        self.prepareGeometryChange()

        pos = event.pos()
        v = pos - self.start_pos
        w = self.start_rect.width() + v.x()
        h = self.start_rect.height() + v.y()
        self.set_rect(self.rect.x(), self.rect.y(), w, h)
        self.update(self.rect)
        self.update_children()

        super(Node, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        '''Make sure we disable corner scaling after we release mouse.'''
        self.scaling = False
        super(Node, self).mouseReleaseEvent(event)

    def set_rect(self, x, y, w, h):
        if w < self._min_width:
            w = self._min_width
        if h < self._min_height:
            h = self._min_height
        self.rect = QtCore.QRectF(x, y, w, h)

    def set_bounds(self, text):
        fm = QtGui.QFontMetrics(self._font)
        self._min_width = fm.width(text) + 48
        self._min_height = fm.height() + 24

    def set_label(self, text):
        self._label = text
        self.set_bounds(text)
        self.update()

    def set_label_color(self, color):
        self.label_color = color
        self.update()

    def set_color(self, color):
        self.color = color
        self.update()

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.fillRect(
            self.rect,
            self.color if not self.isSelected() else self.color.lighter(120))
        painter.setFont(self._font)
        painter.setPen(self.label_color)
        painter.drawText(self.rect, QtCore.Qt.AlignCenter, self._label)

        w = self.rect.width()
        h = self.rect.height()
        pnt_a = QtCore.QPointF(w - 14, h)
        pnt_b = QtCore.QPointF(w, h - 14)
        pnt_c = QtCore.QPointF(w, h)
        resize_polygon = QtGui.QPolygonF()
        resize_polygon.append(pnt_a)
        resize_polygon.append(pnt_b)
        resize_polygon.append(pnt_c)
        resize_polygon.append(pnt_a)
        resize_path = QtGui.QPainterPath()
        resize_path.addPolygon(resize_polygon)
        painter.fillPath(resize_path, self.color.darker(120))
