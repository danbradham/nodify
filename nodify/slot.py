from PySide import QtCore, QtGui


class Slot(QtGui.QGraphicsItem):
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
