from app.database import sql, sql_one


def get_theme(theme_id: int):
    return sql_one(
        f"""
            SELECT
                *
            FROM
                themes
            WHERE
                id = %s
        """,
        (theme_id,),
    )


def update_theme(theme_id: int, name: str, module_id: int):
    update_module = f", module_id = %s" if module_id else ""
    return sql_one(
        f"""
            UPDATE 
                themes
            SET 
                name = %s
                {update_module}
            WHERE 
                id = %s
            RETURNING *
        """,
        (name, theme_id, module_id),
    )


def delete_theme(theme_id: int):
    return sql(
        f"""
            DELETE FROM 
                themes 
            WHERE 
                id = %s
            RETURNING *
        """,
        (theme_id,),
    )


def get_exercises(theme_id: int):
    return sql(
        f"""
            SELECT 
                e.*,
                et.name
            FROM
                exercise e 
            JOIN
                exercise_type et
            ON
                e.type_id = et.id
            WHERE
                e.theme_id = %s
        """,
        (theme_id,),
    )


"""
    Получение текущего упражнения ученика
"""


def get_next_exercise(theme_id: int, prev_ex_id: int = None):
    cut_cond = (
        f"JOIN prev_ex_limit pel ON te.row_n = pel.row_n + 1" if prev_ex_id else ""
    )

    return sql_one(
        f"""
            WITH theme_ex AS (
                SELECT
                	row_number() OVER(ORDER BY e.order ASC) AS row_n,
                	*
                FROM
                	exercise e
                WHERE theme_id = %s
                ORDER BY e.order ASC
            ), prev_ex_limit AS (
                SELECT
            		row_n
                FROM
            		theme_ex
                WHERE id = %s
            )
            SELECT
                te.id,
                te.title,
                te.order,
                te.another_data,
                te.theme_id,
                te.type_id
            FROM
                theme_ex te
            {cut_cond}
            LIMIT 1
        """,
        (theme_id, prev_ex_id or 1),
    )


def create_exersise(theme_id: int, type_id: int, title: str):
    return sql_one(
        f"""
            INSERT INTO 
                exercise 
                (theme_id, type_id, title)
            VALUES 
                (%s, %s, %s) 
            RETURNING *
        """,
        (theme_id, type_id, title),
    )
