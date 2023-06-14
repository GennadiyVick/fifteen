# -*- coding: utf-8 -*-
# Author Roganov G.V. roganovg@mail.ru
# License GNUGPL3 in LICENSE.txt file.
# Also see README.txt
''' UI and menu create module '''
from PyQt5 import QtCore, QtGui, QtWidgets
from mygraphicsview import MyGraphicsView
from lang import Lang

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.lang = Lang()
        #MainWindow.resize(512, 534)
        self.windowSize = 512
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setFixedSize(QtCore.QSize(self.windowSize, self.windowSize))

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
        self.menubar.setStyleSheet('''QMenuBar { color: #fff; padding:2px;border-bottom:1px solid rgba(63, 64, 66,1.000); background:rgba(196, 113, 36, 1.000)} QMenuBar::item {background:transparent;padding:4px} QMenuBar::item:selected {padding:4px;border-radius:4px;background:rgba(255, 255, 255, 0.145)} QMenuBar::item:pressed {padding:4px;margin-bottom:0;padding-bottom:0}
QMenu {background:rgba(196, 113, 36, 1.000);padding:8px 0; color: #fff; }QMenu::separator {margin:4px 0;height:1px;}QMenu::item {padding:4px 19px}QMenu::item:selected {background:rgba(255, 255, 255, 0.133); border-radius:6px;}QMenu::icon {padding-left:10px;width:14px;height:14px}''')
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.mNew = QtWidgets.QMenu(self.menu)
        self.mNew.setObjectName("mNew")

        MainWindow.setMenuBar(self.menubar)

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
        self.menu.addAction(self.aQuit)
        self.menubar.addAction(self.menu.menuAction())


        self.aNew.setShortcut("N")
        self.aNew4.setText("4x4")
        self.aNew5.setText("5x5")
        self.aNew6.setText("6x6")
        self.aQuit.setShortcut("Q")

        self.retranslateUi(MainWindow, self.lang)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, lang):
        MainWindow.setWindowTitle(lang.tr("title"))
        self.menu.setTitle(lang.tr("game"))
        self.mNew.setTitle(lang.tr("newgame"))
        self.aQuit.setText(lang.tr("quit"))
        self.aNew.setText(lang.tr("mix"))

