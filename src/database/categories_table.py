from pymysql import connect


def add_category(db_connection: connect, category_id: str, category_name: str, time: int) -> None:
    sql_query = """
        INSERT INTO categories (category_id, category, total_time)
        VALUES (%s, %s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, category_name, time))

    db_connection.commit()


def delete_category_row(category_id: str) -> None:
    pass


def update_category_name(category_id: str) -> None:
    pass
