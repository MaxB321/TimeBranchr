from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QMenu, QTreeWidget


class LogMenu(QMenu):
    def __init__(self, parent: QTreeWidget):
        super().__init__()
        self.menu = QMenu(parent)
        self.menu_parent: QTreeWidget = parent
        
        self.create_log_action = self.menu.addAction("Create Log")
        self.create_log_action.setCheckable(True)
        
        self.del_log_action = self.menu.addAction("Delete Log")
        self.del_log_action.setCheckable(True)

        self.sort_log_action = self.menu.addAction("Sort Logs Newest to Oldest")
        self.sort_log_action.setCheckable(True)


    def create_log_item(self) -> None:
        pass


    def delete_log_item(self) -> None:
        pass    


    def is_item_selected(self) -> bool:
        cur_item = self.menu_parent.currentItem()
        if cur_item and cur_item.isSelected():
            return True
        return False


    def open_context_menu(self, cur_pos: QPoint) -> None:
        global_pos = self.menu_parent.viewport().mapToGlobal(cur_pos)

        if not self.is_item_selected():
            self.create_log_action.setVisible(False)
        else:  
            self.create_log_action.setVisible(True)

        self.menu.exec(global_pos)


    def sort_logs(self) -> None:
        pass
