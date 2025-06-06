FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including curl for health check
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN pip install uv

# Copy all necessary files for building
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY outscraper_mcp/ ./outscraper_mcp/

# Install dependencies and build the package
RUN uv sync --no-dev

# Expose port (Smithery will set PORT env var)
EXPOSE 8000

# Set the Python path to include the current directory
ENV PYTHONPATH=/app

# Add startup script
RUN echo '#!/bin/bash\necho "🐳 Container starting..."\necho "📝 Environment variables:"\necho "PORT=${PORT:-8000}"\necho "OUTSCRAPER_API_KEY=${OUTSCRAPER_API_KEY:-not_set}"\necho "🚀 Starting server..."\nexec uv run python outscraper_mcp/server_http.py' > /app/start.sh && chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run the server in HTTP mode
CMD ["/app/start.sh"] 