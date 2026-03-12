import requests
from pathlib import Path
import pandas as pd
from utils import config
from database.db_connect import SERVER_URL


def export_csv() -> None:
    user_id: str = config.get_user_id()
    data = {"user_id": user_id}
    response = requests.get(f"{SERVER_URL}/export_csv", json=data)

    with open(DOWNLOAD_PATH / "TimeBranchr_export.zip", "wb") as f:
        f.write(response.content)


SQL_QUERIES: dict[str, str] = {
    "Categories": "SELECT * FROM categories WHERE user_id = %s",
    "SubCategories": "SELECT * FROM sub_categories WHERE user_id = %s",
    "CategoryLogs": "SELECT * FROM time_logs WHERE user_id = %s",
    "SubCategoryLogs": "SELECT * FROM subcategory_time_logs WHERE user_id = %s",
}
DOWNLOAD_PATH: Path = Path.home() / "Downloads"
