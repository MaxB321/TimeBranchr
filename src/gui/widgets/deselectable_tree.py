from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QTreeWidget

class DeselectableTreeWidget(QTreeWidget):

    def mousePressEvent(self, event: QMouseEvent) -> None:
        cur_pos = event.pos()
        if self.itemAt(cur_pos) is None:
            self.clearSelection()

        return super().mousePressEvent(event)
