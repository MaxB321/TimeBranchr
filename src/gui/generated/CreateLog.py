# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_log.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        if not LogDialog.objectName():
            LogDialog.setObjectName(u"LogDialog")
        LogDialog.resize(871, 473)
        self.buttonBox = QDialogButtonBox(LogDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(520, 430, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.label_h = QLabel(LogDialog)
        self.label_h.setObjectName(u"label_h")
        self.label_h.setGeometry(QRect(120, 80, 91, 21))
        self.lineEdit_h = QLineEdit(LogDialog)
        self.lineEdit_h.setObjectName(u"lineEdit_h")
        self.lineEdit_h.setGeometry(QRect(270, 80, 113, 22))
        self.lineEdit_m = QLineEdit(LogDialog)
        self.lineEdit_m.setObjectName(u"lineEdit_m")
        self.lineEdit_m.setGeometry(QRect(270, 130, 113, 22))
        self.lineEdit_s = QLineEdit(LogDialog)
        self.lineEdit_s.setObjectName(u"lineEdit_s")
        self.lineEdit_s.setGeometry(QRect(270, 180, 113, 22))
        self.label_m = QLabel(LogDialog)
        self.label_m.setObjectName(u"label_m")
        self.label_m.setGeometry(QRect(120, 130, 91, 21))
        self.label_s = QLabel(LogDialog)
        self.label_s.setObjectName(u"label_s")
        self.label_s.setGeometry(QRect(120, 180, 91, 21))

        self.retranslateUi(LogDialog)
        self.buttonBox.accepted.connect(LogDialog.accept)
        self.buttonBox.rejected.connect(LogDialog.reject)

        QMetaObject.connectSlotsByName(LogDialog)
    # setupUi

    def retranslateUi(self, LogDialog):
        LogDialog.setWindowTitle(QCoreApplication.translate("LogDialog", u"Dialog", None))
        self.label_h.setText(QCoreApplication.translate("LogDialog", u"Hours", None))
        self.label_m.setText(QCoreApplication.translate("LogDialog", u"Minutes", None))
        self.label_s.setText(QCoreApplication.translate("LogDialog", u"Seconds", None))
    # retranslateUi

