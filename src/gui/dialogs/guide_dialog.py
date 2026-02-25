import textwrap
from PySide6.QtWidgets import QDialog
from gui.generated.guideDialog import Ui_guideDialog
from utils import stylesheets


class guideDialog(QDialog, Ui_guideDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Guide")
        self.setGeometry(500, 250, 550, 400)
        self.setFixedSize(550, 400)
        self.textBrowser.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "text_dialogs.qss")))
        
        text: str = textwrap.dedent("""
        How to make subcategory:
            1) Click on item to select it
            2) After item is selected, click new category button in the toolbar
            3) You can have up to 3 layers. See about section for example.
        
        The Parent category's time is the sum of the child item's time along with its own.
            - you can turn off the display for sub item's time in the view menu

        Deleting a category with sub items will delete both the selected category and all of its sub items.

        You can create a log by right clicking inside of the logs widget and selecting the option from the context menu.
        If a log item is selected you will have the option to delete the log in the context menu.

        "Export to CSV" under the file section will download all user related tables into separate csv files: 
            - Categories
            - SubCategories
            - Category Time Logs
            - Subcategory Time Logs
        These files will be stored in the downloads folder.
        """)
        
        
        self.textBrowser.setText(text.strip())
