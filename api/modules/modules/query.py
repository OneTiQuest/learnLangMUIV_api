from app.database import sql, sql_one

def update_module(module_id: int, name: str):
    return sql_one(
        f"""
            UPDATE 
                modules 
            SET 
                name = %s
            WHERE 
                id = %s
            RETURNING *
        """, 
        (name, module_id)
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
        (name, lang_id)
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
        (module_id,)
    )

def create_theme(module_id: int, name: str):
    sql(
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
        (
            name, 
            module_id
        )
    )
