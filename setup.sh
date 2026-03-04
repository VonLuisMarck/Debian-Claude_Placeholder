#!/bin/bash
# Setup script for Claude Hub on Debian
# Fixes SSL certificate issues and installs all dependencies

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "=== Claude Hub Setup ==="

# ── 1. Root check ──────────────────────────────────────────────────────────────
if [ "$EUID" -ne 0 ]; then
    log_error "Please run as root: sudo bash setup.sh"
    exit 1
fi

# ── 2. System dependencies ─────────────────────────────────────────────────────
log_info "Installing system dependencies..."
apt update && apt install -y \
    python3 python3-pip python3-venv \
    nodejs npm git curl openssh-server passwd \
    ca-certificates gnupg

# ── 3. Fix SSL certificates (resolves npm UNABLE_TO_GET_ISSUER_CERT_LOCALLY) ──
log_info "Configuring SSL certificates for npm..."
# apt install ca-certificates already regenerates the bundle via dpkg triggers.
# We just point npm to the system CA file.
npm config set cafile /etc/ssl/certs/ca-certificates.crt
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt

# Persist for all future sessions
ENV_FILE=/etc/environment
if ! grep -q "NODE_EXTRA_CA_CERTS" "$ENV_FILE" 2>/dev/null; then
    echo "NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt" >> "$ENV_FILE"
    log_info "NODE_EXTRA_CA_CERTS persisted in $ENV_FILE."
fi

# ── 4. Dedicated user ─────────────────────────────────────────────────────────
if ! id "claude-agent" &>/dev/null; then
    /usr/sbin/useradd -m -s /bin/bash claude-agent
    log_info "User claude-agent created."
fi

# ── 5. Working directory ───────────────────────────────────────────────────────
mkdir -p /opt/claude-hub
chown claude-agent:claude-agent /opt/claude-hub

# ── 6. Python virtual environment ─────────────────────────────────────────────
log_info "Setting up Python virtual environment..."
python3 -m venv /opt/claude-hub/venv
/opt/claude-hub/venv/bin/pip install -r /opt/Debian-Claude_Placeholder/requirements.txt

# ── 7. Install Claude Code (with SSL fix applied above) ───────────────────────
log_info "Installing @anthropic-ai/claude-code..."
npm install -g @anthropic-ai/claude-code

# ── 8. Copy server files ───────────────────────────────────────────────────────
cp /opt/Debian-Claude_Placeholder/mcp_server.py /opt/claude-hub/mcp_server.py

# ── 9. Configure .env ─────────────────────────────────────────────────────────
if [ ! -f /opt/claude-hub/.env ]; then
    cp /opt/Debian-Claude_Placeholder/.env.example /opt/claude-hub/.env
    chmod 600 /opt/claude-hub/.env
    echo ""
    log_warn "IMPORTANTE: Edita /opt/claude-hub/.env y añade tu ANTHROPIC_API_KEY"
fi

echo ""
echo "=== Setup completado ==="
log_info "Próximo paso: edita /opt/claude-hub/.env con tu API key"
log_info "Luego ejecuta: bash start_mcp.sh"
log_warn "Abre un nuevo terminal (o: source /etc/environment) para que NODE_EXTRA_CA_CERTS tome efecto."
