from PySide6.QtWidgets import QDialog
from gui.generated.CreateLog import Ui_LogDialog


class LogDialog(QDialog, Ui_LogDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.hours: int = 0
        self.minutes: int = 0
        self.seconds: int = 0


    def get_log_time(self) -> list[int]:
        return [self.hours, self.minutes, self.seconds]


    def set_log_time(self) -> None:
        pass
