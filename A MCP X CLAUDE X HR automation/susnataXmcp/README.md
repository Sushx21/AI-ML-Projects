CallLeaveManager MCP Server

This repository contains an MCP (Model Context Protocol) server designed for internal HR automation.
The server provides a simple leave management and employee tracking system, exposing multiple tools for integration with MCP-compatible clients.

Features

Retrieve employee performance and leave summaries

Apply for and revoke leaves with persistent storage

Query leave history for audit or reporting

Lightweight greeting resource for conversational contexts

All employee data is stored locally in employee_data.json and automatically updated whenever changes are made.

Run Instructions

From the project root directory, run:

uv run main.py


This starts the MCP server and registers all tools and resources.

MCP Configuration

Example mcp.json configuration:

{
    "mcpServers": {
        "susnata-agent": {
            "command": "C:\\Users\\Sushnato\\.local\\bin\\uv.exe",
            "args": [
                "--directory",
                "D:\\susnataXmcp",
                "run",
                "main.py"
            ]
        }
    }
}

Author

Developed and maintained by Susnata
For demonstration and experimentation with Model Context Protocol (MCP) integrations.