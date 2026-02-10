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


def get_user_logs(db_connection, user_id: str) -> dict[str, int]:  # need date-time and log_time for user logs to load user data 
    sql_query = """
        SELECT log_time
        FROM time_logs
        WHERE user_id = (%s)
    """
    user_data: dict[str, int] = {}

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (user_id))
        rows = cursor.fetchall()
        user_data.update( [row["category"] for row in rows] )
        user_data.update( [row["log_time"] for row in rows] )

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
