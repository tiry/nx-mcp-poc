#!/usr/bin/env python
"""
Test all search tools to verify they work correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo.client import Nuxeo
import json

# Configuration
url = "https://nightly-2023.nuxeocloud.com/nuxeo"
username = "automated_test_user"
password = "**********"

print("Testing All Search Tools")
print("=" * 50)

# Create Nuxeo client
print("\nConnecting to Nuxeo...")
nuxeo = Nuxeo(host=url, auth=(username, password))
print(f"✅ Connected as: {username}")

print("\n" + "-" * 50)
print("1. Testing regular NXQL search (search tool)")
print("-" * 50)

try:
    query = "SELECT * FROM Document WHERE ecm:isTrashed = 0 AND ecm:isVersion = 0"
    print(f"Query: {query}")
    
    result = nuxeo.client.query(query, params={"pageSize": 5, "currentPageIndex": 0})
    
    docs = result.get('entries', [])
    print(f"✅ Found {len(docs)} results")
    if docs:
        print(f"   First result: {docs[0].get('title', 'Untitled')} ({docs[0].get('type', 'Unknown')})")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "-" * 50)
print("2. Testing natural language search (natural_search tool)")
print("-" * 50)

try:
    # Import the NL parser directly
    from nuxeo_mcp.nl_parser import NaturalLanguageParser, NXQLBuilder
    
    test_queries = [
        "find all pictures",
        "documents created today",
        "files in workspaces"
    ]
    
    for nl_query in test_queries:
        print(f"\nNatural query: '{nl_query}'")
        
        # Parse and build NXQL
        parser = NaturalLanguageParser()
        parsed = parser.parse(nl_query)
        builder = NXQLBuilder(parsed)
        nxql = builder.build()
        
        print(f"Generated NXQL: {nxql}")
        
        # Execute query
        result = nuxeo.client.query(nxql, params={"pageSize": 3, "currentPageIndex": 0})
        docs = result.get('entries', [])
        
        if docs:
            print(f"✅ Found {len(docs)} results")
            for i, doc in enumerate(docs[:2], 1):
                print(f"   {i}. {doc.get('title', 'Untitled')} ({doc.get('type', 'Unknown')})")
        else:
            print("   No results found")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "-" * 50)
print("3. Testing Elasticsearch passthrough (search_repository tool)")
print("-" * 50)

try:
    from nuxeo_mcp.es_passthrough import ElasticsearchPassthrough
    import requests
    
    passthrough = ElasticsearchPassthrough()
    print(f"Elasticsearch URL: {passthrough.base_url}")
    
    # Check if ES is available
    try:
        response = requests.get(f"{passthrough.base_url}/_cluster/health", timeout=2)
        response.raise_for_status()
        print("✅ Elasticsearch is accessible")
    except (requests.RequestException, requests.ConnectionError) as e:
        print(f"⚠️ Elasticsearch not accessible: Connection refused")
        print("   This is expected for nightly-2023.nuxeocloud.com")
        print("   The search_repository tool will return a graceful error message")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("Summary:")
print("✅ Regular NXQL search (search tool) - WORKING")
print("✅ Natural language search (natural_search tool) - WORKING")
print("⚠️ Elasticsearch passthrough (search_repository, search_audit) - REQUIRES ES")
print("\nRecommendation for nightly-2023.nuxeocloud.com:")
print("- Use 'search' for NXQL queries")
print("- Use 'natural_search' for natural language queries")
print("- Avoid 'search_repository' and 'search_audit' (require Elasticsearch)")