from datetime import datetime
from pymysql import connect

from utils.enums import CategoryType


def cleanup_log_row(db_connection, category_id: str, category_type: CategoryType) -> None:   
    if category_type == CategoryType.MainCategory:
        sql_query = """
            DELETE FROM time_logs 
            WHERE category_id = (%s)
        """
    else:
        sql_query = """
            DELETE FROM subcategory_time_logs 
            WHERE category_id = (%s)
        """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id))

    db_connection.commit()


def get_log_id(db_connection, user_id: str, date_time: datetime, category_type: CategoryType) -> int:  # will primarily be for deleting logs
    if category_type == CategoryType.MainCategory:
        sql_query = """
            SELECT log_id
            FROM time_logs 
            WHERE user_id = (%s) AND date_time = (%s)
        """
    else:
        sql_query = """
            SELECT log_id
            FROM subcategory_time_logs 
            WHERE user_id = (%s) AND date_time = (%s)
        """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (user_id, date_time))
        row = cursor.fetchone()

    db_connection.commit()
    
    return row["log_id"]


def get_user_logs(db_connection, user_id: str, category_type: CategoryType) -> dict[str, list[int]]:  # add categoryType arg, call it twice and just append the second call results after the first in dict
    if category_type == CategoryType.MainCategory:
        sql_query = """
            SELECT category_id, log_time
            FROM time_logs
            WHERE user_id = (%s)
        """
    else:
        sql_query = """
            SELECT category_id, log_time
            FROM subcategory_time_logs
            WHERE user_id = (%s)
        """

    user_data: dict[str, list[int]] = {}
    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (user_id))
        rows = cursor.fetchall() 
        
        for row in rows:
            if row["category_id"] not in user_data:
                user_data[row["category_id"]] = []
            user_data[row["category_id"]].append(row["log_time"])

    return user_data


def get_user_logs_datetime(db_connection, user_id: str, category_type: CategoryType) -> dict[str, list[datetime]]:
    if category_type == CategoryType.MainCategory:
        sql_query = """
            SELECT category_id, date_time
            FROM time_logs
            WHERE user_id = (%s)
        """
    else:
        sql_query = """
            SELECT category_id, date_time
            FROM subcategory_time_logs
            WHERE user_id = (%s)
        """

    user_data: dict[str, list[datetime]] = {}
    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (user_id))
        rows = cursor.fetchall() 
        
        for row in rows:
            if row["category_id"] not in user_data:
                user_data[row["category_id"]] = []
            user_data[row["category_id"]].append(row["date_time"])

    return user_data 


def init_log(db_connection, category_id: str, log_time: int, user_id: str, date_time: datetime, category_type: CategoryType) -> None:
    if category_type == CategoryType.MainCategory:
        sql_query = """
            INSERT INTO time_logs (category_id, log_time, user_id, date_time)
            VALUES (%s, %s, %s, %s)
        """
    else:
        sql_query = """
            INSERT INTO subcategory_time_logs (category_id, log_time, user_id, date_time)
            VALUES (%s, %s, %s, %s)
        """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, log_time, user_id, date_time))

    db_connection.commit()


def init_subcat_log(db_connection, category_id: str, log_time: int, user_id: str, date_time: datetime) -> None:
    sql_query = """
        INSERT INTO subcategory_time_logs (category_id, log_time, user_id, date_time)
        VALUES (%s, %s, %s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, log_time, user_id, date_time))

    db_connection.commit()


def user_del_log_row(db_connection, log_id: int, category_type: CategoryType) -> None:  
    if category_type == CategoryType.MainCategory:
        sql_query = """
            DELETE FROM time_logs
            WHERE log_id = (%s)
        """
    else:
        sql_query = """
            DELETE FROM subcategory_time_logs
            WHERE log_id = (%s)
        """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (log_id))

    db_connection.commit()
