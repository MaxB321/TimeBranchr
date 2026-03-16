"""
Handles The Main GUI Window 
"""

import requests
from datetime import datetime
from sqlite3 import Cursor
import sys
from pathlib import Path
from typing import Optional
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
from database import export_csv
from gui.dialogs.about_dialog import aboutDialog
import gui.dialogs.getUserID
import gui.dialogs.change_name
from gui.dialogs.guide_dialog import guideDialog
import gui.resources_rc
from gui.widgets import log_widget
from gui.widgets.category_widget import CategoryWidget
from gui.widgets.toolbar_widget import ToolbarWidget
from utils import config
from utils import stylesheets
from utils.category_menu import CategoryMenu
from utils.enums import CategoryType, DisplayModeType
from utils.log_menu import LogMenu
from gui.generated.MainWindow import Ui_MainWindow
from gui.widgets.timer_widget import TimerWidget
from gui.widgets.log_widget import LogWidget
from database.db_connect import SERVER_URL


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(300, 150, 1280, 720)
        self.setIconSize(QSize(25, 25))

        self.timer_widget = TimerWidget(self.timerLabel, self.pauseLabel)
        self.cat_widget = CategoryWidget(self.categoryTreeWidget)
        self.log_widget = LogWidget(self.logTreeWidget)
        self.category_menu = CategoryMenu(self.categoryTreeWidget, self.cat_widget)
        self.log_menu = LogMenu(self.logTreeWidget, self.categoryTreeWidget, self.log_widget)
        self.toolbar = ToolbarWidget(self.timer_widget)
        self.addToolBar(self.toolbar)
        self.menu_widget = MenuWidget(self)
        
        self.user_dialog = gui.dialogs.getUserID.UserDialog()
        self.change_name_dialog = gui.dialogs.change_name.changeNameDialog()
        self._user_id: str = ""
        self._user_name: str = ""
        self._user_categories: dict[str, str] = {}
        self._user_subcategories: dict[str, list[str]] = {}  # index(0) == category_name ; index(1) == parent_id
        self._user_logs: dict[str, list[int]] = {}
        self._user_logs_datetime: dict[str, list[datetime]] = {}

        self.view_flags: dict[str, bool] = {}

        self.toolbar.new_category_button.triggered.connect(self.new_cat_btn_clicked)
        self.toolbar.delete_category_button.triggered.connect(self.delete_cat_btn_clicked)
        self.toolbar.start_button.triggered.connect(self.start_btn_clicked)
        self.toolbar.pause_button.triggered.connect(self.pause_btn_clicked)
        self.toolbar.stop_button.triggered.connect(self.stop_btn_clicked) 

        self.categoryTreeWidget.itemClicked.connect(self.update_log_view)
        self.categoryTreeWidget.itemChanged.connect(self.update_log_view)

        self.log_widget.log_added.connect(self.update_category_time_add)
        self.log_widget.log_del.connect(self.update_category_time_del)

        self.log_menu.sort_log_action.triggered.connect(self.sort_logs)
        self.log_menu.del_log_action.triggered.connect(self.del_log)
        self.log_menu.create_log_action.triggered.connect(self.create_log)
        self.log_menu.clear_view_action.triggered.connect(self.clear_log_view)
        
        self.installEventFilter(self)

        self.init_user_data()
        
        self.cat_widget.init_category_tree()
        self.init_log_tree()


    # TOOLBAR FUNCTIONS
    def delete_cat_btn_clicked(self) -> None:
        self.toolbar.delete_btn_clicked(self.categoryTreeWidget, self.cat_widget, self.log_widget)


    def new_cat_btn_clicked(self) -> None:
        self.cat_widget.add_category(self.log_widget)


    def pause_btn_clicked(self) -> None:
        self.timer_widget.pause_timer() 

    
    def start_btn_clicked(self) -> None:
        self.toolbar.start_btn_clicked(self.cat_widget, self.log_widget)


    def stop_btn_clicked(self) -> None:
        sort_new_first: bool = self.log_menu.sort_log_action.isChecked()
        self.toolbar.stop_btn_clicked(self._user_id, self.cat_widget, self.log_widget, sort_new_first)


    # LOG CONTEXT MENU FUNCTIONS
    def clear_log_view(self) -> None:
        self.log_widget.clear_log_view()
    
    
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
            self.log_menu.delete_log(category_id, self.log_widget, self._user_id, CategoryType.MainCategory)
        else:
            self.log_menu.delete_log(category_id, self.log_widget, self._user_id, CategoryType.SubCategory)


    def sort_logs(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if not cur_item:
            return

        category_id = self.cat_widget.get_category_id()
        if self.log_menu.sort_log_action.isChecked():
            self.log_widget.display_logs_newest_first(self.logTreeWidget, category_id)
            config.set_flag("logs_asc", True)
        else:
            self.log_widget.display_logs_oldest_first(self.logTreeWidget, category_id)
            config.set_flag("logs_asc", False)
    

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
            self.cat_widget.user_id = self.user_dialog._user_id
        else:
            self._user_id = config.get_user_id()
            self._user_name = config.get_user_name()

            data = {
            "user_id": self._user_id,
            }
            response = requests.get(f"{SERVER_URL}/get_user_categories", json=data)
            self._user_categories = response.json()["user_categories"]
            
            data = {
            "user_id": self._user_id,
            }
            response = requests.get(f"{SERVER_URL}/get_user_subcategories", json=data)
            self._user_subcategories = response.json()["user_subcategories"]

            self.cat_widget.user_categories = self._user_categories
            self.cat_widget.user_subcategories = self._user_subcategories

            data = {
            "user_id": self._user_id,
            "category_type": CategoryType.MainCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_user_logs", json=data)
            self._user_logs = response.json()["user_logs"]

            data = {
            "user_id": self._user_id,
            "category_type": CategoryType.SubCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_user_logs", json=data)
            self._user_logs |= response.json()["user_logs"]

            data = {
            "user_id": self._user_id,
            "category_type": CategoryType.MainCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_user_logs_datetime", json=data)
            self._user_logs_datetime = response.json()["logs_datetime"]

            data = {
            "user_id": self._user_id,
            "category_type": CategoryType.SubCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_user_logs_datetime", json=data)
            self._user_logs_datetime |= response.json()["logs_datetime"]

            self.cat_widget.user_id = config.get_user_id()
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
            data = {
            "category_id": parent_id,
            "category_type": CategoryType.MainCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
            parent_time = response.json()["category_time"]
        else:
            data = {
            "category_id": parent_id,
            "category_type": CategoryType.SubCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
            parent_time = response.json()["category_time"]

        end_time = sum(self.log_widget._user_logs[item_id])
        time_diff = end_time - start_time
        if not self.cat_widget.is_innermost_layer():
            new_time = parent_time + time_diff
            data = {
            "parent_id": parent_id,
            "new_time": new_time
            }
            requests.post(f"{SERVER_URL}/update_parent_time", json=data)
            self.cat_widget.update_category_time(self.log_widget, CategoryType.MainCategory, parent_item)
        else:
            new_time = parent_time + time_diff
            data = {
            "parent_id": parent_id,
            "new_time": new_time
            }
            requests.post(f"{SERVER_URL}/update_parent_time", json=data)
            self.cat_widget.update_category_time(self.log_widget, CategoryType.SubCategory, parent_item)

            outermost_item = parent_item.parent()
            outermost_id = outermost_item.data(0, Qt.ItemDataRole.UserRole)
            data = {
            "category_id": outermost_id,
            "category_type": CategoryType.MainCategory.value
            }
            response = requests.get(f"{SERVER_URL}/get_category_time", json=data)
            outermost_time = response.json()["category_time"]
            new_time = outermost_time + time_diff
            data = {
            "parent_id": outermost_id,
            "new_time": new_time
            }
            requests.post(f"{SERVER_URL}/update_parent_time", json=data)
            self.cat_widget.update_category_time(self.log_widget, CategoryType.MainCategory, outermost_item)
        
        self.log_widget.start_time = 0


class MenuWidget():
    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main_window = main_window
        self.init_appearance()
        self.about_dialog = aboutDialog()
        self.guide_dialog = guideDialog()


        # File
        self.main_window.actionQuit.triggered.connect(self.quit_menu_clicked)
        self.main_window.actionExport_CSV.triggered.connect(export_csv.export_csv)

        # View 
        self.main_window.actionDark_Mode_New.triggered.connect(self.dark_mode)
        self.main_window.actionDark_Mode_New.setCheckable(True)
        self.main_window.actionShow_Toolbar.triggered.connect(self.show_toolbar_menu_clicked)
        self.main_window.actionShow_Toolbar.setCheckable(True)
        self.main_window.actionShow_Subcategory_Totals.triggered.connect(self.show_subcat_totals)
        self.main_window.actionShow_Subcategory_Totals.setCheckable(True)
        self.main_window.actionShow_Username_in_Window_Title.triggered.connect(self.show_username)
        self.main_window.actionShow_Username_in_Window_Title.setCheckable(True)
        self.toggle_flags()

        # Settings
        self.main_window.actionDisplay_Name.triggered.connect(self.change_name_clicked)

        # Help
        self.main_window.actionGuide.triggered.connect(self.open_guide)
        self.main_window.actionAbout.triggered.connect(self.open_about)


    def change_name_clicked(self) -> None:
        self.main_window.change_name_dialog.init_dialog(self.main_window._user_id)
        self.main_window.change_name_dialog.exec()
        self.main_window._user_name = self.main_window.change_name_dialog.get_new_name()
        self.show_username()
    
    
    def dark_mode(self, display_mode: Optional[DisplayModeType] = None) -> None:
        if display_mode:
            if display_mode == DisplayModeType.DarkMode:
                self.set_stylesheets(display_mode)
                self.main_window.setPalette(DARK_WINDOW)
                self.set_timer_color(display_mode)
                return
            elif display_mode == DisplayModeType.LightMode:
                self.set_stylesheets(display_mode)
                self.main_window.setPalette(LIGHT_WINDOW)
                self.set_timer_color(display_mode)
                return

        flag = self.main_window.actionDark_Mode_New.isChecked()
        config.set_flag("dark_mode", flag)
        
        if flag:
            self.set_stylesheets(DisplayModeType.DarkMode)
            self.main_window.setPalette(DARK_WINDOW)
            self.set_timer_color(DisplayModeType.DarkMode)
        else:
            self.set_stylesheets(DisplayModeType.LightMode)
            self.main_window.setPalette(LIGHT_WINDOW)
            self.set_timer_color(DisplayModeType.LightMode)


    def init_appearance(self) -> None:
        if config.isConfig():
            if config.dark_mode:
                self.dark_mode(DisplayModeType.DarkMode)
            else:
                self.dark_mode(DisplayModeType.LightMode)

            if config.show_username:
                self.main_window.setWindowTitle(f"TimeBranchr - {config.get_user_name()}")
            else:
                self.main_window.setWindowTitle("TimeBranchr")
        else:
            self.dark_mode(DisplayModeType.DarkMode)
            self.main_window.setWindowTitle("TimeBranchr")


    def open_about(self) -> None:
        self.about_dialog.exec()


    def open_guide(self) -> None:
        self.guide_dialog.exec()


    def quit_menu_clicked(self) -> None:
        sys.exit()


    def set_stylesheets(self, display_mode: DisplayModeType) -> None:
        if display_mode == DisplayModeType.DarkMode:
            self.main_window.groupBox.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "darkMode_groupbox.qss")))
            self.main_window.categoryTreeWidget.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "tree_widgets.qss")))
            self.main_window.logTreeWidget.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "tree_widgets.qss")))

            palette = self.main_window.categoryTreeWidget.palette()
            palette.setColor(QPalette.ColorRole.Base, QColor("#2e2e2e"))
            self.main_window.categoryTreeWidget.setPalette(palette)
            self.main_window.logTreeWidget.setPalette(palette)
            
            header_palette = self.main_window.categoryTreeWidget.header().palette()
            header_palette.setColor(QPalette.ColorRole.Button, QColor("#383838"))
            header_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
            self.main_window.categoryTreeWidget.header().setPalette(header_palette)
            self.main_window.logTreeWidget.header().setPalette(header_palette)
        else:
            self.main_window.groupBox.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "lightMode_groupbox.qss")))
            self.main_window.categoryTreeWidget.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "tree_widgets.qss")))
            self.main_window.logTreeWidget.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "tree_widgets.qss")))
            
            palette = self.main_window.categoryTreeWidget.palette()
            palette.setColor(QPalette.ColorRole.Base, QColor("#757778"))
            self.main_window.categoryTreeWidget.setPalette(palette)
            self.main_window.logTreeWidget.setPalette(palette)

            header_palette = self.main_window.categoryTreeWidget.header().palette()
            header_palette.setColor(QPalette.ColorRole.Button, QColor("#484848"))
            header_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
            self.main_window.categoryTreeWidget.header().setPalette(header_palette)
            self.main_window.logTreeWidget.header().setPalette(header_palette)


    def set_timer_color(self, display_mode: DisplayModeType) -> None:
        if display_mode == DisplayModeType.DarkMode:
            text_color = self.main_window.timerLabel.palette()
            text_color.setColor(QPalette.ColorRole.WindowText, LIGHT_TEXT)
            self.main_window.timerLabel.setPalette(text_color)
        else:
            text_color = self.main_window.timerLabel.palette()
            text_color.setColor(QPalette.ColorRole.WindowText, DARK_TEXT)
            self.main_window.timerLabel.setPalette(text_color)


    def show_toolbar_menu_clicked(self) -> None:
        if self.main_window.actionShow_Toolbar.isChecked():
            self.main_window.toolbar.show()
        else:
            self.main_window.toolbar.hide()


    def show_username(self) -> None:
        flag = self.main_window.actionShow_Username_in_Window_Title.isChecked()
        config.set_flag("show_username", flag)
        if flag:
            self.main_window.setWindowTitle(f"TimeBranchr - {self.main_window._user_name}")
        else:
            self.main_window.setWindowTitle("TimeBranchr")


    def show_subcat_totals(self) -> None:
        flag = self.main_window.actionShow_Subcategory_Totals.isChecked()
        config.set_flag("show_subcat_totals", flag)
        if flag:
            self.main_window.cat_widget.show_subcat_total(self.main_window.log_widget)
        else:
            self.main_window.cat_widget.hide_subcat_total()


    def toggle_flags(self) -> None:
        if config.isConfig():
            if config.dark_mode:
                self.main_window.actionDark_Mode_New.toggle()
            if config.show_username:
                self.main_window.actionShow_Username_in_Window_Title.toggle()
            if config.categories_asc:
                self.main_window.category_menu.sort_items.toggle()
            if config.logs_asc:
                self.main_window.log_menu.sort_log_action.toggle()
            
            self.main_window.actionShow_Toolbar.toggle()
            self.main_window.actionShow_Subcategory_Totals.toggle()
        else:
            self.main_window.actionDark_Mode_New.toggle()
            self.main_window.actionShow_Subcategory_Totals.toggle()
            self.main_window.actionShow_Username_in_Window_Title.toggle()
            self.main_window.category_menu.sort_items.toggle()
            self.main_window.log_menu.sort_log_action.toggle()
            self.main_window.actionShow_Toolbar.toggle()


def display_main_window() -> None:
    main_window.show()
    app.exec()


def load_base_ui() -> None:
    ui_path = BASE_DIR / "src" / "gui" / "ui" / "main_window.ui"
    ui_window = ui_loader.load(str(ui_path), None)
    ui_window.show()
    app.exec()


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Base Project Path
DARK_WINDOW = QColor(30, 30, 30, 255)
LIGHT_WINDOW = QColor(237, 237, 240, 255)
DARK_TEXT = QColor(45, 45, 50, 255)
LIGHT_TEXT = QColor(255, 255, 255, 255)


# main window instance
ui_loader = QUiLoader()
app = QApplication(sys.argv)
main_window = MainWindow()
