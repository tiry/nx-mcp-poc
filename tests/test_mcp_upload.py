#!/usr/bin/env python
"""
Test MCP create_document with file upload
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.server import NuxeoMCPServer
import asyncio

# Create server
print("Creating MCP server...")
server = NuxeoMCPServer(
    nuxeo_url="https://nightly-2023.nuxeocloud.com/nuxeo",
    username="nuxeo_mcp",
    password="**********",
    use_oauth2=False
)

print("Getting tools...")
async def test_upload():
    tools = await server.mcp.get_tools()
    
    if 'create_document' in tools:
        print("\nTesting create_document with file upload...")
        
        # Test with the test image
        test_file = "/tmp/test_image.png"
        if os.path.exists(test_file):
            print(f"Using test file: {test_file}")
            
            # Call the tool through MCP's call_tool method
            result = await server.mcp._call_tool(
                "create_document",
                {
                    "name": "mcp-upload-test",
                    "type": "Picture",
                    "properties": {
                        "dc:title": "MCP Upload Test",
                        "dc:description": "Testing file upload via MCP"
                    },
                    "parent_path": "/default-domain/workspaces",
                    "file_path": test_file
                }
            )
            
            print("✅ Upload successful!")
            print(f"Result: {result}")
        else:
            print(f"❌ Test file not found: {test_file}")
    else:
        print("❌ create_document tool not found")

# Run the test
asyncio.run(test_upload())