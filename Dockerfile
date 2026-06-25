# MCP server image for cloud deploy (Render). Tools-only server; no LLM, no secrets baked in.
# Role is chosen at runtime via MCP_ROLE (cop|thief); Render injects $PORT.
FROM python:3.10-slim

# uv is the only supported package manager (project rule).
RUN pip install --no-cache-dir uv

WORKDIR /app
COPY . .

# Install locked runtime deps (no dev tooling needed to serve MCP).
RUN uv sync --frozen --no-dev

# Render sets $PORT; the runner reads PORT + MCP_ROLE from the environment.
ENV MCP_ROLE=cop
CMD ["uv", "run", "python", "scripts/run_mcp_server.py"]
