import asyncio
import os
import sys
from typing import Optional

from mcp.server.stdio import stdio_server

from .utils import env, to_json
from .client import TrackleafCursorClient
from .server_tools import create_server


def main(argv: Optional[list[str]] = None) -> int:
    base_url = os.environ.get("TRACKLEAF_BASE_URL", "https://www.api.trackleaf.in/")
    pat = env("TRACKLEAF_PAT")

    client = TrackleafCursorClient(base_url=base_url, pat=pat)
    server = create_server(client)

    async def runner() -> None:
        async with stdio_server() as (read_stream, write_stream):
            # Some versions require initialization options, others don't.
            if hasattr(server, "create_initialization_options"):
                init_opts = server.create_initialization_options()
                await server.run(read_stream, write_stream, init_opts)
            else:
                await server.run(read_stream, write_stream)

    try:
        asyncio.run(runner())
        return 0
    except Exception as e:
        print(f"[trackleaf-cursor-mcp] fatal: {e}", file=sys.stderr)
        return 2
