from uuid import uuid4
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from gui.widgets.log_widget import LogWidget
from utils import config
import database.categories_table
from database.db_connect import db_conn
from utils.category_type import CategoryType


class CategoryWidget():
    def __init__(self, parent: QTreeWidget) -> None:
        super().__init__()
        self.user_id: str = config.get_user_id()
        self.user_categories: dict[str, str] = {}
        self.cat_tree = parent
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
        self.update_display()


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
        self.update_display()


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
        self.cat_tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)


    def is_category_selected(self) -> bool:
        cur_item = self.cat_tree.currentItem()
        if cur_item and cur_item.isSelected():
            return True
        
        return False
    

    def is_innermost_layer(self, selected_item: QTreeWidgetItem) -> bool:
        layer2_item = selected_item.parent()
        if layer2_item:
            layer1_item = layer2_item.parent()
            if layer1_item:
                return True
            else:
                return False

        return False
    

    def is_outermost_layer(self) -> bool:
        cur_item = self.cat_tree.currentItem()
        parent = cur_item.parent()
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
        pass


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


    def update_cat_name_db(self) -> None:
        if self.cat_tree.currentItem() is None:
            return

        cur_item_text = self.cat_tree.currentItem().text(0)
        database.categories_table.update_category_name(db_conn, self.get_category_id(), cur_item_text)
        self.update_display()


    def update_category_time(self, log_widget: LogWidget, cat_type: CategoryType) -> None:
        if log_widget.log_created or log_widget.log_deleted:
            category_id = self.get_category_id()
        else:
            category_id = log_widget._category_id

        child_item = self.cat_item_ref[category_id]

        category_time = database.categories_table.get_category_time(db_conn, category_id, cat_type)

        sec = category_time % 60
        min = (category_time % 3600) // 60
        hrs = category_time // 3600
        hrs_display: float = float(category_time / 3600) 
        min_display: float = float(category_time / 60)

        if hrs > 0:
            child_item.setText(1, f"{hrs_display:.1f} Hrs")
        elif hrs == 0 and min > 0:
            child_item.setText(1, f"{min_display:.1f} Min")
        else:
            child_item.setText(1, f"{sec} Sec")
        
        log_widget.log_created = False
        log_widget.log_deleted = False
    

    def update_display(self) -> None:
        if self.sort_ascending:
            self.cat_tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        else:
            self.cat_tree.sortByColumn(0, Qt.SortOrder.DescendingOrder)
