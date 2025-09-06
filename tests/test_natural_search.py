#!/usr/bin/env python
"""
Test the fixed natural_search functionality
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

print("Testing Natural Language Search")
print("=" * 50)

async def test_natural_search():
    # Create server
    server = NuxeoMCPServer(
        nuxeo_url=nuxeo_url,
        username=username,
        password=password,
        use_oauth2=False
    )
    
    # Test queries
    test_queries = [
        "find all documents",
        "show me pictures",
        "documents created today",
        "files in workspaces"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        print("-" * 40)
        
        try:
            # Call the natural_search tool through MCP's internal call mechanism
            result = await server.mcp._call_tool(
                "natural_search",
                {
                    "query": query,
                    "page_size": 5
                }
            )
            
            print(f"✅ Query successful!")
            if result and len(result) > 0:
                print(f"   Found {len(result)} results")
                for i, doc in enumerate(result[:3], 1):
                    print(f"   {i}. {doc.get('title', 'Untitled')} ({doc.get('type', 'Unknown')})")
            else:
                print("   No results found")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

# Run the test
print("\nStarting natural search tests...")
asyncio.run(test_natural_search())

print("\n" + "=" * 50)
print("Natural search testing complete!")