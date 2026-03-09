from fastapi import FastAPI
from database.db_connect import engine


app_api = FastAPI()


from api.routes import api_categories_table, api_logs_table, api_user_table


@app_api.get("/")
def get_status() -> dict[str, str]:
    return {"status": "API Running"}
