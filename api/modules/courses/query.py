from app.database import sql, sql_one


def get_courses():
    return sql(f"SELECT id, name, code FROM courses")


def add_course(name: str):
    return sql_one(
        f"""
            INSERT INTO
                courses
                (name)
            VALUES
                (%s)
            RETURNING *
        """,
        (name,),
    )


def delete_course(cource_id: int):
    return sql_one(
        f"""
            DELETE FROM
                courses
            WHERE
                id = %s
            RETURNING *
        """,
        (cource_id,),
    )
