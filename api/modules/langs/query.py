from app.database import sql, sql_one


def get_langs():
    return sql(
        f"""
            SELECT 
                id, 
                name, 
                short_name 
            FROM 
                langs
        """
    )


def add_lang(name: str):
    return sql_one(
        f"""
            INSERT INTO
                langs
                (name)
            VALUES
                (%s)
            RETURNING *
        """,
        (name,),
    )


def delete_lang(lang_id: int):
    return sql_one(
        f"""
            DELETE FROM
                langs
            WHERE
                id = %s
            RETURNING *
        """,
        (lang_id,),
    )
