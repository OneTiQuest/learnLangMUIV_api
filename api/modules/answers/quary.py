from app.database import sql, sql_one

def save_answer(ex_id: int, user_id: int, answer: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                DELETE FROM answers WHERE exercise_id = {ex_id} AND user_id = {user_id};
                INSERT INTO answers (exercise_id, user_id, answer) VALUES ({ex_id}, {user_id}, %s);
            """,
            (answer,)
        )


def get_user_answers(user_id: int, theme_id: int):
    return run_sql(
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
            	AND t.id = {theme_id}
            	AND a.user_id = {user_id}
        """
    )
