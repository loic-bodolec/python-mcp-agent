from os import devnull
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


class MCPToolClient:
    def __init__(self, server_script: Path | None = None):
        self.server_script = (server_script or Path(__file__).with_name("server.py")).resolve()
        self._exit_stack = AsyncExitStack()
        self.session: ClientSession | None = None
        self.tool_names: set[str] = set()

    async def connect(self) -> set[str]:
        errlog = self._exit_stack.enter_context(open(devnull, "w", encoding="utf-8"))
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(self.server_script)],
            cwd=str(self.server_script.parent.resolve()),
        )
        read_stream, write_stream = await self._exit_stack.enter_async_context(stdio_client(server_params, errlog=errlog))
        self.session = await self._exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await self.session.initialize()
        tools = await self.session.list_tools()
        self.tool_names = {tool.name for tool in tools.tools}
        return self.tool_names

    async def call_tool(self, name: str, arguments: dict[str, str]) -> str:
        if self.session is None:
            raise RuntimeError("La session MCP n'est pas initialisée.")
        if name not in self.tool_names:
            raise ValueError(f"Tool MCP indisponible: {name}")

        result = await self.session.call_tool(name, arguments)
        text_parts = [item.text for item in result.content if getattr(item, "type", None) == "text"]
        return "\n".join(text_parts).strip()

    async def aclose(self) -> None:
        await self._exit_stack.aclose()