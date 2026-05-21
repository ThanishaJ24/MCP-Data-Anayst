import pandas as pd
from app.database import get_connection

def process_file(file_path, table_name):

    # Read file
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    else:
        raise Exception("Unsupported file")
    

    conn=get_connection()

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    return{
        "message": "File stored successfully",
        "rows": len(df),
        "columns": list(df.columns)
    }