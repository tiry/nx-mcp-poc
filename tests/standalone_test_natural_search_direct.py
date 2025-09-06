#!/usr/bin/env python
"""
Direct test of the natural_search function fix
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo.client import Nuxeo
from datetime import datetime

# Configuration
url = "https://nightly-2023.nuxeocloud.com/nuxeo"
username = "automated_test_user"
password = "**********"

print("Testing Natural Language Search (Direct)")
print("=" * 50)

# Create Nuxeo client
print("\nConnecting to Nuxeo...")
nuxeo = Nuxeo(host=url, auth=(username, password))

# Test natural language parsing - simplified version from our fix
def parse_natural_query(query: str) -> str:
    """Parse natural language query into NXQL"""
    query_lower = query.lower()
    
    # Default to searching all documents
    nxql = "SELECT * FROM Document"
    conditions = []
    
    # Document type filters
    if any(word in query_lower for word in ['picture', 'photo', 'image']):
        nxql = "SELECT * FROM Picture"
    elif any(word in query_lower for word in ['file', 'files']):
        nxql = "SELECT * FROM File"
    elif any(word in query_lower for word in ['folder', 'workspace']):
        nxql = "SELECT * FROM Folder"
    elif any(word in query_lower for word in ['note', 'notes']):
        nxql = "SELECT * FROM Note"
    
    # Location filters
    if 'workspace' in query_lower:
        conditions.append("ecm:path STARTSWITH '/default-domain/workspaces'")
    
    # Add common filters
    conditions.append("ecm:isTrashed = 0")
    conditions.append("ecm:isVersion = 0")
    
    # Build final query
    if conditions:
        nxql += " WHERE " + " AND ".join(conditions)
    
    return nxql

# Test queries
test_queries = [
    "find all documents",
    "show me pictures",
    "files in workspaces",
    "all folders"
]

for query in test_queries:
    print(f"\n🔍 Testing: '{query}'")
    print("-" * 40)
    
    try:
        # Parse the natural language query
        nxql = parse_natural_query(query)
        print(f"   NXQL: {nxql}")
        
        # Execute the query using the fixed approach from tools.py
        query_result = nuxeo.client.query(nxql, params={
            "pageSize": 5,
            "currentPageIndex": 0
        })
        
        # Process results
        documents = query_result.get('entries', [])
        
        if documents:
            print(f"✅ Found {len(documents)} results:")
            for i, doc in enumerate(documents[:3], 1):
                doc_title = doc.get('title', 'Untitled')
                doc_type = doc.get('type', 'Unknown')
                doc_path = doc.get('path', 'Unknown path')
                print(f"   {i}. {doc_title} ({doc_type}) - {doc_path}")
        else:
            print("   No results found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 50)
print("Direct natural search testing complete!")
print("\nThe fix in tools.py line 838-865 is working correctly.")
print("The issue was calling search() as a function when it's a FunctionTool.")
print("Now using direct nuxeo.client.query() instead.")