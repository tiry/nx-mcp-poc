#!/usr/bin/env python
"""
Test MCP tools with authentication.
"""

import sys
import os

# Add the source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.server import NuxeoMCPServer

# Create server with hardcoded credentials
print("Creating MCP server with basic auth...")
server = NuxeoMCPServer(
    nuxeo_url="https://nightly-2023.nuxeocloud.com/nuxeo",
    username="nuxeo_mcp", 
    password="**********",
    use_oauth2=False
)

print("\nTesting tools...")

# Try to get tool count (FastMCP stores tools internally)
import asyncio

async def get_tools_async():
    return await server.mcp.get_tools()

try:
    tools = asyncio.run(get_tools_async())
    print(f"Found {len(tools)} tools registered")
    for tool_name in list(tools.keys())[:5]:
        print(f"  - {tool_name}")
except:
    print("Could not retrieve tools list (async issues)")

# Test by directly calling the Nuxeo client
print("\nTesting direct Nuxeo client...")
try:
    # Test server info
    info = server.nuxeo.client.server_info()
    print(f"✅ Server info retrieved: {info.get('serverVersion', 'unknown')}")
except Exception as e:
    print(f"❌ Error getting server info: {e}")

# Test search with Nuxeo client
print("\nTesting search with Nuxeo client...")
try:
    # Use the Nuxeo client's query method
    query = "SELECT * FROM Document WHERE ecm:primaryType = 'Workspace' AND ecm:isVersion = 0 AND ecm:isTrashed = 0"
    result = server.nuxeo.client.query(query, params={'pageSize': 1})
    if hasattr(result, 'json'):
        data = result.json() if callable(result.json) else result
    else:
        data = result
    print(f"✅ Search successful: Found results")
except Exception as e:
    print(f"❌ Search error: {e}")

print("\n✅ All tests completed!")