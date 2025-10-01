#!/usr/bin/env python3
"""
Outscraper MCP HTTP Server

HTTP server wrapper for Smithery deployment using FastMCP's streamable HTTP transport.
This properly implements the MCP protocol over HTTP with SSE support.
"""

import os
import logging
import uvicorn
from starlette.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("outscraper-mcp-http")

# Import the MCP server
from outscraper_mcp.server import mcp

def main():
    """Main entry point for HTTP server"""
    logger.info("Starting Outscraper MCP Server in HTTP mode...")

    # Get the Starlette app from FastMCP and add CORS middleware
    app = mcp.get_asgi_app()

    # Add CORS middleware with proper header exposure for MCP session management
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this more restrictively in production
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id", "mcp-protocol-version"],  # Allow client to read session ID
        max_age=86400,
    )

    # Use PORT environment variable (Smithery and cloud platforms typically set this)
    port = int(os.environ.get("PORT", 8000))

    logger.info(f"Server will listen on 0.0.0.0:{port}")
    logger.info(f"OUTSCRAPER_API_KEY configured: {'Yes' if os.getenv('OUTSCRAPER_API_KEY') else 'No'}")

    # Run the MCP server with HTTP transport using uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces for containerized deployment
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main() 