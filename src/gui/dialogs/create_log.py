from pathlib import Path
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QCloseEvent, QEnterEvent, QKeyEvent
from PySide6.QtWidgets import QDialog
from gui.generated.CreateLog import Ui_LogDialog


class LogDialog(QDialog, Ui_LogDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setGeometry(700, 225, 450, 500)
        self.label_h.setGeometry(20, 20, 75, 50)
        self.label_m.setGeometry(20, 80, 75, 50)
        self.label_s.setGeometry(20, 140, 80, 50)
        self.lineEdit_h.setGeometry(110, 35, 100, 25)
        self.lineEdit_m.setGeometry(110, 95, 100, 25)
        self.lineEdit_s.setGeometry(110, 155, 100, 25)
        self.ok_btn.setGeometry(310, 455, 60, 30)
        self.cancel_btn.setGeometry(375, 455, 60, 30)
        self.setFixedSize(450, 500)
        
        self.hours: int = 0
        self.minutes: int = 0
        self.seconds: int = 0
        self.converted_time_seconds: int = 0
        self.accept_flag: bool = False

        self.setStyleSheet(load_stylesheet(str(STYLES_DIR / "log_dialog.qss")))        
        
        self.ok_btn.clicked.connect(self.ok_btn_clicked)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)


    def cancel_btn_clicked(self) -> None:
        self.reject()


    def clear_lineedits(self) -> None:
        self.lineEdit_h.clear()
        self.lineEdit_m.clear()
        self.lineEdit_s.clear()


    def closeEvent(self, event: QCloseEvent) -> None:
        self.clear_lineedits()
        self.deselect_lineedits()
        
        return super().closeEvent(event)

    
    def convert_time_seconds(self, hours: int, minutes: int, seconds: int) -> int:
        converted_time: int = 0
        h_seconds: int = hours * 3600
        m_seconds: int = minutes * 60
        converted_time = h_seconds + m_seconds + seconds

        return converted_time


    def deselect_lineedits(self) -> None:
        self.setFocus()


    def get_log_time(self) -> list[int]:
        return [self.hours, self.minutes, self.seconds]


    def init_dialog(self) -> None:
        self.deselect_lineedits()
        self.clear_lineedits()
        self.ok_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.cancel_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        self.accept_flag = False
        self.error_msg.setGeometry(150, 220, 300, 50)
        self.error_msg.setText("Enter an integer value")
        self.error_msg.setVisible(False)


    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Enter:
            event.ignore()
            return

        return super().keyPressEvent(event)


    def ok_btn_clicked(self) -> None:
        self.set_log_time()
        if not self.accept_flag:
            return

        self.accept()


    def set_log_time(self) -> None:
        try:
            self.hours = int(self.lineEdit_h.text())
            self.minutes = int(self.lineEdit_m.text())
            self.seconds = int(self.lineEdit_s.text())
        except ValueError as e:
            self.show_error_msg(e)
            return

        self.converted_time_seconds = self.convert_time_seconds(self.hours, self.minutes, self.seconds)
        self.accept_flag = True
        
    
    def show_error_msg(self, e) -> None:
        self.error_msg.setVisible(True)


def load_stylesheet(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


STYLES_DIR = Path(__file__).resolve().parent.parent / "styles"  # Style Sheets Path
