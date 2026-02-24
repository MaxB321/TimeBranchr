from datetime import datetime
from PySide6.QtCore import QDateTime, QEvent, QObject, Signal, Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from database.db_connect import db_conn
import database.categories_table
import database.logs_table
from utils.enums import CategoryType


class LogWidget(QObject):
    log_added = Signal(str)
    log_del = Signal(str)

    def __init__(self, log_tree: QTreeWidget) -> None:
        super().__init__()

        self._user_logs: dict[str, list[int]] = {}
        self._user_log_datetime: dict[str, list[datetime]] = {}
        self._category_id: str = ""
        self.log_tree = log_tree
        self.log_created: bool = False
        self.log_deleted: bool = False
        self.start_time: int =  0


    def add_log(self, log_tree: QTreeWidget, seconds: int, selected_category_id: str, user_id: str, sort_new_first: bool, cat_type: CategoryType) -> None:  
        if seconds == 0:
            return
        
        cur_date_time = datetime.now().replace(microsecond=0)
        self._user_logs[self._category_id].append(seconds)
        self._user_log_datetime[self._category_id].append(cur_date_time)
        
        database.logs_table.init_log(db_conn, self._category_id, seconds, user_id, cur_date_time, cat_type)

        if sort_new_first:
            self.display_logs_newest_first(log_tree, selected_category_id)
        else:
            self.display_logs_oldest_first(log_tree, selected_category_id)
        
        self.log_added.emit(self._category_id)


    def category_with_no_logs(self, user_logs: dict[str, list[int]], user_categories: dict[str, str], user_subcategories: dict[str, list[str]]) -> list[str]:
        category_ids = list[str](user_categories.keys())
        category_ids.extend(user_subcategories.keys())
        category_id_logs = list[str](user_logs.keys())
        categories_with_no_logs: list[str] = []
        
        for x in category_ids:
            if x not in category_id_logs:
                categories_with_no_logs.append(x)

        return categories_with_no_logs


    def create_log(self, log_tree: QTreeWidget, seconds: int, category_id: str, user_id: str, sort_new_first: bool, category_type: CategoryType):  # user-created log 
        if seconds == 0:
            return
        
        cur_date_time = datetime.now().replace(microsecond=0)
        self._user_logs[category_id].append(seconds)
        self._user_log_datetime[category_id].append(cur_date_time)
        database.logs_table.init_log(db_conn, category_id, seconds, user_id, cur_date_time, category_type)

        if sort_new_first:
            self.display_logs_newest_first(log_tree, category_id)
        else:
            self.display_logs_oldest_first(log_tree, category_id)
        
        self.log_created = True
        self.log_added.emit(category_id)


    def delete_log_item(self, category_id: str, parent: QTreeWidget, sort_new_first: bool) -> datetime:
        cur_item = self.log_tree.currentItem()
        item_datetime: datetime = self.get_datetime(cur_item)
        item_index = self._user_log_datetime[category_id].index(item_datetime)
        self._user_logs[category_id].pop(item_index)
        self._user_log_datetime[category_id].pop(item_index)
        
        if sort_new_first:
            self.display_logs_newest_first(parent, category_id)
        else:
            self.display_logs_oldest_first(parent, category_id)
        
        self.log_deleted = True
        
        return item_datetime 


    def display_logs(self, category_tree: QTreeWidget, category_id: str, sort_new_first: bool) -> None:  
        cur_item = category_tree.currentItem()
        if not cur_item:
            return

        cur_item_name = cur_item.text(0)
        header = self.log_tree.headerItem()
        header.setText(0, f"Logs - {cur_item_name}")

        if sort_new_first:
            self.display_logs_newest_first(self.log_tree, category_id)
        else:
            self.display_logs_oldest_first(self.log_tree, category_id)


    def display_logs_newest_first(self, parent: QTreeWidget, category_id: str) -> None:
        parent.clear()
        datetime_list: list[datetime] = []
        converted_datetime_list: list[str] = []

        for x in reversed(self._user_log_datetime[category_id]):
            datetime_list.append(x)
            converted_datetime_list.append(str(x))

        for i, val in enumerate(reversed(self._user_logs[category_id])): 
            s = val % 60
            m = (val % 3600) // 60
            h = val // 3600
            log_str = f"{h:02}:{m:02}:{s:02}" 
            datetime_str = str(converted_datetime_list[i])
            new_log = QTreeWidgetItem(parent)
            new_log.setText(0, log_str)
            new_log.setText(1, datetime_str)
            new_log.setData(1, Qt.ItemDataRole.UserRole, datetime_list[i])


    def display_logs_oldest_first(self, parent: QTreeWidget, category_id: str) -> None:
        parent.clear()
        datetime_list: list[datetime] = []
        converted_datetime_list: list[str] = []

        for x in self._user_log_datetime[category_id]:
            datetime_list.append(x)
            converted_datetime_list.append(str(x))

        for i, val in enumerate(self._user_logs[category_id]): 
            s = val % 60
            m = (val % 3600) // 60
            h = val // 3600
            log_str = f"{h:02}:{m:02}:{s:02}" 
            datetime_str = str(datetime_list[i])
            new_log = QTreeWidgetItem(parent)
            new_log.setText(0, log_str)
            new_log.setText(1, datetime_str)
            new_log.setData(1, Qt.ItemDataRole.UserRole, datetime_list[i])


    def get_datetime(self, cur_item: QTreeWidgetItem) -> datetime:
        item_datetime: datetime = cur_item.data(1, Qt.ItemDataRole.UserRole)
        return item_datetime


    def init_category(self, category_id: str, category_name: str, user_id: str) -> None:
        self._user_logs[category_id] = []
        self._user_log_datetime[category_id] = []
        database.categories_table.init_category(db_conn, category_id, category_name, 0, user_id)
    

    def init_subcategory(self, category_id: str, parent_id: str, category_name: str, user_id: str) -> None:
        self._user_logs[category_id] = []
        self._user_log_datetime[category_id] = []
        database.categories_table.init_subcategory(db_conn, category_id, parent_id, category_name, 0, user_id)

    
    def load_logs(self, user_logs: dict[str, list[int]], user_categories: dict[str, str], user_subcategories: dict[str, list[str]], user_logs_datetime: dict[str, list[datetime]]) -> None:
        categories_with_no_logs: list[str] = self.category_with_no_logs(user_logs, user_categories, user_subcategories)
        for key, val in user_logs.items():
            if key not in self._user_logs:
                self._user_logs[key] = []
            self._user_logs[key] = val
        for x in categories_with_no_logs:
            self._user_logs[x] = []
        
        for key, val in user_logs_datetime.items():
            if key not in self._user_logs:
                self._user_log_datetime[key] = []
            self._user_log_datetime[key] = val
        for x in categories_with_no_logs:
            self._user_log_datetime[x] = []


    def set_category_id(self, category_id: str) -> None:
        self._category_id = category_id
