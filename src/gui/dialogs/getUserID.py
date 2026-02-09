"""
DIALOG WIDGET, ONLY APPEARS ON FIRST STARTUP
"""

import sys
from PySide6.QtWidgets import QApplication, QDialog
from gui.generated import MainWindow
from gui.generated.GetUserID import Ui_UserDialog

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
        

    def get_user_id(self) -> str:
        return ""
    

    def get_user_name(self) -> str:
        return ""


    def isConfig(self) -> bool:  # checks if config is present on local drive
        return True


    def write_config(self) -> None:
        pass

    
    def user_quit(self) -> None:  # if user quits out of dialog window before entering user_name then shut down the main window as well 
        pass


    def read_config(self) -> None:
        pass

