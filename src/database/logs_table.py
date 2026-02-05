from pymysql import connect


def add_log(db_connection: connect, category_id: str, log_time: int) -> None:
    sql_query = """
        INSERT INTO time_logs (category_id, log_time)
        VALUES (%s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, log_time))

    db_connection.commit()


def delete_log_row(log_id: int) -> None:
    pass


def get_log_id() -> int:
    return 0
