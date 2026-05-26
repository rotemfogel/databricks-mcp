# databricks-mcp
An MCP server for using databricks query

## configure in claude
Edit your `.claude.json` file:
```
vi $HOME/.claude.json
```

Add the following section under `mcpServers`:
```
"databricks": {
  "command": "uv",
  "args": [
    "run",
    "--directory",
    "/<full-path-to-dir>/databricks-mcp",
    "python",
    "server.py"
  ],
  "env": {
    "DATABRICKS_SERVER_HOSTNAME": "<your-databricks-domain>",
    "DATABRICKS_HTTP_PATH": "/sql/1.0/warehouses/<warehouse-id>",
    "DATABRICKS_TOKEN": "<your-databricks-access-token>"
  }
}
```

Example:
```
"mcpServers": {
  "databricks": {
    "command": "uv",
    "args": [
      "run",
      "--directory",
      "/Users/user1/src/python/databricks-mcp",
      "python",
      "server.py"
    ],
    "env": {
      "DATABRICKS_SERVER_HOSTNAME": "data-engineering.cloud.databricks.com",
      "DATABRICKS_HTTP_PATH": "/sql/1.0/warehouses/6ab0d23fbabe290c",
      "DATABRICKS_TOKEN": "da..."
    }
  }
}
```
