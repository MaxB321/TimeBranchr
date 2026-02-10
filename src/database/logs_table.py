from PySide6.QtCore import QDateTime
from pymysql import connect


def cleanup_log_row(db_connection, category_id: str) -> None:   
    sql_query = """
        DELETE FROM time_logs 
        WHERE category_id = (%s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id))

    db_connection.commit()


def get_log_id(category_id: str, user_id: str, date_time: QDateTime) -> int:  # will primarily be for deleting logs
    return 0


def get_user_logs(db_connection, user_id: str) -> dict[str, list[int]]: 
    sql_query = """
        SELECT category_id, log_time
        FROM time_logs
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


def init_log(db_connection, category_id: str, log_time: int, user_id: str) -> None:
    sql_query = """
        INSERT INTO time_logs (category_id, log_time, user_id)
        VALUES (%s, %s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, log_time, user_id))

    db_connection.commit()


def user_del_log_row() -> None:  
    pass
