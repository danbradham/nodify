'''
node
====
QGraphicItem subclass.
'''

from PySide import QtCore, QtGui
from .connection import Connection


class Sides(object):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    @staticmethod
    def iterate():
        for i in xrange(4):
            yield i


class Slot(QtGui.QGraphicsItem):
    '''Input/Output slot graphic for a Node GraphicsItem.

    :param side: Side that :class:`Slot` belongs to pass :class:`Sides` enum
    :param parent: parent :class:`Node`
    '''

    def __init__(self, side, w=14, h=14, color=None, parent=None):
        super(Slot, self).__init__(parent)

        self.side = side
        self.width = w
        self.height = h
        self.polygon = self._poly()
        self.color = color or QtGui.QColor.fromRgb(255, 255, 255, 255)
        self.parent = parent
        self.connection = None
        self.connection_item = None
        self.reposition()

        self.setAcceptDrops(True)

    def connect(self, slot, connection):
        self.connection = slot
        self.connection_item = connection

    def dropEvent(self, event):
        print event

    def reposition(self):
        pw = self.parent.rect.width()
        ph = self.parent.rect.height()
        if self.side == Sides.LEFT:
            offset = QtCore.QPointF(0, ph * 0.5)
        elif self.side == Sides.UP:
            offset = QtCore.QPointF(pw * 0.5, 0)
        elif self.side == Sides.RIGHT:
            offset = QtCore.QPointF(pw, ph * 0.5)
        else:
            offset = QtCore.QPointF(pw * 0.5, ph)

        self.setPos(offset)

    def set_color(self, color):
        self.color = color
        self.update()

    def set_size(self, w, h):
        self.width = width
        self.height = height
        self.polygon = self._poly()
        self.update()

    def l_pnts(self):
        '''QPoints for left side'''
        pnt_a = QtCore.QPointF(0, -self.height * 0.5)
        pnt_b = QtCore.QPointF(0, self.height * 0.5)
        pnt_c = QtCore.QPointF(self.width * 0.5, 0)
        return pnt_a, pnt_b, pnt_c

    def t_pnts(self):
        '''QPoints for up side'''
        pnt_a = QtCore.QPointF(-self.width * 0.5, 0)
        pnt_b = QtCore.QPointF(self.width * 0.5, 0)
        pnt_c = QtCore.QPointF(0, self.height * 0.5)
        return pnt_a, pnt_b, pnt_c

    def r_pnts(self):
        '''QPoints for right side'''
        pnt_a = QtCore.QPointF(0, -self.height * 0.5)
        pnt_b = QtCore.QPointF(0, self.height * 0.5)
        pnt_c = QtCore.QPointF(-self.width * 0.5, 0)
        return pnt_a, pnt_b, pnt_c

    def b_pnts(self):
        '''QPoints for down side'''
        pnt_a = QtCore.QPointF(-self.width * 0.5, 0)
        pnt_b = QtCore.QPointF(self.width * 0.5, 0)
        pnt_c = QtCore.QPointF(0, -self.height * 0.5)
        return pnt_a, pnt_b, pnt_c

    def _poly(self):
        pnt_a, pnt_b, pnt_c = (
            self.l_pnts,
            self.t_pnts,
            self.r_pnts,
            self.b_pnts
            )[self.side]()

        polygon = QtGui.QPolygonF()
        polygon.append(pnt_a)
        polygon.append(pnt_b)
        polygon.append(pnt_c)
        polygon.append(pnt_a)
        return polygon

    def center(self):
        return self.mapToScene(self.boundingRect().center())

    def boundingRect(self):
        return self.polygon.boundingRect()

    def paint(self, painter, option, widget):
        path = QtGui.QPainterPath()
        path.addPolygon(self.polygon)
        if self.connection:
            painter.fillPath(path, self.color)
        else:
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Overlay)
            painter.fillPath(path, self.color.darker(120))


class Node(QtGui.QGraphicsItem):

    flag_state = {
        'default': (
            QtGui.QGraphicsItem.ItemIsMovable |
            QtGui.QGraphicsItem.ItemIsSelectable |
            QtGui.QGraphicsItem.ItemIsFocusable |
            QtGui.QGraphicsItem.ItemSendsScenePositionChanges),
        'scaling': (
            QtGui.QGraphicsItem.ItemIsSelectable |
            QtGui.QGraphicsItem.ItemIsFocusable|
            QtGui.QGraphicsItem.ItemSendsScenePositionChanges),
    }

    def __init__(self, label, x, y, w, h, label_color=None,
                 color=None, parent=None, scene=None):

        super(Node, self).__init__(parent, scene)
        self._slots = {}

        self._scaling = False
        self._font = QtGui.QFont("Helvetica", 12)
        self._label = label
        self.label_color = label_color or QtGui.QColor.fromRgb(255, 255, 255)
        self.color = color or QtGui.QColor.fromRgb(55, 55, 55)

        self.setFlags(self.flag_state['default'])
        self.setHandlesChildEvents(False)
        self.drop_shadow = QtGui.QGraphicsDropShadowEffect(
            blurRadius=12,
            color=QtGui.QColor(0, 0, 0, 145),
            offset=QtCore.QPointF(0, 2),
            )
        self.setGraphicsEffect(self.drop_shadow)
        self.set_bounds(self._label)
        self.set_rect(x, y, w, h)

        self.add_slot('left', 0)
        self.add_slot('up', 1)
        self.add_slot('right', 2)
        self.add_slot('down', 3)

    def __getattr__(self, name):
        try:
            return self._slots[name]
        except KeyError:
            raise AttributeError('Attribute {} does not exist'.format(name))

    def add_slot(self, name, side):
        slot = Slot(side, parent=self)
        self._slots[name] = slot

    def del_slot(self, name):
        slot = self._slots.pop(name)
        self.scene().removeItem(slot)

    def update_children(self):
        for item in self.childItems():
            if hasattr(item, 'reposition'):
                item.reposition()

    def update_slots(self):
        for name, slot in self._slots.iteritems():
            if slot.connection_item:
                slot.connection_item.update()

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemScenePositionHasChanged:
            self.update_slots()
        return super(Node, self).itemChange(change, value)

    @property
    def scaling(self):
        return self._scaling

    @scaling.setter
    def scaling(self, value):
        self._scaling = value
        if not self._scaling:
            self.setFlags(self.flag_state['default'])
        else:
            self.setFlags(self.flag_state['scaling'])

    def mousePressEvent(self, event):
        event.accept()
        z = 0
        items = self.scene().items()
        for item in items:
            if isinstance(item, self.__class__) and item.zValue() >= z:
                z = item.zValue() + 0.1
                item.setZValue(z - 0.1)
        self.setZValue(z)

        pos = event.pos()
        if pos.x() > self.rect.width()-10 and pos.y() > self.rect.height()-10:
            self.scaling = True
            self.start_pos = pos
            self.start_rect = self.rect

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
        self.update_slots()

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

    def center(self):
        return self.mapToScene(self.rect.center())

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
