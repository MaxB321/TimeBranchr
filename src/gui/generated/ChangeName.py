# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'change_name.ui'
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

class Ui_changeNameDialog(object):
    def setupUi(self, changeNameDialog):
        if not changeNameDialog.objectName():
            changeNameDialog.setObjectName(u"changeNameDialog")
        changeNameDialog.resize(527, 343)
        self.oldNameLabel = QLabel(changeNameDialog)
        self.oldNameLabel.setObjectName(u"oldNameLabel")
        self.oldNameLabel.setGeometry(QRect(110, 50, 81, 16))
        self.newNameLabel = QLabel(changeNameDialog)
        self.newNameLabel.setObjectName(u"newNameLabel")
        self.newNameLabel.setGeometry(QRect(110, 140, 81, 16))
        self.oldName = QLabel(changeNameDialog)
        self.oldName.setObjectName(u"oldName")
        self.oldName.setGeometry(QRect(220, 50, 49, 16))
        self.newNameEdit = QLineEdit(changeNameDialog)
        self.newNameEdit.setObjectName(u"newNameEdit")
        self.newNameEdit.setGeometry(QRect(200, 140, 113, 22))
        self.errorLabel = QLabel(changeNameDialog)
        self.errorLabel.setObjectName(u"errorLabel")
        self.errorLabel.setGeometry(QRect(180, 220, 49, 16))

        self.retranslateUi(changeNameDialog)

        QMetaObject.connectSlotsByName(changeNameDialog)
    # setupUi

    def retranslateUi(self, changeNameDialog):
        changeNameDialog.setWindowTitle(QCoreApplication.translate("changeNameDialog", u"Dialog", None))
        self.oldNameLabel.setText(QCoreApplication.translate("changeNameDialog", u"TextLabel", None))
        self.newNameLabel.setText(QCoreApplication.translate("changeNameDialog", u"TextLabel", None))
        self.oldName.setText(QCoreApplication.translate("changeNameDialog", u"TextLabel", None))
        self.errorLabel.setText(QCoreApplication.translate("changeNameDialog", u"TextLabel", None))
    # retranslateUi

