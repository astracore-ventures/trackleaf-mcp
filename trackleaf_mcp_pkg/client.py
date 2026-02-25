from typing import Any, Dict, Optional
import requests


class TrackleafCursorClient:
    """Small HTTP client for Trackleaf Cursor API.

    Keeps a requests.Session and exposes thin methods used by the MCP.
    """

    def __init__(self, base_url: str, pat: str, timeout_s: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {pat}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "trackleaf-cursor-mcp/0.2",
        })

    def _url(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return f"{self.base_url}/api/v1/cursor{path}"

    def list_issues(self, project_id: Optional[str] = None, status: Optional[str] = None, search: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if project_id:
            params["projectId"] = project_id
        if status:
            params["status"] = status
        if search:
            params["search"] = search
        r = self.s.get(self._url("/issues"), params=params, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def get_issue(self, issue_ref: str) -> Dict[str, Any]:
        r = self.s.get(self._url(f"/issues/{issue_ref}"), timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def create_issue(
        self,
        title: str,
        project_id: str,
        type_: str,
        description: Optional[str] = None,
        priority_id: Optional[str] = None,
        status_id: Optional[str] = None,
        assignee_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {"title": title, "projectId": project_id, "type": type_}
        if description is not None:
            body["description"] = description
        if priority_id is not None:
            body["priorityId"] = priority_id
        if status_id is not None:
            body["statusId"] = status_id
        if assignee_id is not None:
            body["assigneeId"] = assignee_id

        r = self.s.post(self._url("/issues"), json=body, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def update_issue(self, issue_id: str, status_id: Optional[str] = None, comment: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if status_id is not None:
            body["statusId"] = status_id
        if comment is not None:
            body["comment"] = comment

        r = self.s.patch(self._url(f"/issues/{issue_id}"), json=body, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def add_comment(self, issue_id: str, body_text: str) -> Dict[str, Any]:
        body = {"body": body_text}
        r = self.s.post(self._url(f"/issues/{issue_id}/comments"), json=body, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()
