import requests
from PySide6.QtGui import QAction, QContextMenuEvent, QIcon, Qt
from PySide6.QtWidgets import QToolBar, QTreeWidget, QTreeWidgetItem
from gui.widgets.category_widget import CategoryWidget
from gui.widgets.log_widget import LogWidget
from gui.widgets.timer_widget import TimerWidget
from utils.enums import CategoryType
from database.db_connect import SERVER_URL



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
                data = {
                "category_id": category_id,
                "category_type": CategoryType.MainCategory.value
                }
                requests.post(f"{SERVER_URL}/delete_category_row", json=data)
                cat_tree.takeTopLevelItem(cat_tree.indexOfTopLevelItem(cur_item))
            else:
                data = {
                "category_id": category_id,
                "category_type": CategoryType.SubCategory.value
                }
                response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
                old_time: int = response.json()["category_time"]
                parent_id: str = parent.data(0, Qt.ItemDataRole.UserRole)
                cat_widget.cleanup_children_items(cur_item)
                data = {
                "category_id": category_id,
                "category_type": CategoryType.SubCategory.value
                }
                requests.post(f"{SERVER_URL}/delete_category_row", json=data)
                parent.removeChild(cur_item)

                if parent.parent() is None:
                    data = {
                    "category_id": parent_id,
                    "category_type": CategoryType.MainCategory.value
                    }
                    response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
                    parent_time = response.json()["category_time"]
                    new_time = parent_time - old_time
                    data = {
                    "parent_id": parent_id,
                    "new_time": new_time
                    }
                    requests.post(f"{SERVER_URL}/update_parent_time", json=data)
                    cat_widget.update_category_time(log_widget, CategoryType.MainCategory, parent)
                else:
                    data = {
                    "category_id": parent_id,
                    "category_type": CategoryType.SubCategory.value
                    }
                    response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
                    parent_time = response.json()["category_time"]
                    new_time = parent_time - old_time
                    data = {
                    "parent_id": parent_id,
                    "new_time": new_time
                    }
                    requests.post(f"{SERVER_URL}/update_parent_time", json=data)
                    cat_widget.update_category_time(log_widget, CategoryType.SubCategory, parent)

                    outermost_item = parent.parent()
                    outermost_id = outermost_item.data(0, Qt.ItemDataRole.UserRole)
                    data = {
                    "category_id": outermost_id,
                    "category_type": CategoryType.MainCategory.value
                    }
                    response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
                    outermost_time = response.json()["category_time"]
                    new_time = outermost_time - old_time
                    data = {
                    "parent_id": outermost_id,
                    "new_time": new_time
                    }
                    requests.post(f"{SERVER_URL}/update_parent_time", json=data)
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
            data = {
            "category_id": log_widget._category_id,
            "category_type": CategoryType.SubCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
            start_time: int = response.json()["category_time"]
            log_widget.add_log(log_widget.log_tree, self.timer_widget._elapsed_seconds, selected_category_id, user_id, sort_flag, cat_type)
            self.timer_widget.stop_timer()
            data = {
            "category_id": log_widget._category_id,
            "category_type": CategoryType.SubCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
            end_time: int = response.json()["category_time"]
            time_diff: int = end_time - start_time
            parent_item = tracked_item.parent()
            parent_id = parent_item.data(0, Qt.ItemDataRole.UserRole)

            if cat_widget.is_outermost_layer(parent_item):
                data = {
                "category_id": parent_id,
                "category_type": CategoryType.MainCategory.value
                }
                response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
                parent_time = response.json()["category_time"]
                new_time = parent_time + time_diff    
                data = {
                "parent_id": parent_id,
                "new_time": new_time
                }
                requests.post(f"{SERVER_URL}/update_parent_time", json=data)
                cat_widget.update_category_time(log_widget, CategoryType.MainCategory, parent_item)
            else:
                data = {
                "category_id": parent_id,
                "category_type": CategoryType.SubCategory.value
                }
                response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
                parent_time: int = response.json()["category_time"]
                new_time: int = parent_time + time_diff
                data = {
                "parent_id": parent_id,
                "new_time": new_time
                }
                requests.post(f"{SERVER_URL}/update_parent_time", json=data)
                cat_widget.update_category_time(log_widget, CategoryType.SubCategory, parent_item)

                if cat_widget.is_innermost_layer(tracked_item):
                    outermost_item = parent_item.parent()
                    outermost_id = outermost_item.data(0, Qt.ItemDataRole.UserRole)
                    data = {
                    "category_id": outermost_id,
                    "category_type": CategoryType.MainCategory.value
                    }
                    response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
                    outermost_time: int = response.json()["category_time"]
                    new_time = outermost_time + time_diff
                    data = {
                    "parent_id": outermost_id,
                    "new_time": new_time
                    }
                    requests.post(f"{SERVER_URL}/update_parent_time", json=data)
                    cat_widget.update_category_time(log_widget, CategoryType.MainCategory, outermost_item)

