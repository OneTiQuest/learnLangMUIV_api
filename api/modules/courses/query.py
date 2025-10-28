from app.database import sql


def get_courses():
    return sql(f"SELECT id, name, code FROM courses")