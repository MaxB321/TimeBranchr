import textwrap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from gui.generated.seeGuideDialog import Ui_seeGuideDialog
from utils import colors, stylesheets


class seeGuideDialog(QDialog, Ui_seeGuideDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Guide/About")
        self.setGeometry(500, 250, 350, 200)
        self.setFixedSize(350, 200)
        self.setPalette(colors.DARK_WINDOW)
        self.label.setGeometry(10, 5, 335, 110)

        self.label.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "see_guide_font.qss")))

        text: str = textwrap.dedent("""
        See the Guide and About section under 
        the Help Menu for details about how 
        the app works.
        """)

        self.label.setText(text.strip())
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
