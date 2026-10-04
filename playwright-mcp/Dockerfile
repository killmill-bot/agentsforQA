FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir "mcp<2" playwright

RUN playwright install --with-deps chromium

COPY playwright_mcpwith_Docker.py .

ENV PLAYWRIGHT_HEADLESS=true
ENV MCP_TRANSPORT=stdio

CMD ["python", "playwright_mcpwith_Docker.py"]