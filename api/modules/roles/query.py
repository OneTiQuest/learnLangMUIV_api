from app.database import sql, sql_one

def get_roles():
    return sql(f"SELECT id, name FROM roles")
