# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'guide_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_guideDialog(object):
    def setupUi(self, guideDialog):
        if not guideDialog.objectName():
            guideDialog.setObjectName(u"guideDialog")
        guideDialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(guideDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser = QTextBrowser(guideDialog)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(guideDialog)

        QMetaObject.connectSlotsByName(guideDialog)
    # setupUi

    def retranslateUi(self, guideDialog):
        guideDialog.setWindowTitle(QCoreApplication.translate("guideDialog", u"Dialog", None))
    # retranslateUi

