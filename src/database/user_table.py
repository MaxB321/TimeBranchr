

def init_user(db_connection, user_id: str, user_name: str) -> None:
    sql_query = """
        INSERT INTO user_data (user_id, user_name)
        VALUES (%s, %s)
    """

    with db_connection.cursor() as cursor:
        cursor.execute(sql_query, (user_id, user_name))

    db_connection.commit()


def update_user_name(user_id: str) -> None:  # allow user to change name and update the mysql column 
    pass
