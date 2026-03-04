import asyncio
import os
from dotenv import load_dotenv
import anthropic
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

load_dotenv("/opt/claude-hub/.env")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

ALLOWED_MODELS = {
    "opus":   "claude-opus-4-5",
    "sonnet": "claude-sonnet-4-5",
}

app = Server("claude-hub")


@app.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="ask_claude",
            description="Envía un mensaje a Claude. El agente declara qué modelo usar.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt":     {"type": "string", "description": "El mensaje al modelo"},
                    "model":      {"type": "string", "enum": ["opus", "sonnet"], "description": "Modelo a usar"},
                    "max_tokens": {"type": "integer", "default": 4096},
                },
                "required": ["prompt", "model"]
            }
        ),
        types.Tool(
            name="list_models",
            description="Lista los modelos disponibles",
            inputSchema={"type": "object", "properties": {}}
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "list_models":
        return [types.TextContent(type="text", text=str(ALLOWED_MODELS))]

    if name == "ask_claude":
        model_key  = arguments.get("model", "sonnet")
        model_id   = ALLOWED_MODELS.get(model_key, ALLOWED_MODELS["sonnet"])
        prompt     = arguments["prompt"]
        max_tokens = arguments.get("max_tokens", 4096)

        response = client.messages.create(
            model=model_id,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return [types.TextContent(type="text", text=response.content[0].text)]


async def main():
    async with stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
