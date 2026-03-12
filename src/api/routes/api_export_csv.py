from fastapi import Response, Request
import pandas as pd
import io
import zipfile
from api.fast_api import app_api
from database.db_connect import engine


SQL_QUERIES: dict[str, str] = {
    "Categories": "SELECT * FROM categories WHERE user_id = %s",
    "SubCategories": "SELECT * FROM sub_categories WHERE user_id = %s",
    "CategoryLogs": "SELECT * FROM time_logs WHERE user_id = %s",
    "SubCategoryLogs": "SELECT * FROM subcategory_time_logs WHERE user_id = %s",
}

@app_api.get("/export_csv")
async def api_export_csv(request: Request) -> Response:
    data = await request.json()
    user_id = data["user_id"]
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_STORED) as zf:
        for filename, query in SQL_QUERIES.items():
            df: pd.DataFrame = pd.read_sql(query, engine, params=(user_id,))
            csv_data = df.to_csv(index=False)

            zf.writestr(f"{filename}.csv", csv_data)
    
    zip_buffer.seek(0)

    return Response(
        content=zip_buffer.getvalue(),
        headers={"Content-Disposition": "attachment; filename=user_export.zip"},
        media_type="application/zip"
    )