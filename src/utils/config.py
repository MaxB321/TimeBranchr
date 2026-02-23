from json.decoder import JSONDecodeError
import os
import json
from pathlib import Path


def create_config(user_id: str, user_name: str) -> None:
    CONFIG_PATH.mkdir(parents=True, exist_ok=True)
    user_data = {
        "user": {
            "user_id": user_id,
            "user_name": user_name
        },
        "view_flags": {
            "dark_mode": True,
            "show_subcat_totals": True,
            "show_username": True,
            "categories_asc": True,
            "logs_asc": True
        }   
    }
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4)


def get_flag(key: str) -> bool:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError("Config not found.")
    
    config: dict = {}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        raise RuntimeError("Config missing name field.")
    
    flag: bool = config["view_flags"][key]

    return flag


def get_user_id() -> str:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError("Config not found.")
    
    config: dict = {}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        raise RuntimeError("Config missing id field.")

    user_id: str = config["user"]["user_id"]
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
    
    user_name: str = config["user"]["user_name"]
    return user_name


def isConfig() -> bool:  # checks if config is present on local drive
    return CONFIG_FILE.exists()


def set_flag(key: str, val: bool) -> None:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError("Config not found.")
    
    config: dict = {}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        raise RuntimeError("Config missing name field.")
    
    config["view_flags"][key] = val

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def update_username(name: str) -> None:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError("Config not found.")
    
    config: dict = {}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError:
        raise RuntimeError("Config missing name field.")
    
    config["user"]["user_name"] = name

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


# Constants
APPDATA_PATH: Path = Path(os.environ["APPDATA"])
APP_NAME: str = "TimeBranchr"
CONFIG_PATH: Path = APPDATA_PATH / APP_NAME
CONFIG_FILE: Path = CONFIG_PATH / "config.json"

# FLAGS
if isConfig():
    dark_mode: bool = get_flag("dark_mode")
    show_subcat_totals: bool = get_flag("show_subcat_totals")
    show_username: bool = get_flag("show_username")
    categories_asc: bool = get_flag("categories_asc")
    logs_asc: bool = get_flag("logs_asc")
