from fastapi import Request
from datetime import datetime
from api.fast_api import app_api
from database import logs_table
from utils.enums import CategoryType

@app_api.post("/cleanup_log_row")
async def api_cleanup_log_row(request: Request) -> dict[str, str]: 
    data = await request.json()
    category_type = CategoryType(data["category_type"])

    logs_table.cleanup_log_row(
        data["category_id"], 
        category_type
        )

    return {"status": "OK"}


@app_api.get("/get_log_id")
async def api_get_log_id(request: Request) -> dict[str, int]: 
    data = await request.json()
    category_type = CategoryType(data["category_type"])

    log_id: int = logs_table.get_log_id(
        data["user_id"], 
        data["date_time"],
        category_type
        )

    return {"log_id": log_id}


@app_api.get("/get_user_logs")
async def api_get_user_logs(request: Request) -> dict[str, dict[str, list[int]]]: 
    data = await request.json()
    category_type = CategoryType(data["category_type"])

    user_logs: dict[str, list[int]] = logs_table.get_user_logs(
        data["user_id"], 
        category_type
        )

    return {"user_logs": user_logs}


@app_api.get("/get_user_logs_datetime")
async def api_get_user_logs_datetime(request: Request) -> dict[str, dict[str, list[datetime]]]: 
    data = await request.json()
    category_type = CategoryType(data["category_type"])

    logs_datetime: dict[str, list[datetime]] = logs_table.get_user_logs_datetime(
        data["user_id"], 
        category_type
        )

    return {"logs_datetime": logs_datetime}


@app_api.post("/init_log")
async def api_init_log(request: Request) -> dict[str, str]: 
    data = await request.json()
    category_type = CategoryType(data["category_type"])

    logs_table.init_log(
        data["category_id"], 
        data["log_time"],
        data["user_id"], 
        data["date_time"],
        category_type
        )

    return {"status": "OK"}


@app_api.post("/init_subcat_log")
async def api_init_subcat_log(request: Request) -> dict[str, str]: 
    data = await request.json()
    logs_table.init_subcat_log(
        data["category_id"], 
        data["log_time"], 
        data["user_id"], 
        data["date_time"]
        )

    return {"status": "OK"}


@app_api.post("/user_del_log_row")
async def api_user_del_log_row(request: Request) -> dict[str, str]: 
    data = await request.json()
    category_type = CategoryType(data["category_type"])

    logs_table.user_del_log_row(
        data["log_id"], 
        category_type
        )

    return {"status": "OK"}