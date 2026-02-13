from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QDialog
from gui.generated.CreateLog import Ui_LogDialog


class LogDialog(QDialog, Ui_LogDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setGeometry(700, 225, 450, 550)
        self.label_h.setGeometry(20, 20, 75, 50)
        self.label_m.setGeometry(20, 80, 75, 50)
        self.label_s.setGeometry(20, 140, 75, 50)
        self.lineEdit_h.setGeometry(110, 35, 100, 25)
        self.lineEdit_m.setGeometry(110, 95, 100, 25)
        self.lineEdit_s.setGeometry(110, 155, 100, 25)
        self.buttonBox.setGeometry(280, 470, 150, 100)

        self.hours: int = 0
        self.minutes: int = 0
        self.seconds: int = 0

        self.setStyleSheet(load_stylesheet(str(STYLES_DIR / "log_dialog.qss")))

        self.buttonBox.accepted.connect(self.ok_btn_clicked)
        self.buttonBox.rejected.connect(self.cancel_btn_clicked)


    def cancel_btn_clicked(self) -> None:
        print("cancel")


    def get_log_time(self) -> list[int]:
        return [self.hours, self.minutes, self.seconds]


    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
            return

        return super().keyPressEvent(event)


    def ok_btn_clicked(self) -> None:
        print("ok")


    def set_log_time(self) -> None:
        pass


def load_stylesheet(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


STYLES_DIR = Path(__file__).resolve().parent.parent / "styles"  # Style Sheets Path
