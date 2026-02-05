from typing import Final
from dotenv import load_dotenv
import pymysql
import os


load_dotenv()

def require_env(var: str) -> str:
    env_val: Final = os.getenv(var)
    if env_val is None:
        raise RuntimeError(f"Missing environment variable: {var}")
    return env_val


DB_HOST: Final = require_env("DB_HOST")
DB_USER: Final = require_env("DB_USER")
DB_PASSWORD: Final = require_env("DB_PASSWORD")
DB_NAME: Final = require_env("DB_NAME")
DB_CHARSET: Final = require_env("DB_CHARSET")

db_conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset=DB_CHARSET,
    cursorclass=pymysql.cursors.DictCursor
)
