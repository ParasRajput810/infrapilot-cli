from __future__ import annotations

import json
import logging

from infrapilot_common.logging.context import set_scan_id
from infrapilot_common.logging.setup import setup_logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4
from google.auth.exceptions import DefaultCredentialsError
from infrapilot_common.clients.gcp_auth import assert_adc_works

import typer
from rich.console import Console

from infrapilot_common.config.loader import load_config
from infrapilot_common.config.validation import validate_project_id

scan_app = typer.Typer(help="Run a project scan.")
console = Console()



@dataclass(frozen=True)
class StubScanResult:
    scan_id: str
    created_at: str
    project_id: str
    time_range: str
    status: str
    note: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not output_dir.is_dir():
        raise ValueError(f"output_dir is not a directory: {output_dir}")


@scan_app.command("run")
def run(
    project: Optional[str] = typer.Option(
        None, "--project", "-p", help="GCP project id to scan (overrides config)."
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Directory where scan outputs will be written (overrides config).",
    ),
    time_range: Optional[str] = typer.Option(
        None,
        "--time-range",
        "-t",
        help="Time range preset for the scan (overrides config). Example: last_7_days",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        help="Path to config file (YAML). If omitted, InfraPilot searches default locations.",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    ),
) -> None:
    
    setup_logging(level=log_level)
    logger = logging.getLogger("infrapilot.scan")

    try:
        cfg = load_config(config)

        effective_project = project or cfg.scan.project_id
        effective_output_dir = output_dir or Path(cfg.scan.output_dir)
        effective_time_range = time_range or cfg.scan.time_range

        validate_project_id(effective_project)
        _ensure_output_dir(effective_output_dir)

        adc_info = assert_adc_works(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        logger.info("adc_ok", extra={"adc": adc_info.__dict__})

        scan_id = f"scan_{uuid4().hex[:12]}"
        set_scan_id(scan_id)

        logger.info(
            "scan_started",
            extra={
                "project_id": effective_project,
                "time_range": str(effective_time_range),
                "output_dir": str(effective_output_dir),
            },
        )

        created_at = _utc_now_iso()
        result = StubScanResult(
            scan_id=scan_id,
            created_at=created_at,
            project_id=effective_project,
            time_range=str(effective_time_range),
            status="stub_success",
            note="US-1/US-2/US-3 stub scan output. No GCP calls performed.",
        )

        scan_dir = effective_output_dir / "scans" / scan_id
        scan_dir.mkdir(parents=True, exist_ok=True)

        out_file = scan_dir / "scan_result.json"
        out_file.write_text(json.dumps(asdict(result), indent=2) + "\n", encoding="utf-8")

        logger.info("scan_completed", extra={"output_file": str(out_file)})

        console.print("[green]Scan completed (stub).[/green]")
        console.print(f"Project:    {effective_project}")
        console.print(f"Time range: {effective_time_range}")
        console.print(f"Scan ID:    {scan_id}")
        console.print(f"Output:     {out_file}")

    except (ValueError, FileNotFoundError) as e:
        logger.error("scan_failed", extra={"error": str(e)}, exc_info=True)
        console.print(f"[red]ERROR:[/red] {e}")
        raise typer.Exit(code=2)
    except Exception as e:
        logger.error("scan_failed_unexpected", extra={"error": str(e)}, exc_info=True)
        console.print("[red]ERROR:[/red] Unexpected error. Re-run with --log-level DEBUG for details.")
        raise typer.Exit(code=1)
    except DefaultCredentialsError as e:
        logger.error("adc_missing", extra={"error": str(e)}, exc_info=True)
        console.print("[red]ERROR:[/red] GCP Application Default Credentials not found or invalid.")
        console.print("Fix: run [bold]gcloud auth application-default login[/bold]")
        raise typer.Exit(code=2)