# -*- coding: utf-8 -*-
# Author Roganov G.V. roganovg@mail.ru
# License GNUGPL3 in LICENSE.txt file.
# Also see README.txt
''' UI and menu create module '''
from PyQt5 import QtCore, QtGui, QtWidgets
from mygraphicsview import MyGraphicsView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(512, 534)
        self.windowSize = 512
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setFixedSize(QtCore.QSize(self.windowSize, self.windowSize))
        #self.centralwidget.setMinimumSize(QtCore.QSize(512, 512))
        #self.centralwidget.setMaximumSize(QtCore.QSize(512, 512))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gv = MyGraphicsView(self.centralwidget)# QtWidgets.QGraphicsView(self.centralwidget)
        self.gv.setObjectName("gv")
        self.horizontalLayout.addWidget(self.gv)
        MainWindow.setCentralWidget(self.centralwidget)

        #create menu
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.windowSize, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.mNew = QtWidgets.QMenu(self.menu)
        self.mNew.setObjectName("mNew")
        #self.mInfo = QtWidgets.QMenu(self.menubar)
        #self.mInfo.setObjectName("mInfo")
        MainWindow.setMenuBar(self.menubar)
        #self.aSave = QtWidgets.QAction(MainWindow)
        #self.aSave.setObjectName("aSave")
        #self.aLoad = QtWidgets.QAction(MainWindow)
        #self.aLoad.setObjectName("aLoad")
        self.aQuit = QtWidgets.QAction(MainWindow)
        self.aQuit.setObjectName("aQuit")
        self.aNew4 = QtWidgets.QAction(MainWindow)
        self.aNew4.setObjectName("aNew4")
        self.aNew5 = QtWidgets.QAction(MainWindow)
        self.aNew5.setObjectName("aNew5")
        self.aNew6 = QtWidgets.QAction(MainWindow)
        self.aNew6.setObjectName("aNew6")
        self.mNew.addAction(self.aNew4)
        self.mNew.addAction(self.aNew5)
        self.mNew.addAction(self.aNew6)
        self.aNew = QtWidgets.QAction(MainWindow)
        self.aNew.setObjectName("aNew")
        self.mNew.addSeparator()
        self.mNew.addAction(self.aNew)
        self.menu.addSeparator()
        self.menu.addAction(self.mNew.menuAction())
        self.menu.addSeparator()
        #self.menu.addAction(self.aSave)
        #self.menu.addAction(self.aLoad)
        #self.menu.addSeparator()
        self.menu.addAction(self.aQuit)
        self.menubar.addAction(self.menu.menuAction())
        #self.menubar.addAction(self.mInfo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Fifteen puzzle game", "Игра Пятьнадцать"))
        self.menu.setTitle(_translate("Game", "Игра"))
        self.mNew.setTitle(_translate("New game", "Новая игра"))
        #self.mInfo.setTitle(_translate("Info", "Инфо"))
        #self.aSave.setText(_translate("Save game", "Сохранить игру"))
        #self.aSave.setShortcut(_translate("S", "S"))
        #self.aLoad.setText(_translate("Load game", "Загрузить игру"))
        #self.aLoad.setShortcut(_translate("L", "L"))
        self.aQuit.setText(_translate("Quit", "Выход"))
        self.aQuit.setShortcut(_translate("Q", "Q"))
        self.aNew.setText(_translate("Mix", "Размешать"))
        self.aNew.setShortcut(_translate("N", "N"))
        self.aNew4.setText(_translate("4x4", "4x4"))
        self.aNew5.setText(_translate("5x5", "5x5"))
        self.aNew6.setText(_translate("6x6", "6x6"))
