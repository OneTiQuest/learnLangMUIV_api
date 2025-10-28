from app.database import sql, sql_one
import json


def get_exercises(theme_id: int):
    return sql(
        f"""
            SELECT 
                *
            FROM
                exercise e 
            WHERE
                e.theme_id = %s
        """,
        (theme_id,),
    )


def get_exercises_types():
    return sql(
        f"""
            SELECT 
                *
            FROM
                exercise_type et
        """
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


def get_exersise(id: int):
    return sql_one(
        f"""
            SELECT 
                * 
            FROM 
                exercise 
            WHERE 
                id = %s
        """,
        (id,),
    )


def update_exersise(id: int, title: str = None, data: dict = None):
    change_title_query = f"title = '{title}'," if title else ""

    change_data_query = ""
    if data:
        key, value = data.popitem()
        change_data_query = f"another_data = jsonb_set(COALESCE(another_data, '{{}}')::jsonb, '{{{key}}}', '{json.dumps(value)}'::jsonb)"

    sql(
        f"""
            UPDATE 
                exercise
            SET 
                {change_title_query}
                {change_data_query}
            WHERE id = %s
        """,
        (id,),
    )


"""
Получение текущего упражнения ученика
"""


def get_next_exercise(theme_id: int, prev_ex_id: int = None):
    cut_cond = (
        f"JOIN prev_ex_limit pel ON te.row_n = pel.row_n + 1" if prev_ex_id else ""
    )

    return sql(
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
