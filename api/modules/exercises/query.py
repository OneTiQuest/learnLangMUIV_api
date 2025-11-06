from app.database import sql, sql_one
import json


def get_exercises_types():
    return sql(
        f"""
            SELECT 
                *
            FROM
                exercise_type et
        """
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


def delete_exersise(id: int):
    return sql_one(
        f"""
            DELETE FROM 
                exercise 
            WHERE 
                id = %s
            RETURNING *
        """,
        (id,),
    )


def update_exersise(id: int, title: str = None, data: dict = None, type_id: int = None):
    change_title_query = f"title = '{title}'" if title else ""
    change_type_id = f",type_id = '{type_id}'" if type_id else ""

    change_data_query = ""
    if data:
        key, value = data.popitem()
        change_data_query = f"another_data = jsonb_set(COALESCE(another_data, '{{}}')::jsonb, '{{{key}}}', '{json.dumps(value)}'::jsonb)"

    if change_title_query and change_data_query:
        change_title_query += ","

    return sql_one(
        f"""
            UPDATE 
                exercise
            SET 
                {change_title_query}
                {change_data_query}
                {change_type_id}
            WHERE id = %s
            RETURNING *
        """,
        (id,),
    )
