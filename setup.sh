#!/bin/bash
set -e

echo "=== Claude Hub Setup ==="

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Dependencias del sistema
apt update && apt install -y \
    python3 python3-pip python3-venv \
    nodejs npm git curl openssh-server passwd

# Crear usuario dedicado
if ! id "claude-agent" &>/dev/null; then
    /usr/sbin/useradd -m -s /bin/bash claude-agent
    echo "Usuario claude-agent creado"
fi

# Directorio de trabajo
mkdir -p /opt/claude-hub
chown claude-agent:claude-agent /opt/claude-hub

# Entorno Python
cd /opt/claude-hub
python3 -m venv venv
source venv/bin/activate
pip install -r "$SCRIPT_DIR/requirements.txt"

# Instalar Claude Code
npm install -g @anthropic-ai/claude-code

# Copiar archivos del servidor
cp "$SCRIPT_DIR/mcp_server.py" /opt/claude-hub/mcp_server.py

# Configurar .env si no existe
if [ ! -f /opt/claude-hub/.env ]; then
    cp "$SCRIPT_DIR/.env.example" /opt/claude-hub/.env
    chmod 600 /opt/claude-hub/.env
    echo ""
    echo "IMPORTANTE: Edita /opt/claude-hub/.env y añade tu ANTHROPIC_API_KEY"
fi

echo ""
echo "=== Setup completado ==="
echo "Próximo paso: edita /opt/claude-hub/.env con tu API key"
echo "Luego ejecuta: bash start_mcp.sh"
