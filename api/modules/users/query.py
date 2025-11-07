from app.database import sql, sql_one
import json


def get_users():
    return sql(
        f"""
            SELECT
                u.*,
            	r.name AS role_name
            FROM 
            	users u
            JOIN
            	roles r 
            ON
            	r.id = u.role_id
        """
    )


def get_user(id: int):
    return sql_one(
        f"""
            SELECT 
                u.*,
            	r.name AS role_name,
                jsonb_agg(jsonb_strip_nulls(jsonb_build_object('id', l.id, 'name', l.name)))  FILTER (WHERE l.id IS NOT NULL) AS langs,
               	jsonb_agg(jsonb_strip_nulls(jsonb_build_object('id', c.id, 'name', c.name)))  FILTER (WHERE c.id IS NOT NULL) AS courses
            FROM
                users u

            JOIN
            	roles r 
            ON
            	r.id = u.role_id
                
            LEFT JOIN
            	courses_users cu 
            ON
            	u.id = cu.user_id
            LEFT JOIN
            	courses c
            ON
            	c.id = cu.course_id
                
                
            LEFT JOIN
            	users_langs  ul
            ON
            	u.id = ul.user_id
                
            LEFT JOIN
            	langs  l
            ON
            	l.id = ul.lang_id

            WHERE 
                u.id = %s
            GROUP BY (u.id, r.name)
            LIMIT 1
        """,
        (id,),
    )


def get_auth_user(login: str, password: str):
    return sql_one(
        f"""
            SELECT
                u.*
            FROM 
                users u
            WHERE 
                login = %s
                AND password = %s
            LIMIT 1
        """,
        (login, password),
    )


def has_login(login: str):
    return sql_one(
        f"""
            SELECT 
                True
            FROM 
                users 
            WHERE 
                login = %s
            LIMIT 1
        """,
        (login,),
    )


def save_user(user_info: dict):
    return sql_one(
        f"""
            INSERT INTO 
                users
                (
                    name, 
                    last_name, 
                    login,
                    password,
                    chat_id, 
                    role_id
                ) 
            VALUES 
                (
                    %(first_name)s, 
                    %(last_name)s, 
                    %(login)s, 
                    %(password)s, 
                    %(chat_id)s, 
                    %(role_id)s
                ) 
            RETURNING *
        """,
        user_info,
    )


def delete_user(user_id: int):
    return sql_one(
        f"""
            DELETE FROM
                users
            WHERE
                id = %s
            RETURNING *
        """,
        (user_id,),
    )


def set_role(user_id: int, role_id: int):
    return sql(
        f"""
            UPDATE
                users 
            SET 
                role_id = %s
            WHERE
                id = %s
            RETURNING *
        """,
        (role_id, user_id),
    )


def set_chat(user_id: int, chat_id: int):
    return sql(
        f"""
            UPDATE
                users 
            SET 
                chat_id = %s
            WHERE
                id = %s
            RETURNING *
        """,
        (chat_id, user_id),
    )


def create_user_lang(user_id: int, langs_ids: int):
    return sql_one(
        f"""
            INSERT INTO 
                users_langs 
                (
                    user_id, 
                    lang_id
                ) 
            VALUES 
                (%s, UNNEST(%s))
            ON CONFLICT 
                (user_id, lang_id)
            DO NOTHING
            RETURNING *
        """,
        (user_id, langs_ids),
    )


def put_user_lang(user_id: int, langs_ids: int):
    return sql_one(
        f"""
            DELETE FROM users_langs WHERE user_id = %s;
            INSERT INTO 
                users_langs 
                (
                    user_id, 
                    lang_id
                ) 
            VALUES 
                (%s, UNNEST(%s))
            ON CONFLICT 
                (user_id, lang_id)
            DO NOTHING
            RETURNING *
        """,
        (user_id, user_id, langs_ids),
    )


