"""
Handles The Main GUI Window 
"""

from codecs import utf_8_encode
import sys
from pathlib import Path
from tokenize import String
from typing import overload
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
from gui.generated.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(300, 150, 1280, 720)
        self.setIconSize(QSize(25, 25))
        
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

        self.treeWidget.doubleClicked.connect(self.edit_widget_text)
        

        self.installEventFilter(self)

        self.groupBox.setStyleSheet(load_stylesheet(str(STYLES_DIR / "containers.qss")))
        self.treeWidget.setStyleSheet(load_stylesheet(str(STYLES_DIR / "item_widgets.qss")))


    # toolbar functions
    def new_cat_btn_clicked(self) -> None:
        child_item = QTreeWidgetItem(self.treeWidget)
        child_item.setText(0, "New Category")
        child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsEditable)


    def delete_cat_btn_clicked(self) -> None:
        cur_item = self.treeWidget.currentItem()
        if cur_item and cur_item.isSelected():
            parent = cur_item.parent()
            if parent:
                parent.removeChild(cur_item)
            else:
                self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(cur_item))

    
    def start_btn_clicked(self, s) -> None:
        print(s)
    

    def pause_btn_clicked(self, s) -> None:
        print(s)


    def stop_btn_clicked(self, s) -> None:
        print(s)
    

    # menu functions  
    def quit_menu_clicked(self) -> None:
        sys.exit()


    def show_toolbar_menu_clicked(self) -> None:
        if self.actionShow_Toolbar.isChecked():
            self.toolBar.show()
        else:
            self.toolBar.hide()
        
    
    def edit_widget_text(self) -> None:
        self.treeWidget.editItem(self.treeWidget.currentItem(), 0)

    
    # deselect treewidgetitems through overloaded QObject method
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if (event.type() == QEvent.Type.MouseButtonPress):
            self.treeWidget.clearSelection()
            
        return super().eventFilter(obj, event)


def display_window() -> None:
    main_window.show()
    app.exec()


def load_stylesheet(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_base_ui() -> None:
    ui_path = BASE_DIR / "src" / "gui" / "ui" / "main_window.ui"
    ui_window = ui_loader.load(str(ui_path), None)
    ui_window.show()
    app.exec()


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Base Project Path
STYLES_DIR = Path(__file__).resolve().parent / "styles"  # Style Sheets Path

# main window instance
ui_loader = QUiLoader()
app = QApplication(sys.argv)
main_window = MainWindow()
