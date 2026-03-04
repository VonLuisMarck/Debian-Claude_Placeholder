#!/bin/bash
# Ejecutar en tu máquina LOCAL (no en la VM)
set -e

VM_IP="${1:-}"
if [ -z "$VM_IP" ]; then
    echo "Uso: bash setup_ssh_key.sh <IP_VM>"
    exit 1
fi

KEY_FILE="$HOME/.ssh/claude_hub_key"

# Generar clave si no existe
if [ ! -f "$KEY_FILE" ]; then
    ssh-keygen -t ed25519 -f "$KEY_FILE" -C "claude-hub-agent" -N ""
    echo "Clave generada: $KEY_FILE"
fi

# Copiar clave pública a la VM
ssh-copy-id -i "${KEY_FILE}.pub" "claude-agent@${VM_IP}"

echo ""
echo "=== SSH key configurada ==="
echo "Prueba la conexión con:"
echo "  ssh -i $KEY_FILE claude-agent@$VM_IP"
