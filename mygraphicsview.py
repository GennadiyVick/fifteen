from PyQt5.QtWidgets import (QGraphicsView)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QDropEvent, QKeyEvent

class MyGraphicsView(QGraphicsView):
    onKeyPress  = pyqtSignal(QKeyEvent)
    def __init__(self, parent = None):
        super(MyGraphicsView, self).__init__(parent)
        self.setStyleSheet("QGraphicsView {border-width: 0px; border-style: none; outline:0px; background: transparent;}")

    def keyPressEvent(self, event):
        self.onKeyPress.emit(event)





