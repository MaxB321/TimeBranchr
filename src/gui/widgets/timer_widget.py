from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel


class TimerWidget():
    def __init__(self, timerLabel: QLabel, pauseLabel: QLabel) -> None:
        super().__init__()
        self.timerLabel = timerLabel
        self.pauseLabel = pauseLabel
        self.pauseLabel.setVisible(False)
        self._elapsed_seconds = 0
        self._timer = QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._update_timer)


    def pause_timer(self) -> None:
        if self._timer.isActive():
            self._timer.stop()
            self.pauseLabel.setVisible(True)
        elif not self._timer.isActive() and not (self.timerLabel.text() == "00:00:00"):
            self._timer.start()
            self.pauseLabel.setVisible(False)


    def start_timer(self) -> None:
        if not self._timer.isActive() and (self.timerLabel.text() == "00:00:00"):
            self._timer.start()


    def stop_timer(self) -> None:
        self._timer.stop()
        self._elapsed_seconds = 0
        self.timerLabel.setText("00:00:00")
        self.pauseLabel.setVisible(False)


    def _display_timer(self, seconds) -> str:
        s = seconds % 60
        minutes = (seconds % 3600) // 60
        hours = seconds // 3600
        
        return f"{hours:02}:{minutes:02}:{s:02}"


    def _update_timer(self) -> None:
        self._elapsed_seconds += 1
        self.timerLabel.setText(self._display_timer(self._elapsed_seconds))
