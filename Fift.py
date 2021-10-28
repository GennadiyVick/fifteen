#!/usr/bin/env python3
# This Fifteen puzzle game
# In automove mode you can use mouse to click and keyboard arrows. (see settings.py)
# Author Roganov G.V. roganovg@mail.ru
# License GNUGPL3 in LICENSE.txt file.
# Also see README.txt
from PyQt5 import QtGui, QtCore,QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSystemTrayIcon, \
    QAction, QStyle, QMenu, QInputDialog, QMessageBox, QGraphicsScene, QFileDialog
from PyQt5.QtCore import QSize,QRect, Qt, QSettings, pyqtSignal, QTimer, QPointF
from PyQt5.QtGui import QPainter, QPixmap, QImage, QIcon
import sys
import os
import random
from mainwindow import Ui_MainWindow
import images
from piece import Piece, PieceList
from handmove import HandMove
from settings import AUTOMOVE

class MainWindow(QtWidgets.QMainWindow):
    onPieceMDSignal  = pyqtSignal(Piece,int,int)
    onPieceMUSignal  = pyqtSignal(Piece,int,int)
    onPieceMMSignal  = pyqtSignal(Piece,int,int)
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.setFixedSize(self.sizeHint())
        self.setWindowIcon(QIcon(':/15.png'))

        self.ui.aQuit.triggered.connect(self.actQuit)
        self.scene = QGraphicsScene(self)
        self.gv = self.ui.gv
        self.gv.setRenderHint(QPainter.Antialiasing);
        self.gv.setScene(self.scene)
        self.gv.setHorizontalScrollBarPolicy (Qt.ScrollBarAlwaysOff )
        self.gv.setVerticalScrollBarPolicy (Qt.ScrollBarAlwaysOff )
        self.gv.onKeyPress.connect(self.gvKeyPress)
        pixmap = QPixmap(":/bg.jpg")
        self.scene.addPixmap(pixmap)
        self.dg = QPixmap(':/digits.jpg')
        self.bv = QPixmap(':/bevel.png')
        self.mk = QPixmap(':/mask.png')
        self.piecelist = PieceList()
        self.matrixsize = 4
        self.imagesize = 128
        self.createPieces(self.matrixsize)
        #self.onPieceClickSignal.connect(self.pieceClick)
        self.onPieceMDSignal.connect(self.pieceMouseDown)
        self.onPieceMUSignal.connect(self.pieceMouseUP)
        self.onPieceMMSignal.connect(self.pieceMouseMove)
        self.anitimer = QTimer(self)
        self.anitimer.timeout.connect(self.onAniTimer)
        self.lockGame = False
        self.ui.aNew.triggered.connect(self.actNewGame)
        self.ui.aNew4.triggered.connect(self.actNew4Game)
        self.ui.aNew5.triggered.connect(self.actNew5Game)
        self.ui.aNew6.triggered.connect(self.actNew6Game)
        self.automovemode = AUTOMOVE
        self.handmove = None

    def actQuit(self):
        self.close()

    def resizeEvent(self,event):
        self.scene.setSceneRect(0,0,self.ui.windowSize, self.ui.windowSize )

    #when automovemode == true, see pieceMouseDown
    def pieceClick(self, piece):
        #print(self.piecelist.index(piece))
        if self.lockGame: return
        if piece == None: return
        plen = len(self.piecelist)
        lpiece = self.piecelist[-1]
        fx = lpiece.matX
        fy = lpiece.matY
        px, py = piece.getMatPos()

        if fy == py:
            if px < fx:
                for i in range(fx-1,px-1,-1):
                    piec = self.piecelist.findByMPos(i,py)
                    if piec != None:
                        startPos = QPointF(piec.matX*self.imagesize,piec.matY*self.imagesize)
                        stopPos = QPointF((i+1)*self.imagesize,py*self.imagesize)
                        piec.anistack.addAni(piec,startPos,stopPos)
                        piec.setMatPos(i+1,py, False)

            else:
                for i in range(fx+1,px+1):
                    piec = self.piecelist.findByMPos(i,py)
                    if piec != None:
                        startPos = QPointF(piec.matX*self.imagesize,piec.matY*self.imagesize)
                        stopPos = QPointF((i-1)*self.imagesize,py*self.imagesize)
                        piec.anistack.addAni(piec,startPos,stopPos)
                        piec.setMatPos(i-1,py, False)
        elif fx == px:
            if py < fy:
                for i in range(fy-1,py-1,-1):
                    piec = self.piecelist.findByMPos(px,i)
                    if piec != None:
                        startPos = QPointF(piec.matX*self.imagesize,piec.matY*self.imagesize)
                        stopPos = QPointF(px*self.imagesize,(i+1)*self.imagesize)
                        piec.anistack.addAni(piec,startPos,stopPos)
                        piec.setMatPos(px, i+1, False)
            else:
                for i in range(fy+1,py+1):
                    piec = self.piecelist.findByMPos(px,i)
                    if piec != None:
                        startPos = QPointF(piec.matX*self.imagesize,piec.matY*self.imagesize)
                        stopPos = QPointF(px*self.imagesize,(i-1)*self.imagesize)
                        piec.anistack.addAni(piec,startPos,stopPos)
                        piec.setMatPos(px,i-1, False)
        else:
            return

        if not self.anitimer.isActive(): self.anitimer.start(30)
        lpiece.setMatPos(px,py)

    def gvKeyPress(self, event):
        if not self.automovemode: return
        if self.lockGame: return
        l = len(self.piecelist)
        x = self.piecelist[l-1].matX
        y = self.piecelist[l-1].matY

        if event.key() == Qt.Key_Down:
            if y > 0:
                self.pieceClick(self.piecelist.findByMPos(x,y-1))
        elif event.key() == Qt.Key_Up:
            if y < self.matrixsize-1:
                self.pieceClick(self.piecelist.findByMPos(x,y+1))
        elif event.key() == Qt.Key_Right:
            if x > 0:
                self.pieceClick(self.piecelist.findByMPos(x-1,y))
        elif event.key() == Qt.Key_Left:
            if x < self.matrixsize-1:
                self.pieceClick(self.piecelist.findByMPos(x+1,y))

    def onAniTimer(self):
        stop = True
        for piece in self.piecelist:
            if not piece.anistack.doStep(): stop = False
        if stop:
            self.anitimer.stop()
            self.checkComlpeteGame()

    def checkComlpeteGame(self):
        for i in range(len(self.piecelist)):
            x = i % self.matrixsize
            y = i // self.matrixsize
            if self.piecelist[i].matX != x or self.piecelist[i].matY != y:
                return
        self.piecelist[-1].setMatPos(self.matrixsize-1,self.matrixsize-1)
        self.piecelist[-1].setVisible(True)
        self.lockGame = True

    def createPieces(self,msize):
        if msize < 4: return
        self.imagesize = self.ui.windowSize / msize
        sourceimagesize = self.dg.width() / msize
        for y in range(msize):
            for x in range(msize):
                piece = Piece({'mousedown': self.onPieceMDSignal, 'mouseup': self.onPieceMUSignal, 'mousemove': self.onPieceMMSignal})
                piece.setVisible(False)
                pix = piece.createPixmap(x,y,self.imagesize,sourceimagesize, self.dg,self.bv, self.mk)
                piece.setPixmap(pix)
                self.scene.addItem(piece)
                piece.setPos(x*self.imagesize,y*self.imagesize)
                self.piecelist.append(piece)
        self.mix()
        for i in range(len(self.piecelist)-1):
            self.piecelist[i].setVisible(True)


    def randMove(self,pl,fx,fy,ld = -1):
        dm = False
        lp = self.matrixsize - 1
        while not dm:
            d = random.randint(0,3)
            if d == ld: continue
            x = fx
            y = fy
            if d == 0:
                if fx == lp: continue
                else: x = fx+1
            elif d == 1:
                if fy == lp: continue
                else: y = fy+1
            elif d == 2:
                if fx == 0: continue
                else: x = fx-1
            else:
               if fy == 0: continue
               else: y = fy-1
            i = pl.index((x,y))
            if i < 0: continue
            pl[i] = fx,fy
            fx = x
            fy = y
            return fx,fy,(d+2) % 4

    def mix(self):
        pl = []
        for i in range(self.matrixsize*self.matrixsize-1):
            pl.append((i // self.matrixsize, i % self.matrixsize))
        plen = len(self.piecelist)
        fx = self.matrixsize-1 #self.piecelist[plen-1].matX
        fy = self.matrixsize-1 #self.piecelist[plen-1].matY
        d = -1
        for i in range(random.randint(1000,2000)):
            fx,fy,d = self.randMove(pl,fx,fy,d)
        for i in range(len(pl)):
            self.piecelist[i].setMatPos(pl[i][0],pl[i][1])
        self.piecelist[-1].setMatPos(fx,fy)

    def actNewGame(self):
        self.lockGame = False
        self.handmove = None
        self.piecelist[-1].setVisible(False)
        self.mix()


    def newGame(self, msize):
        self.matrixsize = msize
        self.handmove = None
        self.lockGame = False
        filter = "Images (*.jpg *.png)"
        fn,p = QFileDialog.getOpenFileName(self,filter=filter)
        if len(fn) == 0: return
        img = QPixmap(fn)
        ims = self.ui.windowSize
        sy = 0
        sx = 0
        sw = img.width()
        sh = img.height()
        if sw > sh:
            if sw < ims:
                sw,sh = ims,ims
            else:
                sx = (sw - sh) // 2
                sw = sh
        elif sh > sw:
            if sh < ims:
                sw,sh = ims,ims
            else:
                sy = (sh - sw) // 2
                sh = sw

        self.dg = QPixmap.fromImage(QImage(QSize(ims,ims), QImage.Format_ARGB32))
        painter = QPainter(self.dg)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0,0,self.ui.windowSize,self.ui.windowSize,img,sx,sy,sw,sh)

        while len(self.piecelist) > 0:
            self.scene.removeItem(self.piecelist.pop(0))
        self.createPieces(msize)


    def actNew4Game(self):
        self.newGame(4)

    def actNew5Game(self):
        self.newGame(5)

    def actNew6Game(self):
        self.newGame(6)

    def pieceMouseDown(self, piece, x, y):
        if self.lockGame: return
        if self.automovemode:
            #px, py = piece.getMatPos()
            self.pieceClick(piece)#,px,py)
            return
        elif self.handmove == None:
            self.handmove = HandMove.checkmove(self.piecelist,piece,x,y,self.imagesize)
            if self.handmove == None: return
        else:
            if self.handmove.contains(piece):
                self.handmove.mx = x
                self.handmove.my = y
                for p in self.handmove.pieces:
                    p.startX, p.startY = p.piece.pos().x(), p.piece.pos().y()
                self.handmove.canmove = True
            else: self.handmove.canmove = False


    def pieceMouseUP(self, piece, x, y):
        if self.lockGame: return
        if self.automovemode: return
        if self.handmove != None and self.handmove.canmove:
            fstat = self.handmove.checkfinish()
            if fstat == -1: return
            else:
                if fstat == 1:
                    self.handmove.setMatrix(self.piecelist)
                    self.checkComlpeteGame()
                self.handmove = None



    def pieceMouseMove(self, piece, x, y):
        if self.lockGame: return
        if self.automovemode: return
        if self.handmove != None and self.handmove.canmove:
            self.handmove.move(x,y)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(app)
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
