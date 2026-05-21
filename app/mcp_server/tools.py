from app.sql_tools import (
    run_sql,
    get_schema
)

from app.database import get_connection


# -----------------------------------
# EXECUTE SQL
# -----------------------------------

def execute_sql(query: str):

    return run_sql(query)


# -----------------------------------
# GET SCHEMA
# -----------------------------------

def fetch_schema():

    return get_schema()


# -----------------------------------
# LIST TABLES
# -----------------------------------

def fetch_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table';
    """)

    tables = cursor.fetchall()

    conn.close()

    return [table[0] for table in tables]


# -----------------------------------
# VALIDATE SQL
# -----------------------------------

def validate_sql(query: str):

    dangerous = [
        "DROP",
        "DELETE",
        "TRUNCATE",
        "ALTER"
    ]

    upper_query = query.upper()

    for word in dangerous:

        if word in upper_query:

            return {
                "safe": False,
                "reason": f"{word} operation not allowed"
            }

    return {
        "safe": True
    }


# -----------------------------------
# PREVIEW TABLE
# -----------------------------------

def preview_table_data(table_name: str):

    query = f"""
    SELECT *
    FROM {table_name}
    LIMIT 5
    """

    return run_sql(query)