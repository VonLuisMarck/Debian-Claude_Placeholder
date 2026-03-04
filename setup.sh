#!/bin/bash
# Setup script for Claude Code on Debian
# Fixes SSL certificate issues and installs Claude Code

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ── 1. Root check ──────────────────────────────────────────────────────────────
if [ "$EUID" -ne 0 ]; then
    log_error "Please run as root: sudo bash setup.sh"
    exit 1
fi

# ── 2. Update CA certificates ──────────────────────────────────────────────────
log_info "Updating CA certificates..."
apt-get update -qq
apt-get install -y ca-certificates curl gnupg 2>/dev/null

update-ca-certificates --fresh
log_info "CA certificates updated."

# ── 3. Ensure Node.js is installed ─────────────────────────────────────────────
if ! command -v node &>/dev/null; then
    log_info "Node.js not found. Installing via NodeSource (LTS)..."

    mkdir -p /etc/apt/keyrings
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

    NODE_MAJOR=20
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] \
https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" \
        > /etc/apt/sources.list.d/nodesource.list

    apt-get update -qq
    apt-get install -y nodejs
    log_info "Node.js $(node --version) installed."
else
    log_info "Node.js already installed: $(node --version)"
fi

# ── 4. Fix npm SSL configuration ───────────────────────────────────────────────
log_info "Configuring npm SSL settings..."

# Point npm to the system CA bundle
npm config set cafile /etc/ssl/certs/ca-certificates.crt

# Export for the current session as well
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt

log_info "npm SSL configured."

# ── 5. Install Claude Code ─────────────────────────────────────────────────────
log_info "Installing @anthropic-ai/claude-code globally..."

npm install -g @anthropic-ai/claude-code

log_info "Claude Code installed: $(claude --version 2>/dev/null || echo 'check PATH')"

# ── 6. Persist NODE_EXTRA_CA_CERTS for all users ──────────────────────────────
ENV_FILE=/etc/environment
if ! grep -q "NODE_EXTRA_CA_CERTS" "$ENV_FILE" 2>/dev/null; then
    echo "NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt" >> "$ENV_FILE"
    log_info "NODE_EXTRA_CA_CERTS persisted in $ENV_FILE."
fi

echo ""
log_info "Setup complete!"
log_warn "Open a new terminal (or run: source /etc/environment) so the"
log_warn "NODE_EXTRA_CA_CERTS variable takes effect in your session."
echo ""
log_info "Then authenticate with:  claude"
