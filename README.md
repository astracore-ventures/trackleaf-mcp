# trackleaf-cursor-mcp

Lightweight MCP (Model Context Protocol) implementation that exposes Trackleaf Cursor issue API over a stdio MCP server.

Quick links
- Entrypoint: [trackleaf_mcp.py](trackleaf_mcp.py)
- Package: trackleaf_mcp_pkg/
- Dockerfile: [Dockerfile](Dockerfile)

Requirements
- Python 3.11+
- Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Environment
- The server needs one required and one optional environment variable:
  - `TRACKLEAF_PAT` (Required) — personal access token with Cursor API permissions
  - `TRACKLEAF_BASE_URL` (Optional) — base URL of your Trackleaf instance (defaults to https://www.api.trackleaf.in/)

Run locally

Start the MCP using the included wrapper (it runs the stdio MCP server):

Windows (PowerShell):
```powershell
$env:TRACKLEAF_BASE_URL = "https://www.api.trackleaf.in/"
$env:TRACKLEAF_PAT = "sk_xxx"
python trackleaf_mcp.py
```

Linux / macOS:
```bash
export TRACKLEAF_BASE_URL=https://www.api.trackleaf.in/
export TRACKLEAF_PAT=sk_xxx
python trackleaf_mcp.py
```

Docker

Build the image locally:

```bash
docker build -t trackleaf-mcp:latest .
```

Run the container (pass env vars):

```bash
docker run --rm -e TRACKLEAF_BASE_URL=https://www.api.trackleaf.in/ -e TRACKLEAF_PAT=sk_xxx trackleaf-mcp:latest
```

Note: you mentioned pushing to Docker Hub later — this README omits push steps for now.

IDE integration (MCP configuration)
---------------------------------
This MCP implementation communicates over stdio. Most IDE integrations expect a small JSON file describing how to start the MCP process. Below are example `mcp.json` files and IDE-specific hints. Place the chosen `mcp.json` next to your project root or follow the IDE's instructions to point to it.

Common `mcp.json` (generic)

```json
{
  "name": "trackleaf-cursor-mcp",
  "version": "0.1.0",
  "description": "Trackleaf Cursor MCP (stdio)",
  "run": {
    "command": "python",
    "args": ["trackleaf_mcp.py"]
  },
  "stdio": true,
  "env": {
    "TRACKLEAF_BASE_URL": "https://www.api.trackleaf.in/",
    "TRACKLEAF_PAT": "<your_pat_here>"
  }
}
```

Cursor (PHEMIDE/Cursor-compatible editors)
- Cursor supports loading an MCP by pointing at an `mcp.json` file or by configuring a custom tool. Use the Common `mcp.json` above. Make sure Cursor is configured to run the `command` with `args` and to use stdio.

VS Code
- There are a few MCP-related extensions for VS Code (e.g., Cursor integration or other MCP clients). If your extension accepts an `mcp.json` file, use the Common `mcp.json` above.

If the extension requires explicit VS Code settings instead, add a small snippet to your workspace `settings.json` (example — adapt per extension):

```json
{
  "mcp.server": {
    "trackleaf-cursor-mcp": {
      "command": "python",
      "args": ["${workspaceFolder}/trackleaf_mcp.py"],
      "stdio": true,
      "env": {
        "TRACKLEAF_BASE_URL": "https://www.api.trackleaf.in/",
        "TRACKLEAF_PAT": "<your_pat_here>"
      }
    }
  }
}
```

Antigravity
- Antigravity-compatible clients that implement the MCP runner should be able to consume the Common `mcp.json`. Point the IDE to the file and ensure it launches the given `command` and `args` and uses stdio.

Notes on exact fields
- `command`: executable to run (e.g., `python`).
- `args`: arguments array; in this repo the wrapper is `trackleaf_mcp.py` which imports the modular package.
- `stdio`: set to `true` to indicate the agent uses stdio transport.
- `env`: environment values required by the server. For security, do not commit secrets to VCS — prefer to set them via your IDE run configuration or environment.

Troubleshooting
- Missing env vars: the process will raise `Missing required env var` if `TRACKLEAF_PAT` is not set.
- Dependency errors: ensure `requirements.txt` is installed in your environment (or in the Docker image).
- If an IDE fails to start the server, try running `python trackleaf_mcp.py` manually to confirm it starts without the IDE.

Development notes
- The modularized code is in `trackleaf_mcp_pkg/` with `runner.py`, `client.py`, `server_tools.py` and `utils.py`.

Contact / contribution
- Open issues or PRs against this repository. If you add support for a specific IDE integration (e.g., a VS Code extension configuration), please add an example under `docs/` and link it from this README.
# trackleaf-mcp
Official MCP server for Trackleaf 
