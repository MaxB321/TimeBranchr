"""
DIALOG WIDGET, ONLY APPEARS ON FIRST STARTUP
"""

import sys
from pathlib import Path
from uuid import uuid4
from PySide6.QtWidgets import QApplication, QDialog
from gui.generated import MainWindow
from gui.generated.GetUserID import Ui_UserDialog
import utils.config

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
        
        self.lineEdit.returnPressed.connect(self.set_user_data)


    def set_user_data(self) -> None:
        user_id = str(uuid4())
        user_name = self.lineEdit.text()
        utils.config.write_config(user_id, user_name)
        

    def user_quit(self) -> None:  # if user quits out of dialog window before entering user_name then shut down the main window as well 
        pass

