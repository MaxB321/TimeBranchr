from pymysql import connect
from pymysql.cursors import DictCursor


def delete_category_row(category_id: str) -> None:  # when user deletes category
    pass


def init_category(db_connection, category_id: str, category_name: str, time: int) -> None:
    sql_query = """
        INSERT INTO categories (category_id, category, total_time)
        VALUES (%s, %s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, category_name, time))

    db_connection.commit()


def update_category_name(db_connection, category_id: str, category_name: str) -> None:
    sql_query = """
        UPDATE categories
        SET category = (%s)
        WHERE category_id = (%s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_name, category_id))

    db_connection.commit()


def get_category_time(category_id: str) -> int:  # returns the seconds in the total_time 
    return 0
