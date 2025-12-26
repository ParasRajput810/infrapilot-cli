from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ScanConfig(BaseModel):
    project_id: Optional[str] = Field(default=None, description="Default GCP project id")
    time_range: str = Field(default="last_7_days", description="Scan time range preset or ISO range")
    output_dir: str = Field(default="./out", description="Where scan outputs are written")


class AppConfig(BaseModel):
    scan: ScanConfig = Field(default_factory=ScanConfig)