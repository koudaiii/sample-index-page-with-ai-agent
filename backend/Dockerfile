FROM python:3.12-slim AS production

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Create non-root user
RUN addgroup --gid 1001 --system app && \
    adduser --uid 1001 --system --group app

# Create uv cache directory for the app user
RUN mkdir -p /app/.cache/uv && chown -R app:app /app/.cache/uv
ENV UV_CACHE_DIR=/app/.cache/uv

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock* ./

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD uv run python -c "import requests; requests.get('http://localhost:8000/health')"

# Start FastAPI server for production
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
