import textwrap
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QDialog
from gui.generated.aboutDialog import Ui_aboutDialog
from utils import colors, stylesheets


class aboutDialog(QDialog, Ui_aboutDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("About")
        self.setGeometry(500, 250, 500, 350)
        self.setFixedSize(500, 350)
        self.setPalette(colors.DARK_WINDOW)
        self.textBrowser.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "text_dialogs.qss")))
        palette = self.textBrowser.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#2e2e2e"))
        self.textBrowser.setPalette(palette)

        text = textwrap.dedent("""
            Welcome to TimeBranchr!

            This app is a simple Time Tracker.

            Users can create new categories (studying, reading, exercise, etc.) to track time for.

            Each category can have a sub-category.
                - For example, studying can have a sub-category of computer science.

            Each sub-category can have its own sub-category.
                - For example, comp sci can have a sub of operating systems.

            Each level of this hierarchy has its own time count. For example:

                - Studying: 100 Hours
                    - Computer Science: 50 Hours
                        - Operating Systems: 30 Hours
                        - DSA: 20 Hours
                    - Math: 50 Hours
                        - Linear Algebra: 30 Hours
                        - Calculus I: 20 Hours

            The maximum number of hierarchy levels is 3 as shown above.

            See Guide section for more details.
        """)
        self.textBrowser.setText(text.strip())
