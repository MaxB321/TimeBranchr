"""
Handles The Main GUI Window 
"""

from datetime import datetime
from sqlite3 import Cursor
import sys
from pathlib import Path
from uuid import uuid4
from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QWidget,
    QApplication,
    QToolBar,
    QStatusBar,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QMenuBar,
    QMenu,
    QWidgetAction,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QStackedLayout
)
from PySide6.QtGui import (
    QContextMenuEvent,
    QGuiApplication,
    QMouseEvent,
    QWindow,
    QScreen,
    QAction,
    QKeySequence,
    QIcon,
    QColor,
    QPalette
)
from PySide6.QtCore import (
    QEvent,
    QPoint,
    Qt,
    QSize,
    QObject
)
from PySide6.QtUiTools import QUiLoader
import gui.dialogs.getUserID
import gui.dialogs.change_name
import gui.resources_rc
import database.categories_table
import database.logs_table
from gui.widgets import log_widget
from gui.widgets.category_widget import CategoryWidget
from gui.widgets.toolbar_widget import ToolbarWidget
from utils import config
from utils import stylesheets
from utils.category_menu import CategoryMenu
from utils.category_type import CategoryType
from utils.log_menu import LogMenu
from gui.generated.MainWindow import Ui_MainWindow
from gui.widgets.timer_widget import TimerWidget
from gui.widgets.log_widget import LogWidget
from database.db_connect import db_conn


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(300, 150, 1280, 720)
        self.setIconSize(QSize(25, 25))
        self.timer_widget = TimerWidget(self.label)
        self.cat_widget = CategoryWidget(self.categoryTreeWidget)
        self.log_widget = LogWidget(self.logTreeWidget)
        self.category_menu = CategoryMenu(self.categoryTreeWidget, self.cat_widget)
        self.log_menu = LogMenu(self.logTreeWidget, self.categoryTreeWidget, self.log_widget)
        self.toolbar = ToolbarWidget()
        self.addToolBar(self.toolbar)
        
        self.user_dialog = gui.dialogs.getUserID.UserDialog()
        self.change_name_dialog = gui.dialogs.change_name.changeNameDialog()
        self._user_id: str = ""
        self._user_name: str = ""
        self._user_categories: dict[str, str] = {}
        self._user_subcategories: dict[str, list[str]] = {}  # index(0) == category_name ; index(1) == parent_id
        self._user_logs: dict[str, list[int]] = {}
        self._user_logs_datetime: dict[str, list[datetime]] = {}

        self.toolbar.new_category_button.triggered.connect(self.new_cat_btn_clicked)
        self.toolbar.delete_category_button.triggered.connect(self.delete_cat_btn_clicked)
        self.toolbar.start_button.triggered.connect(self.start_btn_clicked)
        self.toolbar.pause_button.triggered.connect(self.pause_btn_clicked)
        self.toolbar.stop_button.triggered.connect(self.stop_btn_clicked)

        self.actionQuit.triggered.connect(self.quit_menu_clicked)
        self.actionShow_Toolbar.triggered.connect(self.show_toolbar_menu_clicked)
        self.actionShow_Toolbar.setCheckable(True)
        self.actionShow_Toolbar.toggle()
        self.actionDisplay_Name.triggered.connect(self.change_name_clicked)

        self.categoryTreeWidget.itemClicked.connect(self.update_log_view)
        self.categoryTreeWidget.itemChanged.connect(self.update_log_view)

        self.log_widget.log_added.connect(self.update_category_time_add)
        self.log_widget.log_del.connect(self.update_category_time_del)

        self.log_menu.sort_log_action.triggered.connect(self.sort_logs)
        self.log_menu.del_log_action.triggered.connect(self.del_log)
        self.log_menu.create_log_action.triggered.connect(self.create_log)
        
        self.installEventFilter(self)

        self.groupBox.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "containers.qss")))
        self.categoryTreeWidget.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "item_widgets.qss")))

        self.init_user_data()
        
        self.cat_widget.init_category_tree()
        self.init_log_tree()


    # TOOLBAR FUNCTIONS
    def delete_cat_btn_clicked(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if cur_item and cur_item.isSelected():
            category_id = cur_item.data(0, Qt.ItemDataRole.UserRole)
            self.log_widget._user_logs.pop(category_id, None)
            parent = cur_item.parent()
            
            if self.cat_widget.is_outermost_layer():
                self.cat_widget.cleanup_children_items(cur_item)
                database.categories_table.delete_category_row(db_conn, category_id, CategoryType.MainCategory)
                self.categoryTreeWidget.takeTopLevelItem(self.categoryTreeWidget.indexOfTopLevelItem(cur_item))
            else:
                self.cat_widget.cleanup_children_items(cur_item)
                database.categories_table.delete_category_row(db_conn, category_id, CategoryType.SubCategory)
                parent.removeChild(cur_item)


    def new_cat_btn_clicked(self) -> None:
        self.cat_widget.add_category(self.log_widget)


    def pause_btn_clicked(self) -> None:
        self.timer_widget.pause_timer() 

    
    def start_btn_clicked(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if cur_item and cur_item.isSelected():
            self.timer_widget.start_timer()
            category_id = cur_item.data(0, Qt.ItemDataRole.UserRole)
            self.log_widget.set_category_id(category_id)
            if not cur_item.parent():
                self.cat_widget.set_category_type(CategoryType.MainCategory)
            else:
                self.cat_widget.set_category_type(CategoryType.SubCategory)


    def stop_btn_clicked(self) -> None:
        selected_category_id = self.cat_widget.get_category_id()
        sort_new_first: bool = self.log_menu.sort_log_action.isChecked()
        cat_type = self.cat_widget.get_category_type()
        
        tracked_id: str = self.log_widget._category_id
        tracked_item = self.cat_widget.cat_item_ref[tracked_id]
        if self.cat_widget.is_outermost_layer(tracked_item):
            self.log_widget.add_log(self.logTreeWidget, self.timer_widget._elapsed_seconds, selected_category_id, self._user_id, sort_new_first, cat_type)
            self.timer_widget.stop_timer()
            return
        else:
            start_time: int = database.categories_table.get_category_time(db_conn, self.log_widget._category_id, CategoryType.SubCategory)
            self.log_widget.add_log(self.logTreeWidget, self.timer_widget._elapsed_seconds, selected_category_id, self._user_id, sort_new_first, cat_type)
            self.timer_widget.stop_timer()
            end_time: int = database.categories_table.get_category_time(db_conn, self.log_widget._category_id, CategoryType.SubCategory)
            time_diff: int = end_time - start_time
            parent_item = tracked_item.parent()
            parent_id = parent_item.data(0, Qt.ItemDataRole.UserRole)

            if self.cat_widget.is_outermost_layer(parent_item):
                parent_time = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.MainCategory)
                new_time = parent_time + time_diff    
                database.categories_table.update_parent_time(db_conn, tracked_id, parent_id, new_time)
                self.cat_widget.update_category_time(self.log_widget, CategoryType.MainCategory, parent_item)
            else:
                parent_time: int = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.SubCategory)
                new_time: int = parent_time + time_diff
                database.categories_table.update_parent_time(db_conn, tracked_id, parent_id, new_time)
                self.cat_widget.update_category_time(self.log_widget, CategoryType.SubCategory, parent_item)

                if self.cat_widget.is_innermost_layer(tracked_item):
                    outermost_item = parent_item.parent()
                    outermost_id = outermost_item.data(0, Qt.ItemDataRole.UserRole)
                    outermost_time: int = database.categories_table.get_category_time(db_conn, outermost_id, CategoryType.MainCategory)
                    new_time = outermost_time + time_diff
                    database.categories_table.update_parent_time(db_conn, parent_id, outermost_id, new_time)
                    self.cat_widget.update_category_time(self.log_widget, CategoryType.MainCategory, outermost_item)


    # TOP MENU FUNCTIONS
    def change_name_clicked(self) -> None:
        self.change_name_dialog.init_dialog(self._user_id)
        self.change_name_dialog.exec()
        self._user_name = self.change_name_dialog.get_new_name()
    
    
    def quit_menu_clicked(self) -> None:
        sys.exit()


    def show_toolbar_menu_clicked(self) -> None:
        if self.actionShow_Toolbar.isChecked():
            self.toolbar.show()
        else:
            self.toolbar.hide()


    # LOG CONTEXT MENU FUNCTIONS
    def create_log(self) -> None:
        category_id = self.cat_widget.get_category_id()
        self.log_widget.start_time = sum(self.log_widget._user_logs[category_id])
        if self.cat_widget.is_outermost_layer():
            self.log_menu.create_log(category_id, self._user_id, CategoryType.MainCategory)
        else:
            self.log_menu.create_log(category_id, self._user_id, CategoryType.SubCategory)
    
    
    def del_log(self) -> None:
        category_id = self.cat_widget.get_category_id()
        self.log_widget.start_time = sum(self.log_widget._user_logs[category_id])
        if self.cat_widget.is_outermost_layer():
            self.log_menu.delete_log(category_id, self.log_widget, db_conn, self._user_id, CategoryType.MainCategory)
        else:
            self.log_menu.delete_log(category_id, self.log_widget, db_conn, self._user_id, CategoryType.SubCategory)


    def sort_logs(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if not cur_item:
            return

        category_id = self.cat_widget.get_category_id()
        if self.log_menu.sort_log_action.isChecked():
            self.log_widget.display_logs_newest_first(self.logTreeWidget, category_id)
        else:
            self.log_widget.display_logs_oldest_first(self.logTreeWidget, category_id)
    

    # MISCELLANEOUS FUNCTIONS
    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        event.ignore()
        return

    
    # deselect treewidgetitems through overloaded QObject method
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if (event.type() == QEvent.Type.MouseButtonPress):
             self.categoryTreeWidget.clearSelection()
             self.logTreeWidget.clearSelection()

        return super().eventFilter(obj, event)


    def init_log_tree(self) -> None:
        header = self.logTreeWidget.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        header.setSectionResizeMode(1, header.ResizeMode.Custom)
        self.logTreeWidget.setColumnWidth(1, 125)


    def init_user_data(self) -> None:
        if not config.isConfig():
            self.show()
            self.user_dialog.exec()
            self._user_id = self.user_dialog._user_id
            self._user_name = self.user_dialog._user_name
        else:
            self._user_id = config.get_user_id()
            self._user_name = config.get_user_name()
            self._user_categories = database.categories_table.get_user_categories(db_conn, self._user_id)
            self._user_subcategories = database.categories_table.get_user_subcategories(db_conn, self._user_id)
            self.cat_widget.user_categories = self._user_categories
            self.cat_widget.user_subcategories = self._user_subcategories
            self._user_logs = database.logs_table.get_user_logs(db_conn, self._user_id, CategoryType.MainCategory)
            self._user_logs |= database.logs_table.get_user_logs(db_conn, self._user_id, CategoryType.SubCategory)
            self._user_logs_datetime = database.logs_table.get_user_logs_datetime(db_conn, self._user_id, CategoryType.MainCategory)
            self._user_logs_datetime |= database.logs_table.get_user_logs_datetime(db_conn, self._user_id, CategoryType.SubCategory)
            self.cat_widget.load_categories()
            self.cat_widget.load_subcategories()
            self.load_logs()


    def load_logs(self) -> None:
        self.log_widget.load_logs(self._user_logs, self._user_categories, self._user_subcategories, self._user_logs_datetime)


    def update_category_time_add(self) -> None:
        if not self.log_widget.log_created:
            category_type = self.cat_widget.get_category_type()
            self.cat_widget.update_category_time(self.log_widget, category_type)
        else:
            if self.cat_widget.is_outermost_layer():
                self.cat_widget.update_category_time(self.log_widget, CategoryType.MainCategory)
            else:
                self.cat_widget.update_category_time(self.log_widget, CategoryType.SubCategory)
                self.update_parent_time(self.log_widget.start_time)


    def update_category_time_del(self) -> None:
        if self.cat_widget.is_outermost_layer():
            self.cat_widget.update_category_time(self.log_widget, CategoryType.MainCategory)
        else:
            self.cat_widget.update_category_time(self.log_widget, CategoryType.SubCategory)
            self.update_parent_time(self.log_widget.start_time)


    def update_log_view(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if not cur_item:
            return

        category_id = self.cat_widget.get_category_id()
        sort_new_first: bool = self.log_menu.sort_log_action.isChecked()
        self.log_widget.display_logs(self.categoryTreeWidget, category_id, sort_new_first)
    

    def update_parent_time(self, start_time: int) -> None:
        item_id = self.cat_widget.get_category_id()
        item: QTreeWidgetItem = self.cat_widget.cat_item_ref[item_id]
        parent_item = item.parent()
        parent_id = parent_item.data(0, Qt.ItemDataRole.UserRole)
        if self.cat_widget.is_outermost_layer(parent_item):
            parent_time = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.MainCategory)
        else:
            parent_time = database.categories_table.get_category_time(db_conn, parent_id, CategoryType.SubCategory)

        end_time = sum(self.log_widget._user_logs[item_id])
        time_diff = end_time - start_time
        if not self.cat_widget.is_innermost_layer():
            new_time = parent_time + time_diff
            database.categories_table.update_parent_time(db_conn, item_id, parent_id, new_time)
            self.cat_widget.update_category_time(self.log_widget, CategoryType.MainCategory, parent_item)
        else:
            new_time = parent_time + time_diff
            database.categories_table.update_parent_time(db_conn, item_id, parent_id, new_time)
            self.cat_widget.update_category_time(self.log_widget, CategoryType.SubCategory, parent_item)

            outermost_item = parent_item.parent()
            outermost_id = outermost_item.data(0, Qt.ItemDataRole.UserRole)
            outermost_time = parent_time = database.categories_table.get_category_time(db_conn, outermost_id, CategoryType.MainCategory)
            new_time = outermost_time + time_diff
            database.categories_table.update_parent_time(db_conn, item_id, outermost_id, new_time)
            self.cat_widget.update_category_time(self.log_widget, CategoryType.MainCategory, outermost_item)
        
        self.log_widget.start_time = 0


def display_main_window() -> None:
    main_window.show()
    app.exec()


def load_base_ui() -> None:
    ui_path = BASE_DIR / "src" / "gui" / "ui" / "main_window.ui"
    ui_window = ui_loader.load(str(ui_path), None)
    ui_window.show()
    app.exec()


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Base Project Path

# main window instance
ui_loader = QUiLoader()
app = QApplication(sys.argv)
main_window = MainWindow()
