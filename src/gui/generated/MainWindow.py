# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStackedWidget, QStatusBar,
    QToolBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(975, 637)
        self.actionDark_Mode = QAction(MainWindow)
        self.actionDark_Mode.setObjectName(u"actionDark_Mode")
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName(u"actionCopy")
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName(u"actionPaste")
        self.actionSign_Out = QAction(MainWindow)
        self.actionSign_Out.setObjectName(u"actionSign_Out")
        self.actionExport_CSV = QAction(MainWindow)
        self.actionExport_CSV.setObjectName(u"actionExport_CSV")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionDark_Mode_2 = QAction(MainWindow)
        self.actionDark_Mode_2.setObjectName(u"actionDark_Mode_2")
        self.actionShow_Subcategory_Totals = QAction(MainWindow)
        self.actionShow_Subcategory_Totals.setObjectName(u"actionShow_Subcategory_Totals")
        self.actionKeyboard_Shortcuts = QAction(MainWindow)
        self.actionKeyboard_Shortcuts.setObjectName(u"actionKeyboard_Shortcuts")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionShow_Toolbar = QAction(MainWindow)
        self.actionShow_Toolbar.setObjectName(u"actionShow_Toolbar")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox = QGroupBox(self.page)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(self.groupBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.groupBox)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.groupBox)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_4)

        self.frame_8 = QFrame(self.groupBox)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_8)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame)

        self.frame_5 = QFrame(self.groupBox)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.groupBox)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_6)

        self.frame_7 = QFrame(self.groupBox)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.frame_7)

        self.treeWidget_2 = QTreeWidget(self.groupBox)
        self.treeWidget_2.setObjectName(u"treeWidget_2")

        self.verticalLayout.addWidget(self.treeWidget_2)


        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 1, 1)

        self.treeWidget = QTreeWidget(self.page)
        font1 = QFont()
        font1.setBold(True)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Categories");
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font1);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.gridLayout_2.addWidget(self.treeWidget, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidget, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 975, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionExport_CSV)
        self.menuFile.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionUndo)
        self.menuView.addAction(self.actionDark_Mode_2)
        self.menuView.addAction(self.actionShow_Subcategory_Totals)
        self.menuView.addAction(self.actionShow_Toolbar)
        self.menuHelp.addAction(self.actionKeyboard_Shortcuts)
        self.menuHelp.addAction(self.actionAbout)
        self.menuSettings.addAction(self.actionSign_Out)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TimeBranchr", None))
        self.actionDark_Mode.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", u"Copy (Ctrl+C)", None))
        self.actionPaste.setText(QCoreApplication.translate("MainWindow", u"Paste (Ctrl+V)", None))
        self.actionSign_Out.setText(QCoreApplication.translate("MainWindow", u"Sign Out", None))
        self.actionExport_CSV.setText(QCoreApplication.translate("MainWindow", u"Export (CSV)", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo (Ctrl+Z)", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionDark_Mode_2.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.actionShow_Subcategory_Totals.setText(QCoreApplication.translate("MainWindow", u"Show Subcategory Totals", None))
        self.actionKeyboard_Shortcuts.setText(QCoreApplication.translate("MainWindow", u"Keyboard Shortcuts", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionShow_Toolbar.setText(QCoreApplication.translate("MainWindow", u"Show Toolbar", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        ___qtreewidgetitem = self.treeWidget_2.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Logs", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

