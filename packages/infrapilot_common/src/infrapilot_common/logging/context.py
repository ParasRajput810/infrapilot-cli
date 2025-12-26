from __future__ import annotations

import contextvars
from typing import Optional

_scan_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("scan_id", default=None)


def set_scan_id(scan_id: str) -> None:
    _scan_id_var.set(scan_id)


def get_scan_id() -> Optional[str]:
    return _scan_id_var.get()