from PySide6.QtGui import QAction, QContextMenuEvent, QIcon, Qt
from PySide6.QtWidgets import QToolBar, QTreeWidget, QTreeWidgetItem

import database.categories_table
import database.categories_table
from gui.widgets.category_widget import CategoryWidget
from gui.widgets.log_widget import LogWidget
from gui.widgets.timer_widget import TimerWidget
from utils.enums import CategoryType
from database.db_connect import db_conn



class ToolbarWidget(QToolBar):
    def __init__(self, timer_widget: TimerWidget) -> None:
        super().__init__()

        self.timer_widget = timer_widget

        self.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.new_category_button = QAction(QIcon(":/icons/plus32.png"), "New Category", self)
        self.new_category_button.setStatusTip("Creates New Category")

        self.delete_category_button = QAction(QIcon(":/icons/minus32.png"), "Delete Category", self)
        self.delete_category_button.setStatusTip("Deletes Selected Category")

        self.start_button = QAction(QIcon(":/icons/play.png"), "Start", self)
        self.start_button.setStatusTip("Start Timer")

        self.pause_button = QAction(QIcon(":/icons/pause.png"), "Pause/Resume", self)
        self.pause_button.setStatusTip("Pause or Resume Timer")

        self.stop_button = QAction(QIcon(":/icons/stop.png"), "Stop", self)
        self.stop_button.setStatusTip("Stop Timer")

        self.addAction(self.new_category_button)
        self.addAction(self.delete_category_button)
        self.addAction(self.start_button)
        self.addAction(self.pause_button)
        self.addAction(self.stop_button)
    

    def delete_btn_clicked(self, cat_tree: QTreeWidget, cat_widget: CategoryWidget, log_widget: LogWidget) -> None:
        cur_item = cat_tree.currentItem()
        if cur_item and cur_item.isSelected():
            category_id = cur_item.data(0, Qt.ItemDataRole.UserRole)
            log_widget._user_logs.pop(category_id, None)
            parent = cur_item.parent()
            
            if cat_widget.is_outermost_layer():
                cat_widget.cleanup_children_items(cur_item)
                database.categories_table.delete_category_row(db_conn, category_id, CategoryType.MainCategory)
                cat_tree.takeTopLevelItem(cat_tree.indexOfTopLevelItem(cur_item))
            else:
                old_time: int = database.categories_table.get_category_time(db_conn, category_id, CategoryType.SubCategory)
                parent_id: str = parent.data(0, Qt.ItemDataRole.UserRole)
                cat_widget.cleanup_children_items(cur_item)
                database.categories_table.delete_category_row(db_conn, category_id, CategoryType.SubCategory)
                parent.removeChild(cur_item)

                if parent.parent() is None:
                    parent_time = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.MainCategory)
                    new_time = parent_time - old_time
                    database.categories_table.update_parent_time(db_conn, parent_id, new_time)
                    cat_widget.update_category_time(log_widget, CategoryType.MainCategory, parent)
                else:
                    parent_time = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.SubCategory)
                    new_time = parent_time - old_time
                    database.categories_table.update_parent_time(db_conn, parent_id, new_time)
                    cat_widget.update_category_time(log_widget, CategoryType.SubCategory, parent)

                    outermost_item = parent.parent()
                    outermost_id = outermost_item.data(0, Qt.ItemDataRole.UserRole)
                    outermost_time = database.categories_table.get_category_time(db_conn, outermost_id, CategoryType.MainCategory)
                    new_time = outermost_time - old_time
                    database.categories_table.update_parent_time(db_conn, outermost_id, new_time)
                    cat_widget.update_category_time(log_widget, CategoryType.MainCategory, outermost_item)
        
        if cat_tree.topLevelItemCount() == 0:
            log_widget.clear_log_view()
                

    
    def start_btn_clicked(self, cat_widget: CategoryWidget, log_widget: LogWidget) -> None:
        cur_item = cat_widget.cat_tree.currentItem()
        if cur_item and cur_item.isSelected():
            self.timer_widget.start_timer()
            category_id = cur_item.data(0, Qt.ItemDataRole.UserRole)
            log_widget.set_category_id(category_id)
            if not cur_item.parent():
                cat_widget.set_category_type(CategoryType.MainCategory)
            else:
                cat_widget.set_category_type(CategoryType.SubCategory)


    def stop_btn_clicked(self, user_id: str, cat_widget: CategoryWidget, log_widget: LogWidget, sort_flag: bool) -> None:
        selected_category_id = cat_widget.get_category_id()
        cat_type = cat_widget.get_category_type()
        
        tracked_id: str = log_widget._category_id
        tracked_item = cat_widget.cat_item_ref[tracked_id]
        if cat_widget.is_outermost_layer(tracked_item):
            log_widget.add_log(log_widget.log_tree, self.timer_widget._elapsed_seconds, selected_category_id,user_id, sort_flag, cat_type)
            self.timer_widget.stop_timer()
            return
        else:
            start_time: int = database.categories_table.get_category_time(db_conn, log_widget._category_id, CategoryType.SubCategory)
            log_widget.add_log(log_widget.log_tree, self.timer_widget._elapsed_seconds, selected_category_id, user_id, sort_flag, cat_type)
            self.timer_widget.stop_timer()
            end_time: int = database.categories_table.get_category_time(db_conn, log_widget._category_id, CategoryType.SubCategory)
            time_diff: int = end_time - start_time
            parent_item = tracked_item.parent()
            parent_id = parent_item.data(0, Qt.ItemDataRole.UserRole)

            if cat_widget.is_outermost_layer(parent_item):
                parent_time = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.MainCategory)
                new_time = parent_time + time_diff    
                database.categories_table.update_parent_time(db_conn, parent_id, new_time)
                cat_widget.update_category_time(log_widget, CategoryType.MainCategory, parent_item)
            else:
                parent_time: int = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.SubCategory)
                new_time: int = parent_time + time_diff
                database.categories_table.update_parent_time(db_conn, parent_id, new_time)
                cat_widget.update_category_time(log_widget, CategoryType.SubCategory, parent_item)

                if cat_widget.is_innermost_layer(tracked_item):
                    outermost_item = parent_item.parent()
                    outermost_id = outermost_item.data(0, Qt.ItemDataRole.UserRole)
                    outermost_time: int = database.categories_table.get_category_time(db_conn, outermost_id, CategoryType.MainCategory)
                    new_time = outermost_time + time_diff
                    database.categories_table.update_parent_time(db_conn, outermost_id, new_time)
                    cat_widget.update_category_time(log_widget, CategoryType.MainCategory, outermost_item)

