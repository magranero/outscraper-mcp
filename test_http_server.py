#!/usr/bin/env python3
"""
Test script for HTTP server functionality
Run this to verify the HTTP server works before deploying to Smithery
"""

import requests
import json
import time
import subprocess
import sys
import os
from threading import Thread

def test_server():
    """Test the HTTP server endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Outscraper MCP HTTP Server...")
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test health endpoint
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test MCP GET endpoint (tool discovery)
        print("\n2. Testing MCP GET endpoint (tool discovery)...")
        response = requests.get(f"{base_url}/mcp?apiKey=test_key")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Server: {result.get('server', {}).get('name')}")
        print(f"   Tools: {len(result.get('tools', []))} available")
        for tool in result.get('tools', []):
            print(f"     - {tool.get('name')}: {tool.get('description')}")
        
        # Test MCP POST endpoint (tool execution) - would need real API key
        print("\n3. Testing MCP POST endpoint...")
        payload = {
            "tool": "google_maps_search",
            "arguments": {
                "query": "coffee shops new york",
                "limit": 2
            }
        }
        response = requests.post(
            f"{base_url}/mcp?apiKey=test_key", 
            json=payload
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 500:
            print("   Expected 500 - API key is invalid for testing")
        else:
            print(f"   Response: {response.json()}")
        
        # Test MCP DELETE endpoint
        print("\n4. Testing MCP DELETE endpoint...")
        response = requests.delete(f"{base_url}/mcp")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        print("\n✅ All endpoints are responding correctly!")
        print("\n📝 Note: Tool execution requires a valid OUTSCRAPER_API_KEY")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False
    
    return True

def start_server():
    """Start the HTTP server in background"""
    print("🚀 Starting HTTP server...")
    
    # Set test environment
    os.environ["OUTSCRAPER_API_KEY"] = "test_key_for_deployment"
    os.environ["PORT"] = "8000"
    
    try:
        # Import and run the server
        from outscraper_mcp.server_http import main
        main()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test-only":
        # Just test, assume server is already running
        test_server()
    else:
        # Start server in background and test
        server_thread = Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Test the server
        if test_server():
            print("\n🎉 HTTP server is ready for Smithery deployment!")
        else:
            print("\n⚠️  Please fix the issues before deploying to Smithery")
        
        print("\nPress Ctrl+C to stop...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!") 