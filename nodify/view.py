'''
view
====
Defines a view class for maintaining a graphics scene.
'''

import math
from PySide import QtCore, QtGui


class View(QtGui.QGraphicsView):
    '''A View supporting smooth panning and zooming. Use Alt+Left Mouse to
    pan and Alt+Middle or Right Mouse to zoom. Dragging without Alt drags out
    a selection marquee.

    .. seealso::

        Documentation for :class:`QtGui.QGraphicsView`'''

    def __init__(self, *args, **kwargs):

        super(View, self).__init__(*args, **kwargs)

        self.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Set a massive canvas for seemingly unlimited pan and zoom
        self.setSceneRect(0, 0, 32000, 32000)
        self.centerOn(16000, 16000)

        self._last_pos = QtCore.QPoint(0, 0)
        self._drag_mod = QtCore.Qt.AltModifier
        self._drag_buttons = [QtCore.Qt.LeftButton]
        self._pan_buttons = [QtCore.Qt.LeftButton]
        self._zoom_buttons = [QtCore.Qt.MiddleButton, QtCore.Qt.RightButton]
        self._rel_scale = 1

    def mousePressEvent(self, event):
        '''Overloaded to support both marquee dragging and pan/zoom. Here we
        setup the dragging mode and store the anchor position.'''

        m = event.modifiers()
        b = event.buttons()

        if m == self._drag_mod or not b in self._drag_buttons:
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
        else:
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self._last_pos = self._anchor_pos = event.pos()

        super(View, self).mousePressEvent(event)

    def zoom(self, factor):
        '''Zoom the view.

        :param factor: Amount to scale'''

        rel_scale = self._rel_scale * factor
        if rel_scale < 0.2 or rel_scale > 8:
            return

        self._rel_scale = rel_scale

        transform = self.transform()
        transform.scale(factor, factor)
        self.setTransform(transform)


    def pan(self, x, y):
        '''Pan the view.

        :param x: Number of pixels in x
        :param y: Number of pixels in y'''

        self.translate(-x, -y)

    def mouseMoveEvent(self, event):

        if not event.modifiers() == QtCore.Qt.AltModifier:
            super(View, self).mouseMoveEvent(event)
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

        super(View, self).mouseReleaseEvent(event)
