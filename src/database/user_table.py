from database.db_connect import db_conn

def init_user(user_id: str, user_name: str) -> None:
    sql_query = """
        INSERT INTO user_data (user_id, user_name)
        VALUES (%s, %s)
    """

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (user_id, user_name))

    db_conn.commit()


def update_user_name(user_id: str, user_name: str) -> None:
    sql_query = """
        UPDATE user_data
        SET user_name = (%s)
        WHERE user_id = (%s)
    """

    with db_conn.cursor() as cursor:
        cursor.execute(sql_query, (user_name, user_id))

    db_conn.commit()
