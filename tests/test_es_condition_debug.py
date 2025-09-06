#!/usr/bin/env python
"""
Debug ES condition processing
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.nl_parser import NaturalLanguageParser, ParsedQuery
from nuxeo_mcp.es_query_builder import ElasticsearchQueryBuilder
import json

print("Testing Condition Processing in ES Query Builder")
print("=" * 50)

# Create a simple parsed query with date condition
parsed = ParsedQuery(
    intent="search",
    doc_type="Document",
    conditions=[
        {"field": "dc:modified", "operator": ">=", "value": "DATE '2025-08-22'"}
    ]
)

print("Input parsed query:")
print(f"  Doc type: {parsed.doc_type}")
print(f"  Conditions: {parsed.conditions}")

# Build ES query
parser = NaturalLanguageParser()
es_query = parser.build_elasticsearch_query(parsed, "nuxeo")

print("\nGenerated ES query:")
print(json.dumps(es_query, indent=2))

print("\n" + "-" * 50)
print("Expected ES query should include date range filter...")

# Manual build to show what we expect
es_builder = ElasticsearchQueryBuilder()
expected = es_builder.bool_query(
    filter=[
        es_builder.range("dc:modified", gte="2025-08-22")
    ]
)

print("\nExpected query structure:")
print(json.dumps(expected, indent=2))