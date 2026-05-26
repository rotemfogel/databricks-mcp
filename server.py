import os
from typing import Any

from databricks import sql
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("databricks-unity-catalog")


def _connect():
    return sql.connect(
        server_hostname=os.environ["DATABRICKS_SERVER_HOSTNAME"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        access_token=os.environ["DATABRICKS_TOKEN"],
    )


def _rows_to_dicts(cursor) -> list[dict[str, Any]]:
    columns = [c[0] for c in cursor.description or []]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def _execute(sql_text: str) -> list[dict[str, Any]]:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_text)
            return _rows_to_dicts(cur)


@mcp.tool()
def query_sql(sql_text: str, max_rows: int = 100) -> dict[str, Any]:
    """
    Run a Databricks SQL query against Unity Catalog.

    Examples:
    SHOW CATALOGS
    SHOW SCHEMAS IN main
    SHOW TABLES IN main.default
    SHOW CREATE TABLE main.default.t1
    DESCRIBE EXTENDED main.default.t1
    """
    if max_rows < 1 or max_rows > 1000:
        raise ValueError("max_rows must be between 1 and 1000")

    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_text)
            rows = cur.fetchmany(max_rows)
            columns = [c[0] for c in cur.description or []]

    return {
        "columns": columns,
        "rows": [dict(zip(columns, row)) for row in rows],
        "row_count_returned": len(rows),
    }


@mcp.tool()
def show_create_table(table_name: str) -> dict[str, Any]:
    """
    Return SHOW CREATE TABLE output for a Unity Catalog table.

    Use a fully qualified name when possible:
    catalog.schema.table
    """
    sql_text = f"SHOW CREATE TABLE {table_name}"
    rows = _execute(sql_text)
    return {"table": table_name, "result": rows}


@mcp.tool()
def describe_extended(table_name: str) -> dict[str, Any]:
    """
    Return DESCRIBE EXTENDED output for a Unity Catalog table.

    Use a fully qualified name when possible:
    catalog.schema.table
    """
    sql_text = f"DESCRIBE EXTENDED {table_name}"
    rows = _execute(sql_text)
    return {"table": table_name, "result": rows}


@mcp.tool()
def list_tables(catalog: str, schema: str) -> dict[str, Any]:
    """List tables in a Unity Catalog schema."""
    sql_text = f"SHOW TABLES IN {catalog}.{schema}"
    rows = _execute(sql_text)
    return {"catalog": catalog, "schema": schema, "tables": rows}


if __name__ == "__main__":
    mcp.run()
