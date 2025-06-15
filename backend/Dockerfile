FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY todo_backend/ todo_backend/
COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --locked
RUN uv pip install .

ENV APP_HOSTNAME=0.0.0.0
ENV APP_PORT=8000

CMD ["uv", "run", "todo_backend/server.py"]