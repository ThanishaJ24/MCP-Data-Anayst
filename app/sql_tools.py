from app.database import get_connection

def run_sql(query):
    try:
        conn =get_connection()
        cursor=conn.cursor()
        cursor.execute(query)
        rows=cursor.fetchall()
        conn.close()

        return {
            "success":True,
            "data":[dict(row) for row in rows]
        }
    except Exception as e:
        return {
            "success":False,
            "error":str(e)
        }
def get_schema():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';"""
    )
    tables=cursor.fetchall()
    schema=""
    for table in tables:

        table_name = table[0]

        schema += f"\nTable: {table_name}\n"

        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = cursor.fetchall()

        for column in columns:

            schema += f"- {column[1]} ({column[2]})\n"

    conn.close()
    return schema