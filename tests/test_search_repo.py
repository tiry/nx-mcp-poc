#!/usr/bin/env python
"""
Test to identify which search function is failing
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.server import NuxeoMCPServer
import asyncio

# Configuration
nuxeo_url = "https://nightly-2023.nuxeocloud.com/nuxeo"
username = "nuxeo_mcp"
password = "**********"

print("Testing Search Functions")
print("=" * 50)

async def test_searches():
    # Create server
    server = NuxeoMCPServer(
        nuxeo_url=nuxeo_url,
        username=username,
        password=password,
        use_oauth2=False
    )
    
    print("\n1. Testing regular search tool...")
    try:
        result = await server.mcp._call_tool(
            "search",
            {
                "query": "SELECT * FROM Document WHERE ecm:isTrashed = 0",
                "pageSize": 5
            }
        )
        print(f"✅ Regular search works! Found {len(result.get('entries', []))} results")
    except Exception as e:
        print(f"❌ Regular search error: {e}")
    
    print("\n2. Testing natural_search tool...")
    try:
        result = await server.mcp._call_tool(
            "natural_search",
            {
                "query": "find all documents",
                "page_size": 5
            }
        )
        print(f"✅ Natural search works! Found results")
    except Exception as e:
        print(f"❌ Natural search error: {e}")
    
    print("\n3. Testing search_repository tool (ES passthrough)...")
    try:
        result = await server.mcp._call_tool(
            "search_repository",
            {
                "query": "documents",
                "limit": 5
            }
        )
        print(f"✅ Search repository works!")
    except Exception as e:
        print(f"❌ Search repository error: {e}")
        print("   This is expected if Elasticsearch is not configured")

# Run the test
print("\nStarting tests...")
asyncio.run(test_searches())

print("\n" + "=" * 50)
print("Test complete!")