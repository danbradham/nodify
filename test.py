import sys
from PySide import QtGui, QtCore
import nodify


class Window(QtGui.QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Nodify Test')
        self.setMinimumSize(800, 600)

        l = QtGui.QGridLayout()
        l.setColumnStretch(0, 1)
        l.setRowStretch(2, 1)
        self.setLayout(l)

        self.line_label_node = QtGui.QLineEdit()
        self.button_add_node = QtGui.QPushButton('Add Node')
        self.button_add_node.clicked.connect(self.add_node)

        self.nodescene =  nodify.NodeScene()
        self.nodeview = nodify.NodeViewer()
        self.nodeview.setScene(self.nodescene)

        l.addWidget(self.nodeview, 0, 0, 3, 1)
        l.addWidget(self.line_label_node, 0, 1)
        l.addWidget(self.button_add_node, 1, 1)

    def add_node(self):
        label = self.line_label_node.text()
        new_node = nodify.Node(label, 0, 0, 160, 90)
        new_node.set_color(QtGui.QColor(155, 60, 60, 255))
        self.nodescene.addItem(new_node)


def main():

    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
