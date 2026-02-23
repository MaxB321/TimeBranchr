from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QTreeWidget

from gui.widgets.category_widget import CategoryWidget
from utils import config


class CategoryMenu(QMenu):
    def __init__(self, category_tree: QTreeWidget, category_widget: CategoryWidget) -> None:
        super().__init__()
        self.menu = QMenu(category_tree)
        self.category_tree: QTreeWidget = category_tree
        self.category_widget: CategoryWidget = category_widget
        self.category_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.category_tree.customContextMenuRequested.connect(self.open_context_menu)

        self.expand_items: QAction = self.menu.addAction("Expand All")
        self.collapse_items: QAction = self.menu.addAction("Collapse All")
        self.sort_items: QAction = self.menu.addAction("Sort Ascending")
        self.sort_items.setCheckable(True)

        self.expand_items.triggered.connect(self.expand_category_items)
        self.collapse_items.triggered.connect(self.collapse_category_items)
        self.sort_items.triggered.connect(self.sort_category_items)
    

    def collapse_category_items(self) -> None:
        self.category_tree.collapseAll()


    def expand_category_items(self) -> None:
        self.category_tree.expandAll()

    
    def sort_category_items(self) -> None:
        if self.sort_items.isChecked():
            self.category_widget.sort_ascending = True
            config.set_flag("categories_asc", True)
            self.category_widget.sort_display()
        else:
            self.category_widget.sort_ascending = False
            config.set_flag("categories_asc", False)
            self.category_widget.sort_display()


    def open_context_menu(self, cur_pos: QPoint) -> None:
        global_pos = self.category_tree.viewport().mapToGlobal(cur_pos)

        
        self.menu.exec(global_pos)
