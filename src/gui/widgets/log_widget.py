from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from gui.generated.MainWindow import Ui_MainWindow


class LogWidget():
    def __init__(self) -> None:
        super().__init__()


    def add_log(self, parent: QTreeWidget, seconds: int):  # add timer log after stop btn pressed
        s = seconds % 60
        minutes = (seconds % 3600) // 60
        hours = seconds // 3600
        log_str = f"{hours:02}:{minutes:02}:{s:02}"

        if not (seconds == 0):
            new_log = QTreeWidgetItem(parent)
            new_log.setText(0, log_str)


    def connect_log(self):  # connect log to category
        pass


    def create_log(self):  # user-created log 
        pass


    def delete_log(self):
        pass
