from fastapi import Request
from api.fast_api import app_api
from database import user_table

@app_api.post("/init_user")
async def api_init_user(request: Request) -> dict[str, str]: 
    data = await request.json()
    user_table.init_user(
        data["user_id"], 
        data["user_name"]
        )

    return {"status": "OK"}


@app_api.post("/update_user_name")
async def api_update_user_name(request: Request) -> dict[str, str]: 
    data = await request.json()
    user_table.update_user_name(
        data["user_id"], 
        data["user_name"]
        )

    return {"status": "OK"}
