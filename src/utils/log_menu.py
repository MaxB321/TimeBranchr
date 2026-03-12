import requests
from datetime import datetime
from PySide6.QtCore import QObject, QPoint, Qt
from PySide6.QtWidgets import QMenu, QTreeWidget
import database.logs_table
from database.db_connect import SERVER_URL
from gui.dialogs.create_log import LogDialog
from gui.widgets.log_widget import LogWidget
from utils.enums import CategoryType


class LogMenu(QMenu):
    def __init__(self, log_tree: QTreeWidget, category_tree: QTreeWidget, log_widget: LogWidget):
        super().__init__()
        self.menu = QMenu(log_tree)
        self.log_tree: QTreeWidget = log_tree
        self.category_tree_widget = category_tree
        self.log_dialog = LogDialog()
        self.log_widget = log_widget
        self.log_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.log_tree.customContextMenuRequested.connect(self.open_context_menu)
        
        self.create_log_action = self.menu.addAction("Create Log")
        self.del_log_action = self.menu.addAction("Delete Log")
        self.sort_log_action = self.menu.addAction("Sort Logs Newest to Oldest")
        self.sort_log_action.setCheckable(True)
        self.clear_view_action = self.menu.addAction("Clear Log View")


    def create_log(self, category_id: str, user_id: str, category_type: CategoryType) -> None:
        self.log_dialog.init_dialog()
        self.log_dialog.exec()

        if self.log_dialog.accept_flag:
            seconds: int = self.log_dialog.converted_time_seconds
            sort_flag: bool = self.sort_log_action.isChecked()
            self.log_widget.create_log(self.log_tree, seconds, category_id, user_id, sort_flag, category_type)


    def delete_log(self, category_id: str, log_widget: LogWidget, user_id: str, category_type: CategoryType) -> None:
        sort_flag: bool = self.sort_log_action.isChecked()
        item_datetime = log_widget.delete_log_item(category_id, self.log_tree, sort_flag)
        
        data = {
        "user_id": user_id,
        "date_time": item_datetime.isoformat(),
        "category_type": category_type.value
        }
        response = requests.get(f"{SERVER_URL}/get_log_id", json=data)
        log_id: int = response.json()["log_id"]

        data = {
        "log_id": log_id,
        "category_type": category_type.value
        }
        requests.post(f"{SERVER_URL}/user_del_log_row", json=data)

        
        self.log_widget.log_del.emit(category_id)


    def is_item_selected(self) -> bool:
        cur_item = self.log_tree.currentItem()
        if cur_item and cur_item.isSelected():
            return True
        return False


    def open_context_menu(self, cur_pos: QPoint) -> None:
        global_pos = self.log_tree.viewport().mapToGlobal(cur_pos)

        if not self.is_item_selected():
            self.del_log_action.setVisible(False)
        else:  
            self.del_log_action.setVisible(True)
        
        if not self.log_widget.is_log_displayed():
            self.create_log_action.setVisible(False)
        else:
            self.create_log_action.setVisible(True)

        self.menu.exec(global_pos)
