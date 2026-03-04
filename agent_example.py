"""
Ejemplo de cómo un agente local llama al MCP server en la VM.
El agente declara qué modelo quiere — el hub enruta automáticamente.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def ask_hub(prompt: str, model: str = "sonnet") -> str:
    """
    Envía un prompt al claude-hub por SSH tunnel.
    model: "opus" para razonamiento complejo, "sonnet" para equilibrio calidad-velocidad.
    """
    server_params = StdioServerParameters(
        command="ssh",
        args=[
            "-i", "~/.ssh/claude_hub_key",
            "-T",
            "claude-agent@<IP_VM>",
            "cd /opt/claude-hub && source venv/bin/activate && python mcp_server.py"
        ]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "ask_claude",
                {"prompt": prompt, "model": model}
            )
            return result.content[0].text


async def main():
    # Agente de razonamiento — usa Opus
    respuesta_compleja = await ask_hub(
        prompt="Diseña la arquitectura de un sistema de caché distribuida.",
        model="opus"
    )
    print("=== Opus ===")
    print(respuesta_compleja)

    # Agente de código — usa Sonnet
    respuesta_codigo = await ask_hub(
        prompt="Escribe una función Python para paginar resultados de una lista.",
        model="sonnet"
    )
    print("\n=== Sonnet ===")
    print(respuesta_codigo)


if __name__ == "__main__":
    asyncio.run(main())
