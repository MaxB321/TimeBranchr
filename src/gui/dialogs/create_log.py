from pathlib import Path
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QCloseEvent, QEnterEvent, QKeyEvent
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
        self.setFixedSize(450, 550)

        self.hours: int = 0
        self.minutes: int = 0
        self.seconds: int = 0

        self.setStyleSheet(load_stylesheet(str(STYLES_DIR / "log_dialog.qss")))
        

        self.buttonBox.accepted.connect(self.ok_btn_clicked)
        self.buttonBox.rejected.connect(self.cancel_btn_clicked)
        


    def cancel_btn_clicked(self) -> None:
        self.clear_lineedits()


    def clear_lineedits(self) -> None:
        self.lineEdit_h.clear()
        self.lineEdit_m.clear()
        self.lineEdit_s.clear()


    def closeEvent(self, event: QCloseEvent) -> None:
        self.clear_lineedits()
        self.deselect_lineedits()
        
        return super().closeEvent(event)


    def deselect_lineedits(self) -> None:
        self.setFocus()


    def get_log_time(self) -> list[int]:
        return [self.hours, self.minutes, self.seconds]


    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Enter:
            event.ignore()
            return
        
        elif event.key() == Qt.Key.Key_Escape:
            self.clear_lineedits()
            self.deselect_lineedits()

        return super().keyPressEvent(event)


    def ok_btn_clicked(self) -> None:
        self.set_log_time()
        print(f"{self.hours}, {self.minutes}, {self.seconds}")
        self.clear_lineedits()


    def set_log_time(self) -> None:
        self.hours = int(self.lineEdit_h.text())
        self.minutes = int(self.lineEdit_m.text())
        self.seconds = int(self.lineEdit_s.text())


def load_stylesheet(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


STYLES_DIR = Path(__file__).resolve().parent.parent / "styles"  # Style Sheets Path
