from pymysql import connect
from pymysql.cursors import DictCursor


def delete_category_row(category_id: str) -> None:
    pass


def init_category(db_connection, category_id: str, category_name: str, time: int) -> None:
    sql_query = """
        INSERT INTO categories (category_id, category, total_time)
        VALUES (%s, %s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, category_name, time))

    db_connection.commit()


def update_category_name(category_id: str) -> None:
    pass
