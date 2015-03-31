from PySide import QtCore, QtGui


class PathSolver(object):
    '''Path Solvers create QPainterPaths from one object to another.'''

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_path(self):
        '''Returns a QPainterPath from start graphic to end graphic.'''


class StraightSolver(PathSolver):
    '''PathSolver returning a straight path'''

    def get_path(self):

        start_pos = self.start.center()
        end_pos = self.end.center()
        path = QtGui.QPainterPath(start_pos)
        path.lineTo(end_pos)
        return path


class CubicSolver(PathSolver):
    '''PathSolver retuning a cubic curve path'''

    def get_path(self):
        pass


class Connection(QtGui.QGraphicsItem):


    def __init__(self, start, end, path_solver=StraightSolver,
                 *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)

        self.path_solver = path_solver(start, end)
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
        return self.path_solver.get_path().boundingRect()

    def paint(self, painter, option, widget):
        path = self.path_solver.get_path()
        painter.setPen(self.pen)
        painter.drawPath(path)


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
