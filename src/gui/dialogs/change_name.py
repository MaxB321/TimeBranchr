import requests
from PySide6.QtWidgets import QDialog, QFrame
from database.db_connect import SERVER_URL
from gui.generated.ChangeName import Ui_changeNameDialog
from utils import colors, config
from utils import stylesheets


class changeNameDialog(QDialog, Ui_changeNameDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(stylesheets.load_stylesheet(str(stylesheets.STYLES_DIR / "change_name.qss")))
        self.setGeometry(500, 275, 400, 450)
        self.setFixedSize(400, 450)
        self.setPalette(colors.DARK_WINDOW)
        self.oldNameLabel.setGeometry(25, 50, 150, 35)
        self.oldName.setGeometry(130, 51, 150, 35)
        self.newNameLabel.setGeometry(25, 125, 175, 35)
        self.newNameEdit.setGeometry(185, 129, 150, 30)
        self.errorLabel.setGeometry(125, 250, 150, 35)
        self._user_id = ""

        self.oldNameLabel.setText("Old Name:")
        self.newNameLabel.setText("Enter New Name:")
        self.errorLabel.setText("Enter a Valid Name")

        self.newNameEdit.returnPressed.connect(self.set_new_name)


    def get_new_name(self) -> str:
        return config.get_user_name()


    def init_dialog(self, user_id: str) -> None:
        self._user_id = user_id
        old_name: str = config.get_user_name()
        self.oldName.setText(old_name)
        self.errorLabel.setVisible(False)
        self.newNameEdit.clear()

    
    def set_new_name(self) -> None:
        new_name: str = self.newNameEdit.text()
        if new_name.isspace() or new_name == "":
            self.show_error_msg()
            return
        
        config.update_username(new_name)

        data = {
        "user_id": self._user_id,
        "user_name": new_name
        }
        requests.post(f"{SERVER_URL}/update_user_name", json=data)

        self.close()
        
    
    def show_error_msg(self):
        self.errorLabel.setVisible(True)

