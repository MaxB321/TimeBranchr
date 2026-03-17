import textwrap
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QDialog
from gui.generated.guideDialog import Ui_guideDialog
from utils import colors, stylesheets


class guideDialog(QDialog, Ui_guideDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Guide")
        self.setFixedSize(550, 400)
        self.setPalette(colors.DARK_WINDOW)
        self.textBrowser.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "text_dialogs.qss")))
        palette = self.textBrowser.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#2e2e2e"))
        self.textBrowser.setPalette(palette)
        
        text: str = textwrap.dedent("""
        How to make category:
            1) Make sure no other category is selected.
            2) Click the New Category Button in the toolbar.

        How to make subcategory:
            1) Click on item to select it.
            2) After item is selected, click new category button in the toolbar.
            3) You can have up to 3 layers. See the About section for an example.
        
        The Parent category's time is the sum of the child item's time along with its own.
            - You can turn off the display for the sub item's time in the view menu.

        Deleting a category with sub items will delete both the selected category and all of its sub items. Be Careful!

        Context Menus:
            - You can open a context menu by simply right clicking. There are context 
              menus for the following:
                - Categories Section
                - Logs Section

        Categories Context Menu Features:
            - Collapse All
            - Expand All
            - Sort Ascending/Descending

        Logs Context Menu Features:
            - Create Log (need to see Logs - "Category Name" for this to appear)
            - Delete Log (need to have log selected for this to appear)
            - Sort Logs Newest to Oldest / Oldest to Newest
            - Clear Log View

        "Export to CSV" under the File section will download all user related tables into a zip file inside your system's downloads folder.
        This zip file will contain the following CSV files.
            - Categories.csv
            - SubCategories.csv
            - Category_Time_Logs.csv
            - Subcategory_Time_Logs.csv
        """)
        
        
        self.textBrowser.setText(text.strip())
