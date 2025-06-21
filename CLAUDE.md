# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Testing:**
```bash
pytest                              # Run all tests
pytest tests/test_server.py         # Run specific test file
pytest -v                          # Verbose output
pytest tests/test_integration.py    # Integration tests
```

**Linting and Code Quality:**
```bash
black outscraper_mcp/              # Format code
flake8 outscraper_mcp/              # Lint code  
mypy outscraper_mcp/                # Type checking
```

**Package Management:**
```bash
uv sync                             # Install dependencies
uv add <package>                    # Add new dependency
uv pip install -e .                    # Install in development mode
```

**Running the Server:**
```bash
# Development with FastMCP inspector
fastmcp dev outscraper_mcp/server.py

# Production (stdio transport)
python -m outscraper_mcp
outscraper-mcp                      # Via entry point

# HTTP transport for testing
python -c "from outscraper_mcp import mcp; mcp.run(transport='streamable-http', host='127.0.0.1', port=8000)"
```

## Architecture

**MCP Server Structure:**
- Built using FastMCP framework for simplified MCP server development
- Two main tools: `google_maps_search` and `google_maps_reviews`
- Outscraper API client with retry logic and error handling
- Supports both synchronous and asynchronous API operations

**Key Components:**
- `outscraper_mcp/server.py` - Main MCP server implementation with tools
- `outscraper_mcp/__init__.py` - Package entry point and main() function  
- `OutscraperClient` class - Handles API communication with retry logic
- Tool validation and response formatting for optimal Claude integration

**API Integration:**
- Uses Outscraper API v3 endpoints (`/maps/search-v3`, `/maps/reviews-v3`)
- Automatic async handling for large requests (>10 queries, >499 reviews)
- Request retry strategy for robust API communication
- Environment variable `OUTSCRAPER_API_KEY` required for operation

**Response Handling:**
- Structured formatting for Claude consumption
- Async request detection and appropriate messaging
- Error handling with specific messages for common failure scenarios
- Request validation with defined limits and constants

**Deployment:**
- Smithery.ai compatible with HTTP server support
- Docker containerized deployment via `Dockerfile`
- Both PyPI distribution and local development installation supported