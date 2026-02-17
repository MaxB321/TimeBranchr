from PySide6.QtGui import QAction, QContextMenuEvent, QIcon, Qt
from PySide6.QtWidgets import QToolBar



class ToolbarWidget(QToolBar):
    def __init__(self) -> None:
        super().__init__()
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

