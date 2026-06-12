import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from tool_services import get_time, get_weather

server = Server("weather-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Retourne la météo actuelle d'une ville",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Nom de la ville (ex: Paris, Londres)"}
                },
                "required": ["city"]
            },
        ),
        Tool(
            name="get_time",
            description="Retourne l'heure actuelle dans un fuseau horaire specifique",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "description": "Fuseau horaire (ex: Europe/Paris, America/New_York)"}
                },
                "required": ["timezone"]
            },
        ),
    ]

@server.call_tool()
async def call_tool(name, arguments):
    if name == "get_weather":
        city = arguments.get("city", "Paris")
        return [TextContent(type="text", text=get_weather(city))]

    if name == "get_time":
        timezone_str = arguments.get("timezone", "Europe/Paris")
        return [TextContent(type="text", text=get_time(timezone_str))]

    return [
        TextContent(
            type="text",
            text=f"Erreur: Outil '{name}' non pris en charge."
        )
    ]

async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())

if __name__ == "__main__":
    print("[INFO] MCP server start (stdio) - waiting for client...", file=sys.stderr)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Arrêt manuel attendu (Ctrl+C) quand le serveur stdio est lancé sans client MCP.
        pass