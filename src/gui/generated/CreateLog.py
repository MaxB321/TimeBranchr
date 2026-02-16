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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        if not LogDialog.objectName():
            LogDialog.setObjectName(u"LogDialog")
        LogDialog.resize(871, 473)
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
        self.ok_btn = QPushButton(LogDialog)
        self.ok_btn.setObjectName(u"ok_btn")
        self.ok_btn.setGeometry(QRect(540, 410, 81, 26))
        self.cancel_btn = QPushButton(LogDialog)
        self.cancel_btn.setObjectName(u"cancel_btn")
        self.cancel_btn.setGeometry(QRect(670, 410, 81, 26))
        self.error_msg = QLabel(LogDialog)
        self.error_msg.setObjectName(u"error_msg")
        self.error_msg.setGeometry(QRect(320, 260, 131, 21))

        self.retranslateUi(LogDialog)

        QMetaObject.connectSlotsByName(LogDialog)
    # setupUi

    def retranslateUi(self, LogDialog):
        LogDialog.setWindowTitle(QCoreApplication.translate("LogDialog", u"Dialog", None))
        self.label_h.setText(QCoreApplication.translate("LogDialog", u"Hours:", None))
        self.label_m.setText(QCoreApplication.translate("LogDialog", u"Minutes:", None))
        self.label_s.setText(QCoreApplication.translate("LogDialog", u"Seconds:", None))
        self.ok_btn.setText(QCoreApplication.translate("LogDialog", u"Ok", None))
        self.cancel_btn.setText(QCoreApplication.translate("LogDialog", u"Cancel", None))
        self.error_msg.setText(QCoreApplication.translate("LogDialog", u"Error", None))
    # retranslateUi

