"""
DIALOG WIDGET, ONLY APPEARS ON FIRST STARTUP
"""

from PySide6.QtWidgets import QDialog
from generated.GetUserID import Ui_Dialog

class UserDialog(Ui_Dialog):
    def __init__(self):
        super().__init__()
        self._user_id: str = ""
        self._user_name: str = ""


    def get_user_id(self) -> str:
        return ""


    def isConfig(self) -> bool:  # checks if config is present on local drive
        return True

    
    def user_quit(self) -> None:  # if user quits out of dialog window then shut down the main window as well 
        pass
