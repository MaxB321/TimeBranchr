from pymysql import connect
from pymysql.cursors import DictCursor
from database import logs_table
from gui.widgets.category_widget import CategoryWidget
from utils.category_type import CategoryType


def delete_category_row(db_connection, category_id: str, category_type: CategoryType) -> None:
    logs_table.cleanup_log_row(db_connection, category_id, category_type)

    if category_type == CategoryType.MainCategory:
        sql_query = """
            DELETE FROM categories 
            WHERE category_id = (%s)
        """
    else:
        sql_query = """
            DELETE FROM sub_categories 
            WHERE category_id = (%s)
        """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id))

    db_connection.commit()


def get_category_time(db_connection, category_id: str, category_type: CategoryType) -> int:  # returns the seconds in the total_time column
    if category_type == CategoryType.MainCategory:
        sql_query = """
            SELECT total_time
            FROM categories
            WHERE category_id = (%s)
        """
    else:
        sql_query = """
            SELECT total_time
            FROM sub_categories
            WHERE category_id = (%s)
        """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id))
        row = cursor.fetchone()

    return row["total_time"]


def get_user_categories(db_connection, user_id: str) -> dict[str, str]:
    sql_query = """
        SELECT category_id, category
        FROM categories
        WHERE user_id = (%s)
    """

    user_data: dict[str, str] = {}

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (user_id))
        rows = cursor.fetchall()
        for row in rows:
            user_data[row["category_id"]] = row["category"]
            
    return user_data


def get_user_subcategories(db_connection, user_id: str) -> dict[str, list[str]]:
    sql_query = """
        SELECT category_id, category, parent_id
        FROM sub_categories
        WHERE user_id = (%s)
    """

    user_data: dict[str, list[str]] = {}

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (user_id))
        rows = cursor.fetchall()
        for row in rows:
            user_data[row["category_id"]] = [row["category"], row["parent_id"]]
    
    return user_data


def init_category(db_connection, category_id: str, category_name: str, time: int, user_id: str) -> None:
    sql_query = """
        INSERT INTO categories (category_id, category, total_time, user_id)
        VALUES (%s, %s, %s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, category_name, time, user_id))

    db_connection.commit()


def init_subcategory(db_connection, category_id: str, parent_id: str, category_name: str, time: int, user_id: str) -> None:
    sql_query = """
        INSERT INTO sub_categories (category_id, category, total_time, parent_id, user_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_id, category_name, time, parent_id, user_id))

    db_connection.commit()  


def update_category_name(db_connection, category_id: str, category_name: str, category_type: CategoryType) -> None:
    if category_type == CategoryType.MainCategory:
        sql_query = """
            UPDATE categories
            SET category = (%s)
            WHERE category_id = (%s)
        """
    else:
        sql_query = """
            UPDATE sub_categories
            SET category = (%s)
            WHERE category_id = (%s)
        """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (category_name, category_id))

    db_connection.commit()


def update_parent_time(db_connection, category_id: str, parent_id: str, new_time: int) -> None:  # time_diff should be calc'd using get_cat_time before and after log init
    sql_query = """
            UPDATE sub_categories
            SET total_time = (%s)
            WHERE category_id = (%s)
        """
    
    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (new_time, parent_id))

    db_connection.commit()

    sql_query = """
            UPDATE categories
            SET total_time = (%s)
            WHERE category_id = (%s)
        """
    
    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (new_time, parent_id))

    db_connection.commit()
