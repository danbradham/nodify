from PySide import QtCore, QtGui


class Scene(QtGui.QGraphicsScene):

    def __init__(self, color=None, parent=None):
        super(Scene, self).__init__(parent)
        self.set_color(color or QtGui.QColor.fromRgb(45, 45, 45))

    def set_color(self, color):
        self.color = color
        brush = QtGui.QBrush(self.color, QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(brush)

    # def mousePressEvent(self, event):
    #     item = self.itemAt(event.scenePos())
    #     if item:
    #         item.mousePressEvent(event)
    #         event.accept()
