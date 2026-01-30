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


    def connect_log(self, category_tree: QTreeWidget, log_tree: QTreeWidget):  # connect log to category
        cur_item = category_tree.currentItem()
        if cur_item:
            cur_item_name = cur_item.text(0)
            header = log_tree.headerItem()
            header.setText(0, f"Logs - {cur_item_name}")
        


    def create_log(self):  # user-created log 
        pass


    def delete_log(self):
        pass
