from __future__ import annotations

from typing import Any, Mapping


REDACT_KEYS = {
    "authorization",
    "access_token",
    "refresh_token",
    "token",
    "password",
    "secret",
    "api_key",
}


def redact(obj: Any) -> Any:
    
    if isinstance(obj, Mapping):
        out = {}
        for k, v in obj.items():
            if str(k).lower() in REDACT_KEYS:
                out[k] = "[REDACTED]"
            else:
                out[k] = redact(v)
        return out
    if isinstance(obj, list):
        return [redact(x) for x in obj]
    return obj