from ast import List
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class LogWidget():
    def __init__(self) -> None:
        super().__init__()

        self._user_logs: dict[str, list[int]] = {}

    def add_log(self, parent: QTreeWidget, seconds: int) -> None:  # add timer log after stop btn pressed
        s = seconds % 60
        minutes = (seconds % 3600) // 60
        hours = seconds // 3600
        log_str = f"{hours:02}:{minutes:02}:{s:02}"

        if not (seconds == 0):
            new_log = QTreeWidgetItem(parent)
            new_log.setText(0, log_str)


    def connect_log(self, category_tree: QTreeWidget, log_tree: QTreeWidget) -> None:  # connect log to category
        cur_item = category_tree.currentItem()
        if not cur_item:
            return
            
        cur_item_name = cur_item.text(0)
        header = log_tree.headerItem()
        header.setText(0, f"Logs - {cur_item_name}")
        

    def create_log(self):  # user-created log 
        pass


    def delete_log(self):
        pass


    def init_category(self, category_id: str):
        self._user_logs[category_id] = []
