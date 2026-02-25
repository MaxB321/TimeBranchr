from pathlib import Path
import pandas as pd
from database.db_connect import db_conn, engine
from utils import config


def export_csv():
    for key, query in SQL_QUERIES.items():
        df: pd.DataFrame = pd.read_sql(query, engine, params=(USER_ID,))
        df.to_csv(f"{DOWNLOAD_PATH}/{key}.csv", index=False)


USER_ID: str = config.get_user_id()
SQL_QUERIES: dict[str, str] = {
    "Categories": "SELECT * FROM categories WHERE user_id = %s",
    "SubCategories": "SELECT * FROM sub_categories WHERE user_id = %s",
    "CategoryLogs": "SELECT * FROM time_logs WHERE user_id = %s",
    "SubCategoryLogs": "SELECT * FROM subcategory_time_logs WHERE user_id = %s",
}
DOWNLOAD_PATH: Path = Path.home() / "Downloads"

user_name: str = config.get_user_name()