from app.database import sql, sql_one

"""
Получение текущего упражнения ученика
"""
def get_exercise(theme_id: int, prev_ex_id: int=None):
    cut_cond = ''
    if prev_ex_id:
        cut_cond += f"JOIN prev_ex_limit pel ON te.row_n = pel.row_n + 1"

    return run_sql(
        f"""
            WITH theme_ex AS (
                SELECT
                	row_number() OVER(ORDER BY e.order ASC) AS row_n,
                	*
                FROM
                	exercise e
                WHERE theme_id = {theme_id}
                ORDER BY e.order ASC
            ), prev_ex_limit AS (
                SELECT
            		row_n
                FROM
            		theme_ex
                WHERE id = {prev_ex_id or 1}
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
        True
    )

def get_exersises(theme_id: int):
    return run_sql(
        f"""
            SELECT 
                *
            FROM
                exercise e 
            WHERE
                e.theme_id = {theme_id}
        """
    )

def get_exersises_types():
    return run_sql(
        f"""
            SELECT 
                *
            FROM
                exercise_type et
        """
    )

def update_exersise(exersise_id: int, name: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
                UPDATE 
                    exercise
                SET 
                    title = %s
                WHERE id = %s
            """
        , (name, exersise_id))

def create_exersise(theme_id: int, type_id: int, title: str):
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO exercise (theme_id, type_id, title) VALUES ({theme_id}, {type_id}, '{title}') RETURNING *"
        )
        return cur.fetchone()
    
def get_exersise_by_id(id: int):
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM exercise WHERE id = {id}")
        return cur.fetchone()
    
def update_exersise(id: int, data: dict = None, title: str = None):
    change_data_query = ''
    change_title_query = ''
    isAnd = ''

    if data:
        local_data = data.copy()
        key, value = local_data.popitem()
        change_data_query = f"another_data = jsonb_set(COALESCE(another_data, '{{}}')::jsonb, '{{{key}}}', '{json.dumps(value)}'::jsonb)"
    
    if title:
        change_title_query = f"title = '{title}'"

    if data and title:
        isAnd = "AND"

    with conn.cursor() as cur:
        cur.execute(
            f"""
                UPDATE 
                    exercise
                SET 
                    {change_data_query}
                    {isAnd}
                    {change_title_query}
                WHERE id = {id}
            """
        )