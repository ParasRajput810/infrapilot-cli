from __future__ import annotations

import re

_PROJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")


def validate_project_id(project_id: str) -> None:
    if not project_id or not project_id.strip():
        raise ValueError("project_id is required (provide --project or set scan.project_id in config).")
    if not _PROJECT_ID_RE.match(project_id):
        raise ValueError("Invalid GCP project_id format. Expected something like 'my-project-123'.")