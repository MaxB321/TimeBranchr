from fastapi import Request
from api.fast_api import app_api
from database import logs_table

@app_api.post("/cleanup_log_row")
async def api_cleanup_log_row(request: Request) -> dict[str ,str]: 
    data = await request.json()
    logs_table.cleanup_log_row(
        data["category_id"], 
        data["category_type"]
        )

    return {"status": "OK"}


@app_api.post("/get_log_id")
async def api_get_log_id(request: Request) -> dict[str ,str]: 
    data = await request.json()
    logs_table.get_log_id(
        data["user_id"], 
        data["date_time"],
        data["category_type"]
        )

    return {"status": "OK"}


@app_api.post("/get_user_logs")
async def api_get_user_logs(request: Request) -> dict[str ,str]: 
    data = await request.json()
    logs_table.get_user_logs(
        data["user_id"], 
        data["category_type"]
        )

    return {"status": "OK"}


@app_api.post("/get_user_logs_datetime")
async def api_get_user_logs_datetime(request: Request) -> dict[str ,str]: 
    data = await request.json()
    logs_table.get_user_logs_datetime(
        data["user_id"], 
        data["category_type"]
        )

    return {"status": "OK"}


@app_api.post("/init_log")
async def api_init_log(request: Request) -> dict[str ,str]: 
    data = await request.json()
    logs_table.init_log(
        data["category_id"], 
        data["log_time"],
        data["user_id"], 
        data["date_time"],
        data["category_type"]
        )

    return {"status": "OK"}


@app_api.post("/init_subcat_log")
async def api_init_subcat_log(request: Request) -> dict[str ,str]: 
    data = await request.json()
    logs_table.init_subcat_log(
        data["category_id"], 
        data["log_time"], 
        data["user_id"], 
        data["date_time"]
        )

    return {"status": "OK"}


@app_api.post("/user_del_log_row")
async def api_user_del_log_row(request: Request) -> dict[str ,str]: 
    data = await request.json()
    logs_table.user_del_log_row(
        data["log_id"], 
        data["category_type"]
        )

    return {"status": "OK"}