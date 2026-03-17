from fastapi import FastAPI, Request
from database.db_connect import engine
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler


app_api = FastAPI()


def get_real_ip(request: Request) -> str:
    return request.headers.get("X-Forwarded-For", request.client.host)

limiter = Limiter(key_func=get_real_ip, default_limits=["100/minute"])

app_api.state.limiter = limiter
app_api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app_api.add_middleware(SlowAPIMiddleware)


from api.routes import api_categories_table, api_logs_table, api_user_table, api_export_csv


@app_api.get("/")
def get_status() -> dict[str, str]:
    return {"status": "API Running"}
