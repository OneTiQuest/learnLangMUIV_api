import psycopg2
from app.config import config

def get_db_connection():
    db_conf = config["DB"]
    conn = psycopg2.connect(
        database=db_conf.get("NAME"), 
        user=db_conf.get("USER"), 
        password=db_conf.get("PASSWORD"),
        host=db_conf.get("HOST"), 
        port=5432
    )
    conn.autocommit = True
    return conn

def sql(sql: str, params: tuple = None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
        
def sql_one(sql: str, params: tuple = None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()