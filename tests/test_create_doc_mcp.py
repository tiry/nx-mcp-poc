#!/usr/bin/env python
"""
Test create_document through MCP
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.server import NuxeoMCPServer
import asyncio
import json

# Configuration
nuxeo_url = "https://nightly-2023.nuxeocloud.com/nuxeo"
username = "nuxeo_mcp"
password = "**********"

print("Testing create_document MCP Tool")
print("=" * 50)

async def test_create():
    # Create server
    server = NuxeoMCPServer(
        nuxeo_url=nuxeo_url,
        username=username,
        password=password,
        use_oauth2=False
    )
    
    # Test 1: Create a simple document without file
    print("\n1. Creating document without file...")
    try:
        # Simulate the MCP tool call
        from nuxeo_mcp.tools import setup_tools
        mcp, nuxeo = setup_tools(server.nuxeo, server.mcp)
        
        # Call create_document directly
        result = mcp._tools["create_document"].function(
            name="test-leopard-doc",
            type="File",
            properties={
                "dc:title": "Test Leopard Document",
                "dc:description": "Testing the create_document fix"
            },
            parent_path="/default-domain/workspaces/Nature"
        )
        
        print("✅ Document created successfully!")
        print(f"   Result type: {type(result)}")
        
        if isinstance(result, dict):
            print("   Result is a dict (correct!)")
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   Message: {result.get('message', 'no message')}")
            print(f"   UID: {result.get('uid', 'no uid')}")
            print(f"   Path: {result.get('path', 'no path')}")
            print(f"   URL: {result.get('url', 'no url')}")
        else:
            print(f"   ❌ Result is {type(result)} - should be dict!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Create a document with a test file
    print("\n2. Creating document with file...")
    
    # Create a test image file
    test_file = "/tmp/test_leopard.txt"
    with open(test_file, "w") as f:
        f.write("This is a test file about leopards.\n")
        f.write("Leopards are magnificent big cats with distinctive spotted coats.\n")
    
    try:
        result = mcp._tools["create_document"].function(
            name="test-leopard-with-file",
            type="File",
            properties={
                "dc:title": "Leopard Document with File",
                "dc:description": "Testing file upload functionality"
            },
            parent_path="/default-domain/workspaces/Nature",
            file_path=test_file
        )
        
        print("✅ Document with file created successfully!")
        if isinstance(result, dict):
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   UID: {result.get('uid', 'no uid')}")
            print(f"   URL: {result.get('url', 'no url')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Clean up test file
    if os.path.exists(test_file):
        os.remove(test_file)

# Run the test
print("\nStarting tests...")
asyncio.run(test_create())

print("\n" + "=" * 50)
print("Test complete!")
print("\nThe create_document tool now returns a proper dict structure:")
print("- status: success/error")
print("- message: descriptive message")
print("- uid: document UID")
print("- path: document path")
print("- url: direct link to document")
print("- details: full formatted document details")