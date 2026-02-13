from datetime import datetime
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeWidget
import database.logs_table
from gui.dialogs.create_log import LogDialog
from gui.widgets.log_widget import LogWidget


class LogMenu(QMenu):
    def __init__(self, parent: QTreeWidget):
        super().__init__()
        self.menu = QMenu(parent)
        self.menu_parent: QTreeWidget = parent
        self.log_dialog = LogDialog()
        
        self.create_log_action = self.menu.addAction("Create Log")
        
        self.del_log_action = self.menu.addAction("Delete Log")

        self.sort_log_action = self.menu.addAction("Sort Logs Newest to Oldest")
        self.sort_log_action.setCheckable(True)
        self.sort_log_action.toggle()


    def create_log(self) -> None:
        # Open dialog widget
        # Lock the main_window functionality 
        # Get user input through lineedits and put it into a dict with keys ("hrs", "min", "sec") - stored in dialog widget object
        # Add log and update the runtime hashmaps in log_widget
        # Insert new log into DB
        # Update log view
        self.log_dialog.exec()
        


    def delete_log(self, category_id: str, log_widget: LogWidget, db_conn, user_id: str) -> None:
        sort_flag: bool = self.sort_log_action.isChecked()
        item_datetime = log_widget.delete_log_item(category_id, self.menu_parent, sort_flag)
        
        log_id: int = database.logs_table.get_log_id(db_conn, user_id, item_datetime)
        database.logs_table.user_del_log_row(db_conn, log_id)


    def deselect_log_item(self, parent: QTreeWidget) -> None:
        if not self.is_item_selected():
            return


    def is_item_selected(self) -> bool:
        cur_item = self.menu_parent.currentItem()
        if cur_item and cur_item.isSelected():
            return True
        return False


    def open_context_menu(self, cur_pos: QPoint) -> None:
        global_pos = self.menu_parent.viewport().mapToGlobal(cur_pos)

        if not self.is_item_selected():
            self.del_log_action.setVisible(False)
        else:  
            self.del_log_action.setVisible(True)

        self.menu.exec(global_pos)
