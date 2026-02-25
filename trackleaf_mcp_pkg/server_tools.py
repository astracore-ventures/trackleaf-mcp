from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


def create_server(client) -> Server:
    server = Server("trackleaf-cursor-mcp")

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="trackleaf_list_issues",
                description="List issues. If project_id is provided, lists project issues; else defaults to 'assigned to me'.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"},
                        "status": {"type": "string"},
                        "search": {"type": "string"},
                    },
                    "required": [],
                },
            ),
            Tool(
                name="trackleaf_get_issue",
                description="Get issue by internal id OR ticketKey (e.g., PROJ-123).",
                inputSchema={
                    "type": "object",
                    "properties": {"issue_ref": {"type": "string"}},
                    "required": ["issue_ref"],
                },
            ),
            Tool(
                name="trackleaf_create_issue",
                description="Create an issue.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "project_id": {"type": "string"},
                        "type": {"type": "string"},
                        "description": {"type": "string"},
                        "priority_id": {"type": "string"},
                        "status_id": {"type": "string"},
                        "assignee_id": {"type": "string"},
                    },
                    "required": ["title", "project_id", "type"],
                },
            ),
            Tool(
                name="trackleaf_update_issue_status",
                description="Update issue status by INTERNAL issue id.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_id": {"type": "string"},
                        "status_id": {"type": "string"},
                        "comment": {"type": "string"},
                    },
                    "required": ["issue_id", "status_id"],
                },
            ),
            Tool(
                name="trackleaf_add_comment",
                description="Add a comment to an issue by INTERNAL issue id.",
                inputSchema={
                    "type": "object",
                    "properties": {"issue_id": {"type": "string"}, "body": {"type": "string"}},
                    "required": ["issue_id", "body"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        try:
            if name == "trackleaf_list_issues":
                data = client.list_issues(
                    project_id=arguments.get("project_id"),
                    status=arguments.get("status"),
                    search=arguments.get("search"),
                )
                return [TextContent(type="text", text=server.to_json(data))]

            if name == "trackleaf_get_issue":
                data = client.get_issue(arguments["issue_ref"])
                return [TextContent(type="text", text=server.to_json(data))]

            if name == "trackleaf_create_issue":
                data = client.create_issue(
                    title=arguments["title"],
                    project_id=arguments["project_id"],
                    type_=arguments["type"],
                    description=arguments.get("description"),
                    priority_id=arguments.get("priority_id"),
                    status_id=arguments.get("status_id"),
                    assignee_id=arguments.get("assignee_id"),
                )
                return [TextContent(type="text", text=server.to_json(data))]

            if name == "trackleaf_update_issue_status":
                data = client.update_issue(
                    issue_id=arguments["issue_id"],
                    status_id=arguments["status_id"],
                    comment=arguments.get("comment"),
                )
                return [TextContent(type="text", text=server.to_json(data))]

            if name == "trackleaf_add_comment":
                data = client.add_comment(arguments["issue_id"], arguments["body"])
                return [TextContent(type="text", text=server.to_json(data))]

            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as e:
            # Normalize exceptions into text responses for the MCP
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    # Attach a convenience helper so callers can format JSON consistently.
    def to_json(obj: Any) -> str:
        import json

        return json.dumps(obj, indent=2, ensure_ascii=False)

    server.to_json = to_json

    return server