def set_user_grade(user_id: int, theme_id: int, grade: int):
    return sql(
        f"""
            INSERT INTO 
                grades 
                (user_id, theme_id, grade) 
            VALUES 
                (%s, %s, %s)
            ON CONFLICT 
                (user_id, theme_id)
            DO UPDATE
            SET grade = %s
            RETURNING *
        """,
        (user_id, theme_id, grade, grade),
    )


def get_user_grade(user_id: int, theme_id: int):
    return sql_one(
        f"""
            SELECT 
                g.grade
            FROM 
                grades  g
            WHERE 
                g.user_id = %s
                AND g.theme_id = %s
        """,
        (user_id, theme_id),
    )


def update_user(user_id: int, role_id: int, user_data):
    params = {"role_id": role_id, "user_id": user_id}
    params.update(user_data)

    update_first_name = (
        f", name = %(first_name)s" if user_data.get("first_name") else ""
    )
    update_last_name = (
        f", last_name = %(last_name)s" if user_data.get("last_name") else ""
    )
    update_login = f", login = %(login)s" if user_data.get("login") else ""
    update_password = f", password = %(password)s" if user_data.get("password") else ""
    update_role = f", role_id = %(role_id)s" if user_data.get("role_id") else ""

    return sql(
        f"""
            UPDATE 
                users 
            SET 
                role_id = %(role_id)s
                {update_first_name}
                {update_last_name}
                {update_login}
                {update_password}
                {update_role}
            WHERE 
                id = %(user_id)s
            RETURNING *
        """,
        params,
    )


def get_modules(user_id: int, is_full: bool = False):
    full_query = ""
    if not is_full:
        full_query = f"""
                JOIN
                    modules_by_course mc
                ON
                    m.id = mc.module_id
                JOIN
                    modules_by_langs ml
                ON
                    m.lang_id = ml.lang_id 
            """

    return sql(
        f"""
            WITH modules_by_course AS (
                SELECT
                    cm.module_id 
                FROM
                    courses_users cu 
                JOIN
                    courses_modules cm
                ON
                    cm.course_id = cu.course_id 
                WHERE
                    cu.user_id = %s
            ), modules_by_langs AS (
                SELECT
                    ul.lang_id
                FROM
                    users_langs ul 
                WHERE
                    ul.user_id = %s
            )
            SELECT DISTINCT
                m.id,
                m.name,
                l.name
            FROM
                modules m
            JOIN
                langs l
            ON
                l.id = m.lang_id
            {full_query}
            ORDER BY id ASC
        """,
        (user_id, user_id),
    )


def get_user_langs(user_id: int):
    return sql(
        f"""
            SELECT 
                id, 
                name, 
                short_name 
            FROM 
                langs l
           	JOIN 
                users_langs ul 
            ON
                ul.lang_id = l.id 
            WHERE
                ul.user_id = %s
        """,
        (user_id,),
    )


# TODO Привязывать к конкретному курсу
def create_module(user_id: int, module_id: int):
    return sql(
        f"""
            INSERT INTO 
                courses_modules 
            (
                course_id, 
                module_id
            ) 
            ( 
                SELECT
                    course_id,
                    %s
                FROM
                    courses_users cu
                WHERE
                    cu.user_id = %s
            )
            ON CONFLICT (course_id, module_id)
            DO NOTHING
            RETURNING *
        """,
        (module_id, user_id),
    )


def get_grades(user_id: int):
    return sql(
        f"""
            WITH gr AS (
                SELECT 
                    t.name, 
                    g.grade,
                    t.module_id 
                FROM 
                    grades  g
                JOIN
                    themes t
                ON
                    t.id = g.theme_id 
                
                WHERE 
                    g.user_id = %s
            )
            SELECT
                m."name",
                json_agg(gr)
            FROM
                modules m
            JOIN
                gr
            ON 
                gr.module_id = m.id
            GROUP BY m.id 
        """,
        (user_id,),
    )


