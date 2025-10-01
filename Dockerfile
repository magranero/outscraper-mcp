FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv for fast package management
RUN pip install --no-cache-dir uv

# Copy all necessary files
COPY pyproject.toml README.md LICENSE ./
COPY outscraper_mcp/ ./outscraper_mcp/

# Install the package and dependencies directly into system Python
# This avoids runtime overhead of uv run
RUN uv pip install --system --no-cache -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port (Smithery will set PORT env var, defaults to 8000)
EXPOSE 8000

# Run the server directly with Python (dependencies already installed)
CMD ["python", "-m", "outscraper_mcp.server_http"]
