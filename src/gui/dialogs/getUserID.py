"""
DIALOG WIDGET, ONLY APPEARS ON FIRST STARTUP
"""

import sys
from pathlib import Path
from uuid import uuid4
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QCloseEvent, QKeyEvent
from PySide6.QtWidgets import QApplication, QDialog
from gui.generated import MainWindow
from gui.generated.GetUserID import Ui_UserDialog
import utils.config
from utils import stylesheets
import database.user_table
from database.db_connect import db_conn

class UserDialog(QDialog, Ui_UserDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._user_id: str = ""
        self._user_name: str = ""
        self.setGeometry(650, 275, 720, 300)
        self.setFixedSize(720, 300)
        self.prompt.setGeometry(100, 2, 500, 125)
        self.lineEdit.setGeometry(200, 100, 300, 25)
        self.errorLabel.setGeometry(290, 145, 300, 50)
        self.errorLabel.setText("Enter a Valid Name")
        self.errorLabel.setVisible(False)

        self.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "user_id_dialog.qss")))


    def closeEvent(self, event: QCloseEvent) -> None:
        if self._user_name == "":
            sys.exit()
        
        return super().closeEvent(event)


    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
            return
        elif event.key() == Qt.Key.Key_Return:
            event.ignore()
            self.set_user_data()
            return

        return super().keyPressEvent(event)


    def set_user_data(self) -> None:
        line_text: str = self.lineEdit.text()
        if line_text.isspace() or (line_text == ""):
            self.show_error_msg()
            return

        user_name = str(line_text)
        user_id = str(uuid4())
        
        self._user_id = user_id
        self._user_name = user_name
        utils.config.create_config(user_id, user_name)
        database.user_table.init_user(db_conn, user_id, user_name)
        self.close()
    

    def show_error_msg(self) -> None:
        self.errorLabel.setVisible(True)

