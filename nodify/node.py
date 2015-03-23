'''
node
====

Curve Connection Item
Node Item
Node Graph Scene
'''

import math
from PySide import QtCore, QtGui


class Side(object):
    '''Enum Representing the side of a Node'''

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3


class NodeViewer(QtGui.QGraphicsView):

    def __init__(self, *args, **kwargs):
        super(NodeViewer, self).__init__(*args, **kwargs)
        self._drag_mod = QtCore.Qt.AltModifier
        self.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSceneRect(0, 0, 320000, 320000)
        self.centerOn(16000, 16000)
        self._last_pos = QtCore.QPoint(0, 0)
        self._drag_buttons = [QtCore.Qt.LeftButton]
        self._pan_buttons = [QtCore.Qt.LeftButton]
        self._zoom_buttons = [QtCore.Qt.MiddleButton, QtCore.Qt.RightButton]

    def mousePressEvent(self, event):

        m = event.modifiers()
        b = event.buttons()

        if m == self._drag_mod or not b in self._drag_buttons:
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
        else:
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self._last_pos = self._anchor_pos = event.pos()

        super(NodeViewer, self).mousePressEvent(event)

    def zoom(self, factor):
        '''Zoom View

        :param factor: Amount to scale'''

        rect = self.sceneRect()
        transform = QtGui.QTransform.fromScale(factor, factor)
        scaled = transform.mapRect(rect)
        self.setSceneRect(scaled)

        transform = self.transform()
        transform.scale(factor, factor)
        self.setTransform(transform)

    def pan(self, x, y):
        '''Pan View

        :param x: Number of pixels in x
        :param y: Number of pixels in y'''

        self.translate(-x, -y)

    def mouseMoveEvent(self, event):

        if not event.modifiers() == QtCore.Qt.AltModifier:
            super(NodeViewer, self).mouseMoveEvent(event)
            return

        b = event.buttons()
        pos = event.pos()
        delta = pos - self._last_pos

        if b in self._pan_buttons:
            delta /= self.transform().m11()
            self.pan(-delta.x(), -delta.y())

        elif b in self._zoom_buttons:
            old_pos = self.mapToScene(self._anchor_pos)

            step = 0.02 * max(math.sqrt(delta.x() ** 2 + delta.y() ** 2), 1.0)
            if delta.x() < 0 or -delta.y() < 0:
                step *= -1
            factor = 1 + step
            self.zoom(factor) # Zoom

            delta = self.mapToScene(self._anchor_pos) - old_pos
            self.pan(-delta.x(), -delta.y()) # Pan to center on mouse pivot

        self._last_pos = pos

    def mouseReleaseEvent(self, event):

        if event.modifiers() == self._drag_mod:
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
        else:
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

        super(NodeViewer, self).mouseReleaseEvent(event)


class NodeScene(QtGui.QGraphicsScene):

    def __init__(self, color=None, parent=None):
        super(NodeScene, self).__init__(parent)
        self.set_color(color or QtGui.QColor.fromRgb(45, 45, 45))

    def set_color(self, color):
        self.color = color
        brush = QtGui.QBrush(self.color, QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(brush)


class NodeConnection(QtGui.QGraphicsPathItem):


    def __init__(self, parent_a, parent_b=None, w=2, color=None):
        super(NodeSlot, self).__init__()

        self.parent_a = parent_a
        self.parent_b = parent_b

    def boundingBox(self):
        pass

    def paint(self):
        pass


class NodeSlot(QtGui.QGraphicsItem):
    '''Input/Output slot graphic for a Node GraphicsItem.

    :param side: Side that :class:`NodeSlot` belongs to pass :class:`Side` enum
    :param parent: parent :class:`Node`
    '''

    def __init__(self, side, w=14, h=14, color=None, parent=None):
        super(NodeSlot, self).__init__(parent)

        self.side = side
        self.width = w
        self.height = h
        self.polygon = self._poly()
        self.color = color or QtGui.QColor.fromRgb(255, 255, 255, 255)
        self.parent = parent
        self.connected = False

        self.reposition()

    def reposition(self):
        pw = self.parent.rect.width()
        ph = self.parent.rect.height()
        if self.side == Side.LEFT:
            offset = QtCore.QPointF(0, ph * 0.5)
        elif self.side == Side.TOP:
            offset = QtCore.QPointF(pw * 0.5, 0)
        elif self.side == Side.RIGHT:
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
        '''QPoints for top side'''
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
        '''QPoints for bottom side'''
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

    def boundingRect(self):
        return self.polygon.boundingRect()

    def paint(self, painter, option, widget):
        path = QtGui.QPainterPath()
        path.addPolygon(self.polygon)
        if self.connected:
            painter.fillPath(path, self.color)
        else:
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Overlay)
            painter.fillPath(path, self.color.darker(120))


class Node(QtGui.QGraphicsItem):

    node_slots = [Side.LEFT, Side.TOP, Side.RIGHT, Side.BOTTOM]

    def __init__(self, label, x, y, w, h, label_color=None,
                 color=None, parent=None, scene=None):

        super(Node, self).__init__(parent, scene)

        self.label = label
        self.label_color = label_color or QtGui.QColor.fromRgb(255, 255, 255)
        self.rect = QtCore.QRectF(x, y, w, h)
        self.color = color or QtGui.QColor.fromRgb(55, 55, 55)
        self.slots = [NodeSlot(i, parent=self) for i in self.node_slots]

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
        self._scaling = False

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
        self.rect = QtCore.QRectF(
            self.rect.x(), self.rect.y(),
            self.start_rect.width() + v.x(), self.start_rect.height() + v.y()
        )
        self.update(self.rect)
        self.update_children()

        super(Node, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        '''Make sure we disable corner scaling after we release mouse.'''
        self.scaling = False
        super(Node, self).mouseReleaseEvent(event)

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
        painter.setPen(self.label_color)
        painter.drawText(self.rect, QtCore.Qt.AlignCenter, self.label)

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
