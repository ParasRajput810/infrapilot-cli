.PHONY: cli-install cli-run

cli-install:
	pip install -e ./packages/infrapilot_common
	pip install -e ./apps/infrapilot_cli

cli-run:
	infrapilot --help


COMPOSE_FILE := docker/docker-compose.yml
SERVICE := infrapilot-cli

.PHONY: d-build d-run d-help d-scan

d-build:
	docker compose -f $(COMPOSE_FILE) build $(SERVICE)


d-run:
	docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) $(ARGS)

d-help:
	$(MAKE) d-run ARGS="--help"

d-scan:
	$(MAKE) d-run ARGS="scan run"