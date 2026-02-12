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
        return True


    def open_context_menu(self, cur_pos: QPoint) -> None:
        global_pos = self.menu_parent.viewport().mapToGlobal(cur_pos)
        self.menu.exec(global_pos)
        

        if not self.is_item_selected():  # hide the del_log_action action
            pass
        else:  # grab selected item 
            pass


    def sort_logs(self) -> None:
        pass
