"""
Handles The Main GUI Window 
"""

from sqlite3 import Cursor
import sys
from pathlib import Path
from uuid import uuid4
from PySide6.QtWidgets import (
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
    Qt,
    QSize,
    QObject
)
from PySide6.QtUiTools import QUiLoader
import gui.resources_rc
import database.categories_table
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
        self.log_widget = LogWidget()
        
        new_category_button = QAction(QIcon(":/icons/plus32.png"), "New Category", self)
        new_category_button.setStatusTip("Creates New Category")
        new_category_button.triggered.connect(self.new_cat_btn_clicked)

        delete_category_button = QAction(QIcon(":/icons/minus32.png"), "Delete Category", self)
        delete_category_button.setStatusTip("Deletes Selected Category")
        delete_category_button.triggered.connect(self.delete_cat_btn_clicked)

        start_button = QAction(QIcon(":/icons/play.png"), "Start", self)
        start_button.setStatusTip("Start Timer")
        start_button.triggered.connect(self.start_btn_clicked)

        pause_button = QAction(QIcon(":/icons/pause.png"), "Pause/Resume", self)
        pause_button.setStatusTip("Pause or Resume Timer")
        pause_button.triggered.connect(self.pause_btn_clicked)
        
        stop_button = QAction(QIcon(":/icons/stop.png"), "Stop", self)
        stop_button.setStatusTip("Stop Timer")
        stop_button.triggered.connect(self.stop_btn_clicked)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.toolBar.setMovable(False)
        self.toolBar.addAction(new_category_button)
        self.toolBar.addAction(delete_category_button)
        self.toolBar.addAction(start_button)
        self.toolBar.addAction(pause_button)
        self.toolBar.addAction(stop_button)
        
        self.actionQuit.triggered.connect(self.quit_menu_clicked)
        self.actionShow_Toolbar.triggered.connect(self.show_toolbar_menu_clicked)
        self.actionShow_Toolbar.setCheckable(True)
        self.actionShow_Toolbar.toggle()

        self.categoryTreeWidget.doubleClicked.connect(self.edit_widget_text)
        self.categoryTreeWidget.itemClicked.connect(self.update_log_view)
        self.categoryTreeWidget.itemChanged.connect(self.update_log_view)
        self.categoryTreeWidget.itemChanged.connect(self.update_cat_name_db)
        
        self.installEventFilter(self)

        self.groupBox.setStyleSheet(load_stylesheet(str(STYLES_DIR / "containers.qss")))
        self.categoryTreeWidget.setStyleSheet(load_stylesheet(str(STYLES_DIR / "item_widgets.qss")))
        self.init_category_tree()


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


    def new_cat_btn_clicked(self) -> None:
        self.categoryTreeWidget.blockSignals(True)

        child_item = QTreeWidgetItem(self.categoryTreeWidget)
        child_item.setText(0, "New Category")
        child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsEditable)
        child_item_text = child_item.text(0)

        category_id = str(uuid4())
        child_item.setData(0, Qt.ItemDataRole.UserRole, category_id)
        
        self.categoryTreeWidget.blockSignals(False)
        self.log_widget.init_category(category_id, child_item_text)   


    def pause_btn_clicked(self) -> None:
        self.timer_widget.pause_timer() 

    
    def start_btn_clicked(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if cur_item and cur_item.isSelected():
            self.timer_widget.start_timer()
            category_id = cur_item.data(0, Qt.ItemDataRole.UserRole)
            self.log_widget.set_category_id(category_id)
    

    def stop_btn_clicked(self) -> None:
        category_id = self.get_category_id()
        self.log_widget.add_log(self.logTreeWidget, self.timer_widget._elapsed_seconds, category_id)
        self.timer_widget.stop_timer()


    # MENU FUNCTIONS
    def quit_menu_clicked(self) -> None:
        sys.exit()


    def show_toolbar_menu_clicked(self) -> None:
        if self.actionShow_Toolbar.isChecked():
            self.toolBar.show()
        else:
            self.toolBar.hide()

    
    # MISCELLANEOUS FUNCTIONS
    def edit_widget_text(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        self.categoryTreeWidget.editItem(cur_item, 0)


    # deselect treewidgetitems through overloaded QObject method
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if (event.type() == QEvent.Type.MouseButtonPress):
            self.categoryTreeWidget.clearSelection()
            
        return super().eventFilter(obj, event)


    def get_category_id(self) -> str:
        cur_item = self.categoryTreeWidget.currentItem()
        category_id: str = cur_item.data(0, Qt.ItemDataRole.UserRole)
        return category_id


    def init_category_tree(self) -> None:
        header = self.categoryTreeWidget.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        header.setSectionResizeMode(1, header.ResizeMode.Fixed)
        self.categoryTreeWidget.setColumnWidth(1, 150)


    def update_cat_name_db(self) -> None:
        if self.categoryTreeWidget.currentItem() is None:
            return
        
        cur_item_text = self.categoryTreeWidget.currentItem().text(0)
        database.categories_table.update_category_name(db_conn, self.get_category_id(), cur_item_text)


    def update_log_view(self) -> None:
        cur_item = self.categoryTreeWidget.currentItem()
        if not cur_item:
            return

        category_id = self.get_category_id()
        self.log_widget.display_logs(self.categoryTreeWidget, self.logTreeWidget, category_id)


def display_window() -> None:
    main_window.show()
    app.exec()


def load_base_ui() -> None:
    ui_path = BASE_DIR / "src" / "gui" / "ui" / "main_window.ui"
    ui_window = ui_loader.load(str(ui_path), None)
    ui_window.show()
    app.exec()


def load_stylesheet(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Base Project Path
STYLES_DIR = Path(__file__).resolve().parent / "styles"  # Style Sheets Path

# main window instance
ui_loader = QUiLoader()
app = QApplication(sys.argv)
main_window = MainWindow()
