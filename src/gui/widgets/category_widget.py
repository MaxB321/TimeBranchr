from typing import Optional
from uuid import uuid4
from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from gui.widgets.log_widget import LogWidget
from utils import config
import database.categories_table
from database.db_connect import db_conn
from utils.category_type import CategoryType


class CategoryWidget(QObject):
    def __init__(self, category_tree: QTreeWidget) -> None:
        super().__init__()
        self.user_id: str = ""
        self.user_categories: dict[str, str] = {}
        self.user_subcategories: dict[str, list[str]] = {}
        self.cat_tree = category_tree
        self.cat_item_ref: dict[str, QTreeWidgetItem] = {}
        self.sort_ascending: bool = True
        self._category_type = CategoryType.MainCategory

        self.cat_tree.doubleClicked.connect(self.edit_widget_text)
        self.cat_tree.itemChanged.connect(self.update_cat_name_db)


    def add_category(self, log_widget: LogWidget) -> None:
        if self.is_category_selected():
            self.add_subcategory(self.cat_tree.currentItem(), log_widget)
            return

        self.cat_tree.blockSignals(True)

        child_item = QTreeWidgetItem(self.cat_tree)
        child_item.setText(0, "New Category")
        child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsEditable)
        child_item_text = child_item.text(0)

        category_id = str(uuid4())
        child_item.setData(0, Qt.ItemDataRole.UserRole, category_id)
        self.cat_item_ref[category_id] = child_item

        child_item.setText(1, "0 Sec")
        
        self.cat_tree.blockSignals(False)
        log_widget.init_category(category_id, child_item_text, self.user_id)
        self.sort_display()


    def add_subcategory(self, selected_item: QTreeWidgetItem, log_widget: LogWidget) -> None:
        if self.is_innermost_layer(selected_item):
            return 
        
        self.cat_tree.blockSignals(True)

        child_item = QTreeWidgetItem()
        child_item.setText(0, "Child Item")
        child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsEditable)
        selected_item.addChild(child_item)
        child_item_text = child_item.text(0)

        category_id = str(uuid4())
        child_item.setData(0, Qt.ItemDataRole.UserRole, category_id)
        self.cat_item_ref[category_id] = child_item
        parent_id = selected_item.data(0, Qt.ItemDataRole.UserRole)

        child_item.setText(1, "0 Sec")

        self.cat_tree.blockSignals(False)
        log_widget.init_subcategory(category_id, parent_id, child_item_text, self.user_id)
        self.sort_display()
    

    def cleanup_children_items(self, cur_item: QTreeWidgetItem) -> None:
        child_count = cur_item.childCount()
        if child_count == 0:
            return 
        
        i: int = 0
        j: int = 0

        while i < child_count:
            cur_child = cur_item.child(0)
            j = 0

            innermost_child_count: int = cur_child.childCount()
            if not innermost_child_count == 0:
                while j < innermost_child_count:
                    innermost_child = cur_child.child(0)
                    category_id = innermost_child.data(0, Qt.ItemDataRole.UserRole)
                    cur_child.removeChild(innermost_child)
                    database.categories_table.delete_category_row(db_conn, category_id, CategoryType.SubCategory)
                    j += 1

            category_id = cur_child.data(0, Qt.ItemDataRole.UserRole)
            cur_item.removeChild(cur_child)
            database.categories_table.delete_category_row(db_conn, category_id, CategoryType.SubCategory)

            i += 1
        


    def display_total_time(self, item: QTreeWidgetItem, time: int) -> None:
        sec = time % 60
        min = (time % 3600) // 60
        hrs = time // 3600
        hrs_display: float = float(time / 3600) 
        min_display: float = float(time / 60)

        if hrs > 0:
            item.setText(1, f"{hrs_display:.1f} Hrs")
        elif hrs == 0 and min > 0:
            item.setText(1, f"{min_display:.1f} Min")
        else:
            item.setText(1, f"{sec} Sec")


    def edit_widget_text(self) -> None:
        cur_item = self.cat_tree.currentItem()
        self.cat_tree.editItem(cur_item, 0)


    def get_category_id(self) -> str:
        cur_item = self.cat_tree.currentItem()
        category_id: str = cur_item.data(0, Qt.ItemDataRole.UserRole)
        return category_id
    
    
    def get_category_type(self) -> CategoryType:
        return self._category_type


    def init_category_tree(self) -> None:
        header = self.cat_tree.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        header.setSectionResizeMode(1, header.ResizeMode.Custom)
        self.cat_tree.setColumnWidth(1, 125)
        if config.isConfig():
            if config.categories_asc:
                self.cat_tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)
            else:
                self.cat_tree.sortByColumn(0, Qt.SortOrder.DescendingOrder)
        else:
            self.cat_tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)


    def is_category_selected(self) -> bool:
        cur_item = self.cat_tree.currentItem()
        if cur_item and cur_item.isSelected():
            return True
        
        return False
    

    def is_innermost_layer(self, item: Optional[QTreeWidgetItem] = None) -> bool:
        if item is None:
            cur_item = self.cat_tree.currentItem()
            parent = cur_item.parent()
            if parent.parent():
                return True
            return False

        layer2_item = item.parent()
        if layer2_item:
            layer1_item = layer2_item.parent()
            if layer1_item:
                return True
            else:
                return False

        return False
    

    def is_outermost_layer(self, item: Optional[QTreeWidgetItem] = None) -> bool:
        if item is None:
            cur_item = self.cat_tree.currentItem()
            parent = cur_item.parent()
            if not parent:
                return True
            return False
        else:
            parent = item.parent()
            if not parent:
                return True

            return False
    

    def load_categories(self) -> None:
        self.cat_tree.blockSignals(True)

        for key, val in self.user_categories.items():

            child_item = QTreeWidgetItem(self.cat_tree)
            child_item.setText(0, val)
            child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsEditable)
            child_item.setData(0, Qt.ItemDataRole.UserRole, key)

            self.cat_item_ref[key] = child_item

            category_time = database.categories_table.get_category_time(db_conn, key, CategoryType.MainCategory)
            child_item.setText(1, self.load_category_time(category_time))

        self.cat_tree.blockSignals(False)
    

    def load_subcategories(self) -> None:
        innermost_items: dict[str, QTreeWidgetItem] = {} # key is parent_id

        self.cat_tree.blockSignals(True)
        for key, val in self.user_subcategories.items():
            
            child_item = QTreeWidgetItem()
            child_item.setText(0, val[0])
            child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsEditable)
            child_item.setData(0, Qt.ItemDataRole.UserRole, key)
            
            try:
                parent_item: QTreeWidgetItem = self.cat_item_ref[val[1]]
                parent_item.addChild(child_item)
            except KeyError:
                innermost_items[val[1]] = child_item
                continue

            self.cat_item_ref[key] = child_item

            category_time = database.categories_table.get_category_time(db_conn, key, CategoryType.SubCategory)
            child_item.setText(1, self.load_category_time(category_time))
        
        self.cat_tree.blockSignals(False)

        if not innermost_items:
            return

        self.cat_tree.blockSignals(True)
        for key, val in innermost_items.items():
            parent_item = self.cat_item_ref[key]
            parent_item.addChild(val)
            category_id: str = val.data(0, Qt.ItemDataRole.UserRole)
            self.cat_item_ref[category_id] = val
            category_time = database.categories_table.get_category_time(db_conn, category_id, CategoryType.SubCategory)
            val.setText(1, self.load_category_time(category_time))

        self.cat_tree.blockSignals(False)


    def load_category_time(self, category_time: int) -> str:
        sec = category_time % 60
        min = (category_time % 3600) // 60
        hrs = category_time // 3600
        hrs_display: float = float(category_time / 3600)
        min_display: float = float(category_time / 60)

        if hrs > 0:
            return f"{hrs_display:.1f} Hrs"
        elif hrs == 0 and min > 0:
            return f"{min_display:.1f} Min"
        else:
            return f"{sec} Sec"
    

    def set_category_type(self, cat_type: CategoryType) -> None:
        self._category_type = cat_type


    def sort_display(self) -> None:
        if self.sort_ascending:
            self.cat_tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        else:
            self.cat_tree.sortByColumn(0, Qt.SortOrder.DescendingOrder)


    def update_cat_name_db(self) -> None:
        if self.cat_tree.currentItem() is None:
            return

        cur_item_text = self.cat_tree.currentItem().text(0)
        if self.is_outermost_layer():
            database.categories_table.update_category_name(db_conn, self.get_category_id(), cur_item_text, CategoryType.MainCategory)
        else:
            database.categories_table.update_category_name(db_conn, self.get_category_id(), cur_item_text, CategoryType.SubCategory)
        self.sort_display()


    def update_category_time(self, log_widget: LogWidget, cat_type: CategoryType, item: Optional[QTreeWidgetItem] = None) -> None:
        if log_widget.log_created or log_widget.log_deleted:
            category_id = self.get_category_id()
        else:
            category_id = log_widget._category_id

        if item is None:        
            child_item = self.cat_item_ref[category_id]

            if self.is_outermost_layer(child_item):
                category_time = database.categories_table.get_category_time(db_conn, category_id, cat_type)
                self.display_total_time(child_item, category_time)
            else:
                category_time = database.categories_table.get_category_time(db_conn, category_id, cat_type)
                self.display_total_time(child_item, category_time)
                parent_item = child_item.parent()
                parent_id = parent_item.data(0, Qt.ItemDataRole.UserRole)

                if not self.is_innermost_layer(child_item):
                    category_time = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.MainCategory)
                    self.display_total_time(parent_item, category_time)
                else:
                    outermost_item = parent_item.parent()
                    outermost_id = outermost_item.data(0, Qt.ItemDataRole.UserRole)
                    category_time = database.categories_table.get_category_time(db_conn, outermost_id, CategoryType.MainCategory)
                    self.display_total_time(outermost_item, category_time)

        else:
            category_id = item.data(0, Qt.ItemDataRole.UserRole)
            category_time = database.categories_table.get_category_time(db_conn, category_id, cat_type)
            self.display_total_time(item, category_time)


        log_widget.log_created = False
        log_widget.log_deleted = False
    
