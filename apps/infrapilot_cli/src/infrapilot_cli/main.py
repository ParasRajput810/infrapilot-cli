import typer

from infrapilot_cli.commands.scan import scan_app

app = typer.Typer(help="InfraPilot - FinOps + SRE Autopilot.")
app.add_typer(scan_app, name="scan")

if __name__ == "__main__":
    app()