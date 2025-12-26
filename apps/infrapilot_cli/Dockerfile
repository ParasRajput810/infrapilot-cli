FROM python:3.10-slim

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*


COPY apps/infrapilot_cli/pyproject.toml apps/infrapilot_cli/README.md /app/apps/infrapilot_cli/
COPY packages/infrapilot_common/pyproject.toml /app/packages/infrapilot_common/


COPY apps/infrapilot_cli/src /app/apps/infrapilot_cli/src
COPY packages/infrapilot_common/src /app/packages/infrapilot_common/src

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir /app/packages/infrapilot_common && \
    pip install --no-cache-dir /app/apps/infrapilot_cli

ENTRYPOINT ["infrapilot"]