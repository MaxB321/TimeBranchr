from ast import List
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class LogWidget():
    def __init__(self) -> None:
        super().__init__()

        self._user_logs: dict[str, list[int]] = {}
        self._category_id: str = ""


    def add_log(self, parent: QTreeWidget, seconds: int) -> None:  # add timer log after stop btn pressed
        if seconds == 0:
            return
        
        self._user_logs[self._category_id].append(seconds)
        self.display_logs_nto(parent)


    def connect_log(self, category_tree: QTreeWidget, log_tree: QTreeWidget) -> None:  # connect log to category
        cur_item = category_tree.currentItem()
        if not cur_item:
            return

        cur_item_name = cur_item.text(0)
        header = log_tree.headerItem()
        header.setText(0, f"Logs - {cur_item_name}")

        self.display_logs_nto(log_tree)
        

    def create_log(self):  # user-created log 
        pass


    def delete_log(self):
        pass


    def display_logs_nto(self, parent: QTreeWidget):
        parent.clear()
        for val in reversed(self._user_logs[self._category_id]):
            s = val % 60
            m = (val % 3600) // 60
            h = val // 3600
            log_str = f"{h:02}:{m:02}:{s:02}" 
            new_log = QTreeWidgetItem(parent)
            new_log.setText(0, log_str)


    def init_category(self, category_id: str):
        self._user_logs[category_id] = []


    def set_category_id(self, category_id: str):
        self._category_id = category_id
    
