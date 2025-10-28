from app.database import sql, sql_one

def get_langs():
    return sql(
        f"""
            SELECT 
                id, 
                name, 
                short_name 
            FROM 
                langs
        """
    )
