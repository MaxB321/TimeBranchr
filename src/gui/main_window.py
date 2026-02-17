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
        self.log_widget = LogWidget(self.logTreeWidget)
        self.log_menu = LogMenu(self.logTreeWidget, self.categoryTreeWidget, self.log_widget)
        self.cat_widget = CategoryWidget(self.categoryTreeWidget)
        self.toolbar = ToolbarWidget()
        self.addToolBar(self.toolbar)
        
        self.user_dialog = gui.dialogs.getUserID.UserDialog()
        self.change_name_dialog = gui.dialogs.change_name.changeNameDialog()
        self._user_id: str = ""
        self._user_name: str = ""
        self._user_categories: dict[str, str] = {}
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

        self.log_widget.log_added.connect(self.update_category_time)
        self.log_widget.log_del.connect(self.update_category_time)

        self.log_menu.sort_log_action.triggered.connect(self.sort_logs)
        self.log_menu.del_log_action.triggered.connect(self.del_log)
        self.log_menu.create_log_action.triggered.connect(self.create_log)
        
        self.installEventFilter(self)

        self.groupBox.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "containers.qss")))
        self.categoryTreeWidget.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "item_widgets.qss")))
        self.cat_widget.init_category_tree()
        self.init_log_tree()

        if not config.isConfig():
            self.show()
            self.user_dialog.exec()
            self._user_id = self.user_dialog._user_id
            self._user_name = self.user_dialog._user_name
        else:
            self._user_id = config.get_user_id()
            self._user_name = config.get_user_name()
            self._user_categories = database.categories_table.get_user_categories(db_conn, self._user_id)
            self.cat_widget.user_categories = self._user_categories
            self._user_logs = database.logs_table.get_user_logs(db_conn, self._user_id)
            self._user_logs_datetime = database.logs_table.get_user_logs_datetime(db_conn, self._user_id)
            self.load_categories()
            self.load_logs()


    # TOOLBAR FUNCTIONS
    def delete_cat_btn_clicked(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if cur_item and cur_item.isSelected():
            category_id = cur_item.data(0, Qt.ItemDataRole.UserRole)
            self.log_widget._user_logs.pop(category_id, None)
            parent = cur_item.parent()
            if parent:
                parent.removeChild(cur_item)
            else:
                self.categoryTreeWidget.takeTopLevelItem(self.categoryTreeWidget.indexOfTopLevelItem(cur_item))
            database.categories_table.delete_category_row(db_conn, category_id)


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
    

    def stop_btn_clicked(self) -> None:
        category_id = self.cat_widget.get_category_id()
        sort_new_first: bool = self.log_menu.sort_log_action.isChecked()
        self.log_widget.add_log(self.logTreeWidget, self.timer_widget._elapsed_seconds, category_id, self._user_id, sort_new_first)
        self.timer_widget.stop_timer()


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
        self.log_menu.create_log(category_id, self._user_id)
    
    
    def del_log(self) -> None:
        category_id = self.cat_widget.get_category_id()
        self.log_menu.delete_log(category_id, self.log_widget, db_conn, self._user_id)


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


    def load_categories(self) -> None:
        self.cat_widget.load_categories()


    def load_logs(self) -> None:
        self.log_widget.load_logs(self._user_logs, self._user_categories, self._user_logs_datetime)


    def update_category_time(self) -> None:
        self.cat_widget.update_category_time(self.log_widget)
        

    def update_log_view(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if not cur_item:
            return

        category_id = self.cat_widget.get_category_id()
        sort_new_first: bool = self.log_menu.sort_log_action.isChecked()
        self.log_widget.display_logs(self.categoryTreeWidget, category_id, sort_new_first)


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
