from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import google.auth
from google.auth.transport.requests import Request


@dataclass(frozen=True)
class ADCInfo:
    project_id: Optional[str]
    quota_project_id: Optional[str]
    credential_type: str


def assert_adc_works(scopes: Optional[Sequence[str]] = None) -> ADCInfo:

    creds, project_id = google.auth.default(scopes=scopes)

    creds.refresh(Request())

    return ADCInfo(
        project_id=project_id,
        quota_project_id=getattr(creds, "quota_project_id", None),
        credential_type=creds.__class__.__name__,
    )