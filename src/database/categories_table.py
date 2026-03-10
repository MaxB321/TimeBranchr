from database import logs_table
from database.db_connect import db_conn
from utils.enums import CategoryType


def delete_category_row(category_id: str, category_type: CategoryType) -> None:
    logs_table.cleanup_log_row(category_id, category_type)

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

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (category_id))

    db_conn.commit()


def get_category_time(category_id: str, category_type: CategoryType) -> int:  # returns the seconds in the total_time column
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

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (category_id))
        row = cursor.fetchone()
        if not row:
            return 1
    
    return row["total_time"]


def get_user_categories(user_id: str) -> dict[str, str]:
    sql_query = """
        SELECT category_id, category
        FROM categories
        WHERE user_id = (%s)
    """

    user_data: dict[str, str] = {}

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (user_id))
        rows = cursor.fetchall()
        for row in rows:
            user_data[row["category_id"]] = row["category"]
            
    return user_data


def get_user_subcategories(user_id: str) -> dict[str, list[str]]:
    sql_query = """
        SELECT category_id, category, parent_id
        FROM sub_categories
        WHERE user_id = (%s)
    """

    user_data: dict[str, list[str]] = {}

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (user_id))
        rows = cursor.fetchall()
        for row in rows:
            user_data[row["category_id"]] = [row["category"], row["parent_id"]]
    
    return user_data


def init_category(category_id: str, category_name: str, time: int, user_id: str) -> None:
    sql_query = """
        INSERT INTO categories (category_id, category, total_time, user_id)
        VALUES (%s, %s, %s, %s)
    """

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (category_id, category_name, time, user_id))

    db_conn.commit()


def init_subcategory(category_id: str, parent_id: str, category_name: str, time: int, user_id: str) -> None:
    sql_query = """
        INSERT INTO sub_categories (category_id, category, total_time, parent_id, user_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (category_id, category_name, time, parent_id, user_id))

    db_conn.commit()  


def update_category_name(category_id: str, category_name: str, category_type: CategoryType) -> None:
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

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (category_name, category_id))

    db_conn.commit()


def update_parent_time(parent_id: str, new_time: int) -> None:
    sql_query = """
            UPDATE sub_categories
            SET total_time = (%s)
            WHERE category_id = (%s)
        """
    
    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (new_time, parent_id))

    db_conn.commit()

    sql_query = """
            UPDATE categories
            SET total_time = (%s)
            WHERE category_id = (%s)
        """
    
    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (new_time, parent_id))

    db_conn.commit()
