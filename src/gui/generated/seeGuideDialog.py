# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'see_guide_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QSizePolicy,
    QWidget)

class Ui_seeGuideDialog(object):
    def setupUi(self, seeGuideDialog):
        if not seeGuideDialog.objectName():
            seeGuideDialog.setObjectName(u"seeGuideDialog")
        seeGuideDialog.resize(300, 200)
        self.label = QLabel(seeGuideDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(110, 70, 49, 16))

        self.retranslateUi(seeGuideDialog)

        QMetaObject.connectSlotsByName(seeGuideDialog)
    # setupUi

    def retranslateUi(self, seeGuideDialog):
        seeGuideDialog.setWindowTitle(QCoreApplication.translate("seeGuideDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("seeGuideDialog", u"TextLabel", None))
    # retranslateUi

