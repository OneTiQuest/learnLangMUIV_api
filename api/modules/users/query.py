from app.database import sql, sql_one
import json


def get_users():
    return sql(
        f"""
            SELECT
            	u.chat_id,
            	u.name,
            	last_name,
            	login,
            	r.name AS role,
            	created_at
            FROM 
            	users u
            JOIN
            	roles r 
            ON
            	r.id = u.role_id
        """
    )


def get_user(id: int):
    return sql(
        f"""
            SELECT 
                name, 
                last_name, 
                login, 
                chat_id, 
                role_id 
            FROM 
                users 
            WHERE 
                id = %s
        """,
        (id,),
    )


def save_user(user_info: dict):
    sql_one(
        f"""
            INSERT INTO 
                users 
                (
                    name, 
                    last_name, 
                    login, 
                    chat_id, 
                    role_id
                ) 
            VALUES 
                (%s, %s, %s, %s, %s) 
            RETURNING *
        """,
        (
            user_info.first_name,
            user_info.last_name,
            user_info.login,
            user_info.chat_id,
            user_info.role_id or 1,
        ),
    )


def create_user_lang(user_id: int, lang_id: int):
    sql_one(
        f"""
            INSERT INTO 
                users_langs 
                (
                    user_id, 
                    lang_id
                ) 
            VALUES 
                (%s, %s)
            ON CONFLICT (user_id, lang_id)
            DO NOTHING
        """,
        (user_id, lang_id),
    )


def set_user_grade(user_id: int, theme_id: int, grade: int):
    sql(
        f"""
            INSERT INTO 
                grades 
                (user_id, theme_id, grade) 
            VALUES 
                (%s, %s, %s)
            RETURNING *
            ON CONFLICT 
                (user_id, theme_id)
            DO NOTHING
        """,
        (user_id, theme_id, grade),
    )


def update_user(user_id: int, role_id: int):
    sql(
        f"""
            UPDATE 
                users 
            SET 
                role_id = %s
            WHERE 
                id = %s
        """,
        (role_id, user_id),
    )


def get_modules(user_id: int):
    return sql(
        f"""
            WITH lang_modules AS (
            	SELECT
            		m.id AS module_id,
            		user_id
            	FROM 
            		users_langs ul
            	JOIN
            		modules m
            	ON 
            		m.lang_id = ul.lang_id
            ), course_modules AS (
            	SELECT
            		module_id,
            		user_id AS cui
            	FROM 
            		courses_modules cm
            	JOIN
            		courses_users cu
            	ON 
            		cm.course_id = cu.course_id::int
            ), m_ids AS (
            	SELECT 
            		*
            	FROM
            		lang_modules lm
            	FULL JOIN
            		course_modules cm
            	USING(module_id)
            )
            SELECT
            	id,
            	name
            FROM 
            	m_ids
            JOIN
            	modules m
            ON
            	m_ids.module_id = m.id
            WHERE 
            	m_ids.user_id = %s
            	AND 
            	m_ids.cui = %s
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
    sql(
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
                    s.user_id = %s
            )
            ON CONFLICT (course_id, module_id)
            DO NOTHING
        """,
        (module_id, user_id),
    )


def get_grades(user_id: int):
    sql(
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
            ON gr.module_id = m.id
            GROUP BY m.id 
        """,
        (user_id),
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
            	ON u.id = ul.user_id
            	JOIN
            		courses_users cu
            	ON
            		cm.user_id = u.id 
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
            	ON m.id = cm.module_id
            	JOIN
            		cl
            	ON cl.lang_id = m.lang_id 
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
            	ON m.id = ex_by_themes.module_id
            	GROUP BY m.id
            )
            SELECT * FROM modules_t 
        """,
        (teacher_id),
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
                (%s, %s, %s);
            ON CONFLICT 
                (exercise_id, user_id)
            DO UPDATE
                SET answer = %s
            RETURNING *
        """,
        (exersice_id, user_id, answer, answer),
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
