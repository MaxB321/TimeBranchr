from pymysql import connect
from pymysql.cursors import DictCursor
from database import logs_table

def delete_category_row(db_connection, category_id: str) -> None:  # when user deletes category
    logs_table.cleanup_log_row(db_connection, category_id)

    # run cat table logic
    sql_query = """
        DELETE FROM categories 
        WHERE category_id = (%s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id))

    db_connection.commit()


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


def get_category_time(db_connection, category_id: str) -> int:  # returns the seconds in the total_time 
    sql_query = """
        SELECT total_time
        FROM categories
        WHERE category_id = (%s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id))
    
        row = cursor.fetchone()
        if row:
            val: int = row["total_time"]
            return val
    
    return 0
    