def get_teacher_stat(teacher_id: int):
    return sql(
        f"""
            WITH cl AS (
            	SELECT
            		lang_id,
            		course_id
            	FROM
            		users u
            	JOIN
            		users_langs ul
            	ON 
                    u.id = ul.user_id
            	JOIN
            		courses_users cu
            	ON
            		cu.user_id = u.id 
            	WHERE u.id = %s
            ), modules_t AS (
            	SELECT 
            		m.id AS module_id,
            		m.name AS module_name,
            		json_agg(ex_by_themes) AS ex_by_themes
            	FROM
            		modules m
            	JOIN
            		courses_modules cm 
            	ON
                    m.id = cm.module_id
            	JOIN
            		cl
            	ON 
                    cl.lang_id = m.lang_id 
            	    AND cl.course_id = cm.course_id 
            	JOIN
            		(
            			SELECT
            				t.id,
				            t.name AS theme_name,
				            t.module_id,
				            json_agg(
				            	json_build_object(
				            		'grade', g.grade, 
				            		'user', u
				            	)
				            ) as grades_data
            			FROM
            				themes t
            			JOIN
            				grades g
            			ON 	g.theme_id = t.id
            			JOIN
            				users u
            			ON u.id = g.user_id 
            			GROUP BY t.id
            		) AS ex_by_themes
            	ON 
                    m.id = ex_by_themes.module_id
            	GROUP BY m.id
            )
            SELECT * FROM modules_t 
        """,
        (teacher_id,),
    )


def get_answers(user_id: int, theme_id: int):
    return sql(
        f"""
            SELECT
            	a.answer,
            	e.another_data::json->>'success_answer'
            FROM 
            	answers a
            JOIN
            	exercise e 
            ON 
            	a.exercise_id = e.id
            JOIN
            	themes t 
            ON
            	t.id = e.theme_id 
            WHERE
            	e.type_id IN (1, 2, 4)
                AND a.user_id = %s
            	AND t.id = %s
        """,
        (user_id, theme_id),
    )


def create_answer(exersice_id: int, user_id: int, answer: str):
    return sql_one(
        f"""
            INSERT INTO 
                answers 
                (exercise_id, user_id, answer) 
            VALUES 
                (%s, %s, %s)
            ON CONFLICT 
                (exercise_id, user_id)
            DO UPDATE
                SET answer = %s
            RETURNING *
        """,
        (exersice_id, user_id, answer, answer),
    )


def get_user_courses(user_id: int):
    return sql(
        f"""
            SELECT
                *
            FROM
                courses_users cu
            JOIN
                courses c
            ON
                cu.course_id = c.id
            WHERE
                cu.user_id = %s
        """,
        (user_id,),
    )


def set_user_course(user_id: int, courses_ids: list[int]):
    return sql(
        f"""
            INSERT INTO
                courses_users
                (user_id, course_id)
            VALUES
                (%s, UNNEST(%s))
            ON CONFLICT 
                (user_id, course_id)
            DO NOTHING
            RETURNING *
        """,
        (user_id, courses_ids),
    )


def put_user_course(user_id: int, courses_ids: int):
    return sql_one(
        f"""
            DELETE FROM courses_users WHERE user_id = %s;
            INSERT INTO
                courses_users
                (user_id, course_id)
            VALUES
                (%s, UNNEST(%s))
            ON CONFLICT 
                (user_id, course_id)
            DO NOTHING
            RETURNING *
        """,
        (user_id, user_id, courses_ids),
    )


def upsert_settings(user_id: int, setting_name=None, value=None):
    res = sql_one(f"SELECT settings FROM settings WHERE user_id=%s", (user_id))
    settings = res and json.loads(res[0])

    if not settings:
        settings = {"course_id": None}
        sql(
            f"INSERT INTO settings (settings, user_id) VALUES (%s, %s)",
            (json.dumps(settings), user_id),
        )

    if setting_name and value:
        settings[setting_name] = value
        sql(
            f"UPDATE settings SET settings = %s, user_id = %s WHERE user_id=%s",
            (json.dumps(settings), user_id, user_id),
        )

    return settings
