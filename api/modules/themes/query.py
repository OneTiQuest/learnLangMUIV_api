from app.database import sql, sql_one


def update_theme(theme_id: int, name: str):
    sql(
        f"""
            UPDATE 
                themes
            SET 
                name = %s
            WHERE 
                id = %s
        """,
        (name, theme_id),
    )


def delete_theme(theme_id: int):
    sql(
        f"""
            DELETE FROM 
                themes 
            WHERE 
                id = %s
        """,
        (theme_id),
    )
