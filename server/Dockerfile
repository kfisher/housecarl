# ----------------------------------------------------------------------
# Build Stage
# ----------------------------------------------------------------------
FROM python:3.14-slim AS build

# Copy the UV binary from the official image.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# UV optimizations for Docker deployment
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy project code and build the project.
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./
COPY README.md ./
RUN uv sync --frozen --no-dev

# ----------------------------------------------------------------------
# Production Stage
# ----------------------------------------------------------------------
FROM python:3.14-slim

WORKDIR /app

# Run the application as a non-root user.
RUN useradd -m lydia && chown -R lydia:lydia /app
USER lydia

# Copy the application from the build stage.
COPY --from=build --chown=lydia:lydia /app /app

# Update $PATH to include the application and configure python to not
# buffer output so that the application output is instantly written to
# the console.
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# May need to include "--proxy-headers" and "--forwarded-allow-ips '*'"
CMD ["fastapi", "run", "src/housecarl/main.py", "--host", "0.0.0.0", "--port", "8000"]

