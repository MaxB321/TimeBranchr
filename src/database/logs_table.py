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


def user_del_log_row() -> None:  
    pass


def get_log_id(category_id: str, user_id: str, date_time: QDateTime) -> int:  # will primarily be for deleting logs
    return 0


def init_log(db_connection, category_id: str, log_time: int) -> None:
    sql_query = """
        INSERT INTO time_logs (category_id, log_time)
        VALUES (%s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, log_time))

    db_connection.commit()
