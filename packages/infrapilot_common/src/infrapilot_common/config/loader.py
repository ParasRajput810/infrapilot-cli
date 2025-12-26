from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from infrapilot_common.config.models import AppConfig


DEFAULT_FILENAMES = [
    Path("infrapilot.yaml"),
    Path.home() / ".config" / "infrapilot" / "infrapilot.yaml",
]


def load_config(path: Optional[Path] = None) -> AppConfig:
    if path is not None:
        data = _read_yaml(path)
        return AppConfig.model_validate(data)

    for candidate in DEFAULT_FILENAMES:
        if candidate.exists():
            data = _read_yaml(candidate)
            return AppConfig.model_validate(data)

    return AppConfig()


def _read_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError("Config YAML must be a mapping/dictionary at the top level.")
    return data