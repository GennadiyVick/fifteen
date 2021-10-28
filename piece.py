# Author Roganov G.V. roganovg@mail.ru
# License GNUGPL3 in LICENSE.txt file.
# Also see README.txt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QPainter, QImage
from animate import AniStack

class PieceList(list):
    def __init__(self):
        super().__init__()

    def findByMPos(self,x,y):
        for p in self:
            if p.matX == x and p.matY == y:
                return p
        return None

class Piece(QGraphicsPixmapItem):
    def __init__(self, signals = None): #, parent, signals
        super(QGraphicsPixmapItem,self).__init__()
        self.matX = -1
        self.matY = -1
        self.imagesize = 128
        if signals != None:
            self.onMouseDown = signals['mousedown']
            self.onMouseUp = signals['mouseup']
            self.onMouseMove = signals['mousemove']
        else:
            self.onMouseDown = None
            self.onMouseMove = None
            self.onMouseUp = None
        self.anistack = AniStack()

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        if self.onMouseDown != None:
            self.onMouseDown.emit(self,x,y)
    def mouseReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.onMouseUp != None:
            self.onMouseUp.emit(self,x,y)
        #return super().mouseReleaseEvent(event)
    def mouseMoveEvent(self, event):
        #return super().mouseMoveEvent(event)
        x = event.scenePos().x()
        y = event.scenePos().y()
        if self.onMouseMove != None:
            self.onMouseMove.emit(self,x,y)


    def createPixmap(self,mx,my,imagesize,sourceimgsize, digitsimage,bevelimage,maskimage):
        self.imagesize = imagesize
        pixmap = QPixmap.fromImage(QImage(QSize(imagesize,imagesize), QImage.Format_ARGB32))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        x = mx * sourceimgsize
        y = my * sourceimgsize
        painter.drawPixmap(0,0,imagesize,imagesize,digitsimage,x,y,sourceimgsize,sourceimgsize)
        painter.drawPixmap(0,0,imagesize,imagesize,bevelimage)
        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        painter.drawPixmap(0,0,imagesize,imagesize,maskimage)
        return pixmap

    def setMatPos(self,x,y, doPos = True):
        self.matX = x
        self.matY = y
        if doPos: self.setPos(x*self.imagesize,y*self.imagesize)

    def getMatPos(self):
        return self.matX, self.matY

