from fastapi import FastAPI
from sqlalchemy import text
from database.db_connect import engine


app_api = FastAPI()


@app_api.get("/")
def get_status() -> dict[str, str]:
    return {"status": "API Running"}
