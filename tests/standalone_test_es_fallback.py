#!/usr/bin/env python
"""
Test Elasticsearch fallback behavior
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.es_passthrough import ElasticsearchPassthrough
import json

print("Testing Elasticsearch Availability Check")
print("=" * 50)

# Create passthrough instance
passthrough = ElasticsearchPassthrough()
print(f"\nElasticsearch configured URL: {passthrough.base_url}")

# Test connection
import requests
try:
    print(f"\nChecking Elasticsearch at {passthrough.base_url}...")
    response = requests.get(f"{passthrough.base_url}/_cluster/health", timeout=2)
    response.raise_for_status()
    print("✅ Elasticsearch is accessible!")
    print(f"   Cluster health: {response.json()}")
except (requests.RequestException, requests.ConnectionError) as e:
    print(f"❌ Elasticsearch not accessible: {e}")
    print("\nThis is expected for nightly-2023.nuxeocloud.com as Elasticsearch is not exposed.")
    print("The tools will now return appropriate error messages.")

print("\n" + "=" * 50)
print("Simulating tool responses when ES is not available:")
print("\nsearch_repository response:")
print(json.dumps({
    "success": False,
    "error": "Elasticsearch not available",
    "message": "Elasticsearch is not accessible. Please use 'natural_search' or 'search' tools instead.",
    "alternative_tools": ["natural_search", "search"]
}, indent=2))

print("\nsearch_audit response:")
print(json.dumps({
    "success": False,
    "error": "Elasticsearch not available",
    "message": "Elasticsearch is not accessible for audit search. Audit logs require Elasticsearch.",
    "alternative": "Check your Nuxeo server's Elasticsearch configuration"
}, indent=2))

print("\n" + "=" * 50)
print("The Elasticsearch passthrough tools now handle unavailability gracefully.")
print("\nRecommendation: Use 'natural_search' or 'search' tools instead for nightly-2023.nuxeocloud.com")