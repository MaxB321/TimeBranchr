from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel


class TimerWidget():
    def __init__(self, label: QLabel) -> None:
        super().__init__()
        self.label = label
        self._elapsed_seconds = 0
        self._timer = QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._update_timer)


    def pause_timer(self) -> None:
        if self._timer.isActive():
            self._timer.stop()
        else:
            self._timer.start()


    def start_timer(self) -> None:
        if not self._timer.isActive() and (self.label.text() == "00:00:00"):
            self._timer.start()


    def stop_timer(self) -> None:
        self._timer.stop()
        self._elapsed_seconds = 0
        self.label.setText("00:00:00")


    def _display_timer(self) -> str:
        seconds = self._elapsed_seconds
        minutes = 0
        hours = 0
        
        return f"{seconds}"
        #return f"{hours}:{minutes}:{seconds}"


    def _update_timer(self) -> None:
        self._elapsed_seconds += 1
        self.label.setText(self._display_timer())
