from PySide6.QtCore import QDateTime
from pymysql import connect


def delete_log_row(log_id: int) -> None:
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
