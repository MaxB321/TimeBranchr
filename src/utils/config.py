from json.decoder import JSONDecodeError
import os
import json
from pathlib import Path


def get_user_id() -> str:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError("Config not found.")
    
    config: dict = {}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        raise RuntimeError("Config missing id field.")

    user_id: str = config["user_id"]
    return user_id


def get_user_name() -> str:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError("Config not found.")
    
    config: dict = {}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        raise RuntimeError("Config missing name field.")
    
    user_name: str = config["user_name"]
    return user_name


def isConfig() -> bool:  # checks if config is present on local drive
    return CONFIG_FILE.exists()


def write_config(user_id: str, user_name: str) -> None:
    CONFIG_PATH.mkdir(parents=True, exist_ok=True)
    user_data = {
        "user_id": user_id,
        "user_name": user_name
    }
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4)


# Constants
APPDATA_PATH: Path = Path(os.environ["APPDATA"])
APP_NAME: str = "TimeBranchr"
CONFIG_PATH: Path = APPDATA_PATH / APP_NAME
CONFIG_FILE: Path = CONFIG_PATH / "config.json"
