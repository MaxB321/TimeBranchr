import requests
from pathlib import Path
import pandas as pd
from database.db_connect import db_conn, engine
from utils import config
from database.db_connect import SERVER_URL


def export_csv() -> None:
    data = {"user_id": USER_ID}
    response = requests.get(f"{SERVER_URL}/export_csv", json=data)

    with open(DOWNLOAD_PATH / "TimeBranchr_export.zip", "wb") as f:
        f.write(response.content)


USER_ID: str = config.get_user_id()
SQL_QUERIES: dict[str, str] = {
    "Categories": "SELECT * FROM categories WHERE user_id = %s",
    "SubCategories": "SELECT * FROM sub_categories WHERE user_id = %s",
    "CategoryLogs": "SELECT * FROM time_logs WHERE user_id = %s",
    "SubCategoryLogs": "SELECT * FROM subcategory_time_logs WHERE user_id = %s",
}
DOWNLOAD_PATH: Path = Path.home() / "Downloads"

user_name: str = config.get_user_name()