# Debian-Claude Hub

VM Debian centralizada con Claude Code y un MCP server orquestador. Tus agentes locales se conectan por SSH tunnel y delegan las llamadas a la API de Anthropic — las keys nunca salen de la VM.

## Arquitectura

```
Tu app local (agentes)
        │
        │  SSH Tunnel (stdio)
        ▼
  VM Debian (/opt/claude-hub)
  ┌─────────────────────────────────┐
  │  MCP Server (orquestador)       │
  │    ├── router: lee "model" tag  │
  │    ├── claude-opus-4-5          │
  │    └── claude-sonnet-4-5        │
  │                                 │
  │  Claude Code (agente coding)    │
  │                                 │
  │  .env → ANTHROPIC_API_KEY       │
  └─────────────────────────────────┘
```

**Flujo:**
1. Tu agente llama al tool `ask_claude` declarando `model: "opus"` o `"sonnet"`
2. El MCP server recibe la llamada por el tunnel SSH
3. Enruta al modelo correcto usando la API key centralizada
4. Devuelve la respuesta al agente

## Setup

### 1. Preparar la VM Debian

```bash
# Clonar el repo en la VM
git clone https://github.com/TU_USUARIO/Debian-Claude_Placeholder.git
cd Debian-Claude_Placeholder

# Ejecutar el setup (instala dependencias, crea usuario, configura /opt/claude-hub)
bash setup.sh

# Añadir tu API key
nano /opt/claude-hub/.env
```

### 2. Configurar SSH keys (en tu máquina local)

```bash
bash setup_ssh_key.sh <IP_DE_LA_VM>
```

### 3. Conectar tus agentes

Copia `mcp_config.example.json` a tu proyecto, reemplaza `<IP_VM>` con la IP real:

```json
{
  "mcpServers": {
    "claude-hub": {
      "command": "ssh",
      "args": ["-i", "~/.ssh/claude_hub_key", "-T", "claude-agent@<IP_VM>",
               "cd /opt/claude-hub && source venv/bin/activate && python mcp_server.py"]
    }
  }
}
```

### 4. Probar

```bash
python agent_example.py
```

## Modelos disponibles

| Alias   | Modelo                | Uso recomendado                      |
|---------|-----------------------|--------------------------------------|
| `opus`  | claude-opus-4-5       | Razonamiento complejo, análisis       |
| `sonnet`| claude-sonnet-4-5     | Equilibrio calidad-velocidad, código  |

## Seguridad

- La `ANTHROPIC_API_KEY` vive solo en `/opt/claude-hub/.env` (permisos `600`)
- Autenticación por SSH key, sin contraseñas
- El usuario `claude-agent` puede restringirse a ejecutar solo el MCP server:

```
# /etc/ssh/sshd_config
Match User claude-agent
    ForceCommand /opt/claude-hub/venv/bin/python /opt/claude-hub/mcp_server.py
    AllowTcpForwarding no
```
