# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_user_id.ui'
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
    QSizePolicy, QWidget)

class Ui_UserDialog(object):
    def setupUi(self, UserDialog):
        if not UserDialog.objectName():
            UserDialog.setObjectName(u"UserDialog")
        UserDialog.resize(908, 550)
        self.prompt = QLabel(UserDialog)
        self.prompt.setObjectName(u"prompt")
        self.prompt.setGeometry(QRect(210, 110, 432, 57))
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.prompt.setFont(font)
        self.prompt.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.lineEdit = QLineEdit(UserDialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(290, 200, 271, 21))
        self.errorLabel = QLabel(UserDialog)
        self.errorLabel.setObjectName(u"errorLabel")
        self.errorLabel.setGeometry(QRect(300, 280, 271, 21))

        self.retranslateUi(UserDialog)

        QMetaObject.connectSlotsByName(UserDialog)
    # setupUi

    def retranslateUi(self, UserDialog):
        UserDialog.setWindowTitle(QCoreApplication.translate("UserDialog", u"Dialog", None))
        self.prompt.setText(QCoreApplication.translate("UserDialog", u"<html><head/><body><p align=\"center\">Enter a Display Name</p></body></html>", None))
        self.errorLabel.setText(QCoreApplication.translate("UserDialog", u"TextLabel", None))
    # retranslateUi

