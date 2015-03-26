from PySide import QtCore, QtGui


# class PathSolver(object):
#     '''Path Solvers create QPainterPaths from one object to another.'''

#     def __init__(self, start, end):
#         self.start = start
#         self.end = end

#     def get_path(self):
#         '''Returns a QPainterPath from start graphic to end graphic.'''


# class StraightSolver(PathSolver):
#     '''PathSolver returning a straight path'''

#     def get_path(self):

#         start_pos = self.start.center()
#         end_pos = self.end.center()
#         path = QtGui.QPainterPath(start_pos)
#         path.lineTo(end_pos)


# class CubicSolver(PathSolver):
#     '''PathSolver retuning a cubic curve path'''

#     def get_path(self):
#         pass


# class Connection(QtGui.QGraphicsItem):


#     def __init__(self, path_solver, *args, **kwargs):
#         super(NodeSlot, self).__init__(*args, **kwargs)

#         self.path_solver = path_solver

#     def boundingRect(self):
#         return self.path_solver.get_path().boundingRect()

#     def paint(self, painter, option, widget):
#         path = self.path_solver.get_path()
#         pen = QtGui.QPen(
#             brush=QtCore.Qt.White,
#             width=3,
#             s=QtCore.Qt.SolidLine,
#             c=QtCore.Qt.FlatCap,)
#         painter.setPen(pen)
#         painter.drawPath(path)


class MousePath(QtGui.QGraphicsPathItem):
    pass
