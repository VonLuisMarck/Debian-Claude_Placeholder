#!/bin/bash
# Ejecutar en la VM para arrancar el MCP server manualmente
set -e

cd /opt/claude-hub
source venv/bin/activate
exec python mcp_server.py
