from PySide import QtCore, QtGui


def straight_solver(start, end):
    '''Creates a PainterPath connecting two graphic items.'''

    path = QtGui.QPainterPath(start.center())
    path.lineTo(end.center())
    return path


def cubic_solver(start, end):
    start_point = start.center()
    start_vect = QtGui.QVector2D(start_point - start.parent.center())
    start_vect.normalize()
    start_cv = QtGui.QVector2D(start_point) + start_vect * 80
    cv1 = QtCore.QPointF(start_cv.x(), start_cv.y())

    end_point = end.center()
    end_vect = QtGui.QVector2D(end_point - end.parent.center())
    end_vect.normalize()
    end_cv = QtGui.QVector2D(end_point) + end_vect * 80
    cv2 = QtCore.QPointF(end_cv.x(), end_cv.y())

    path = QtGui.QPainterPath(start_point)
    path.cubicTo(cv1, cv2, end_point)
    return path


class Connection(QtGui.QGraphicsItem):

    def __init__(self, start, end, path_solver=cubic_solver,
                 *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)

        self.start = start
        self.end = end
        self.path_solver = path_solver
        self.path = path_solver(start, end)
        self.pen = QtGui.QPen(
            QtCore.Qt.white,
            2,
            QtCore.Qt.SolidLine,
            QtCore.Qt.FlatCap,
            QtCore.Qt.RoundJoin
        )
        self.drop_shadow = QtGui.QGraphicsDropShadowEffect(
            blurRadius=12,
            color=QtGui.QColor(0, 0, 0, 145),
            offset=QtCore.QPointF(0, 2)
        )
        self.setGraphicsEffect(self.drop_shadow)

    def boundingRect(self):
        return self.path.boundingRect()

    def paint(self, painter, option, widget):
        self.path = self.path_solver(self.start, self.end)
        painter.setPen(self.pen)
        painter.drawPath(self.path)


class MousePath(QtGui.QGraphicsPathItem):

    def __init__(self, *args, **kwargs):
        super(MousePath, self).__init__( *args, **kwargs)
        self.pen = QtGui.QPen(
            QtCore.Qt.white,
            2,
            QtCore.Qt.SolidLine,
            QtCore.Qt.FlatCap,
            QtCore.Qt.RoundJoin
        )
        self.setPen(self.pen)
        self.drop_shadow = QtGui.QGraphicsDropShadowEffect(
            blurRadius=12,
            color=QtGui.QColor(0, 0, 0, 145),
            offset=QtCore.QPointF(0, 2)
        )
        self.setGraphicsEffect(self.drop_shadow)
