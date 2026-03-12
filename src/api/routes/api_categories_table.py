from fastapi import Request
from api.fast_api import app_api
from database import categories_table
from utils.enums import CategoryType

@app_api.post("/delete_category_row")
async def api_delete_category_row(request: Request) -> dict[str, str]: 
    data = await request.json()
    categories_table.delete_category_row(
        data["category_id"], 
        data["category_type"]
        )

    return {"status": "OK"}


@app_api.get("/get_category_time")
async def api_get_category_time(request: Request) -> dict[str, int]: 
    data = await request.json()
    category_time: int = categories_table.get_category_time(
        data["category_id"], 
        data["category_type"]
        )

    return {"category_time": category_time}


@app_api.get("/get_user_categories")
async def api_get_user_categories(request: Request) -> dict[str, dict[str, str]]: 
    data = await request.json()
    user_categories: dict[str, str] = categories_table.get_user_categories(
        data["user_id"]
        )

    return {"user_categories": user_categories}


@app_api.get("/get_user_subcategories")
async def api_get_user_subcategories(request: Request) -> dict[str, dict[str, list[str]]]: 
    data = await request.json()
    user_subcategories: dict[str, list[str]] = categories_table.get_user_subcategories(
        data["user_id"]
        )

    return {"user_subcategories": user_subcategories}


@app_api.post("/init_category")
async def api_init_category(request: Request) -> dict[str, str]:
    data = await request.json()
    categories_table.init_category(
        data["category_id"], 
        data["category_name"], 
        data["time"],
        data["user_id"]
        )

    return {"status": "OK"}


@app_api.post("/init_subcategory")
async def api_init_subcategory(request: Request) -> dict[str, str]: 
    data = await request.json()
    categories_table.init_subcategory(
        data["category_id"], 
        data["parent_id"], 
        data["category_name"], 
        data["time"],
        data["user_id"]
        )

    return {"status": "OK"}


@app_api.post("/update_category_name")
async def api_update_category_name(request: Request) -> dict[str, str]: 
    data = await request.json()
    categories_table.update_category_name(
        data["category_id"], 
        data["category_name"],
        data["category_type"]
        )

    return {"status": "OK"}


@app_api.post("/update_parent_time")
async def api_update_parent_time(request: Request) -> dict[str, str]: 
    data = await request.json()
    categories_table.update_parent_time(
        data["parent_id"], 
        data["new_time"]
        )

    return {"status": "OK"}

