from mcp.server.fastmcp import FastMCP

from app.mcp_server.tools import (
    execute_sql,
    fetch_schema,
    fetch_tables,
    validate_sql,
    preview_table_data
)

mcp = FastMCP("Data Analyst MCP")


# -----------------------------------
# TOOL 1
# EXECUTE SQL
# -----------------------------------

@mcp.tool()
def query_database(query: str):

    """
    Execute SQL query on SQLite database
    """

    return execute_sql(query)


# -----------------------------------
# TOOL 2
# GET SCHEMA
# -----------------------------------

@mcp.tool()
def get_database_schema():

    """
    Return database schema
    """

    return fetch_schema()


# -----------------------------------
# TOOL 3
# LIST TABLES
# -----------------------------------

@mcp.tool()
def list_tables():

    """
    List all database tables
    """

    return fetch_tables()


# -----------------------------------
# TOOL 4
# VALIDATE SQL
# -----------------------------------

@mcp.tool()
def validate_sql_query(query: str):

    """
    Validate SQL query safety
    """

    return validate_sql(query)


# -----------------------------------
# TOOL 5
# PREVIEW TABLE
# -----------------------------------

@mcp.tool()
def preview_table(table_name: str):

    """
    Preview first few rows of table
    """

    return preview_table_data(table_name)


# -----------------------------------
# START MCP SERVER
# -----------------------------------

if __name__ == "__main__":

    mcp.run()