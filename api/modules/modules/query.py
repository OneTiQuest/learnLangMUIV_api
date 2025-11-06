from app.database import sql, sql_one


def update_module(module_id: int, name: str, lang_id: int):
    update_lang = f", lang_id = {lang_id}" if lang_id else ""

    return sql_one(
        f"""
            UPDATE 
                modules 
            SET 
                name = %s
                {update_lang}
            WHERE 
                id = %s
            RETURNING *
        """,
        (name, module_id),
    )


def delete_module(module_id: int):
    return sql(
        f"""
            DELETE FROM 
                modules 
            WHERE 
                id = %s
            RETURNING *
        """,
        (module_id,),
    )


def create_module(name: str, lang_id: int):
    return sql_one(
        f"""
            INSERT INTO 
                modules
                (
                    name,
                    lang_id
                )
            VALUES 
                (
                    %s,
                    %s
                )
            RETURNING id
        """,
        (name, lang_id),
    )


def put_module_course(module_id: int, courses_ids: list[int]):
    return sql_one(
        f"""
            DELETE FROM courses_modules WHERE module_id = %s;
            INSERT INTO
                courses_modules
                (module_id, course_id)
            VALUES
                (%s, UNNEST(%s))
            ON CONFLICT 
                (module_id, course_id)
            DO NOTHING
            RETURNING *
        """,
        (module_id, module_id, courses_ids),
    )


def get_module(module_id: int):
    return sql_one(
        f"""
            SELECT
            	m.id,
                m.name,
               	jsonb_agg(jsonb_strip_nulls(jsonb_build_object('id', l.id, 'name', l.name))) FILTER (WHERE l.id IS NOT NULL) AS langs,
               	jsonb_agg(jsonb_strip_nulls(jsonb_build_object('id', c.id, 'name', c.name)))  FILTER (WHERE c.id IS NOT NULL) AS courses
            FROM 
            	modules m
            LEFT JOIN
                langs l
            ON
                l.id = m.lang_id
            LEFT JOIN
            	courses_modules cm 
            ON
            	m.id = cm.module_id
            LEFT JOIN
            	courses c
            ON
            	cm.course_id = c.id 
            WHERE
            	m.id = %s
            GROUP BY 
                (m.id, m.name)
        """,
        (module_id,),
    )


def get_modules():
    return sql(
        f"""
            SELECT
            	m.id,
                m.name
            FROM 
            	modules m
        """
    )


def get_themes_by_module_id(module_id: int):
    return sql(
        f"""
            SELECT
            	id,
                name
            FROM 
            	themes t
            WHERE
            	module_id = %s
            ORDER BY t."order" ASC
        """,
        (module_id,),
    )


def create_theme(module_id: int, name: str):
    return sql_one(
        f"""
            INSERT INTO 
                themes
                (
                    name,
                    module_id
                )
            VALUES
                (%s, %s)
            RETURNING *
        """,
        (name, module_id),
    )
