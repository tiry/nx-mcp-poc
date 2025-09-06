#!/usr/bin/env python
"""
Debug ES query building with print statements
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.nl_parser import ParsedQuery
from nuxeo_mcp.es_query_builder import ElasticsearchQueryBuilder
import json
import re

# Manually replicate the build_elasticsearch_query logic with debug output
def build_elasticsearch_query_debug(parsed, index="repository"):
    """Build Elasticsearch query from parsed natural language."""
    es_builder = ElasticsearchQueryBuilder()
    must_clauses = []
    filter_clauses = []
    
    print(f"Starting build_elasticsearch_query")
    print(f"  Parsed doc_type: {parsed.doc_type}")
    print(f"  Number of conditions: {len(parsed.conditions)}")
    
    # Handle document type
    if parsed.doc_type and parsed.doc_type != "Document":
        print(f"  Adding doc type filter for: {parsed.doc_type}")
        type_mapping = {
            "pdf": "File",
            "image": "Picture",
            "picture": "Picture",
            "video": "Video",
            "file": "File",
            "folder": "Folder",
            "workspace": "Workspace",
            "note": "Note",
        }
        nuxeo_type = type_mapping.get(parsed.doc_type.lower(), parsed.doc_type)
        must_clauses.append(es_builder.term("ecm:primaryType", nuxeo_type))
    else:
        print(f"  Skipping doc type (is Document or None)")
    
    # Handle conditions
    for i, condition in enumerate(parsed.conditions):
        print(f"\n  Processing condition {i+1}:")
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]
        
        print(f"    Field: {field}")
        print(f"    Operator: {operator}")
        print(f"    Value: {value}")
        
        # Clean value - remove quotes
        if isinstance(value, str):
            value = value.strip("'").strip('"')
            print(f"    Cleaned value: {value}")
        
        # Map to appropriate Elasticsearch query
        if field in ["dc:created", "dc:modified"]:
            print(f"    Processing as date field")
            # Handle DATE format strings
            if "DATE '" in condition["value"]:  # Check original value
                print(f"    Found DATE format in original value")
                # Extract the date from DATE 'YYYY-MM-DD' format
                date_match = re.search(r"DATE '(\d{4}-\d{2}-\d{2})'", condition["value"])
                if date_match:
                    date_str = date_match.group(1)
                    print(f"    Extracted date: {date_str}")
                    if operator == ">=":
                        range_clause = es_builder.range(field, gte=date_str)
                        print(f"    Adding range clause: {range_clause}")
                        filter_clauses.append(range_clause)
                    elif operator == "<":
                        filter_clauses.append(es_builder.range(field, lt=date_str))
                    elif operator == "<=":
                        filter_clauses.append(es_builder.range(field, lte=date_str))
                    else:
                        filter_clauses.append(es_builder.range(field, gte=date_str))
                    print(f"    Added filter clause, continuing to next condition")
                    continue
                else:
                    print(f"    No date match found")
    
    print(f"\nFinal clauses:")
    print(f"  Must clauses: {len(must_clauses)}")
    print(f"  Filter clauses: {len(filter_clauses)}")
    
    # Build final query
    if not must_clauses and not filter_clauses:
        print("  No clauses - returning match_all")
        return {"match_all": {}}
    elif must_clauses and not filter_clauses:
        print("  Only must clauses")
        if len(must_clauses) == 1:
            return must_clauses[0]
        else:
            return es_builder.bool_query(must=must_clauses)
    elif filter_clauses and not must_clauses:
        print("  Only filter clauses")
        if len(filter_clauses) == 1:
            return filter_clauses[0]
        else:
            return es_builder.bool_query(filter=filter_clauses)
    else:
        print("  Both must and filter clauses")
        return es_builder.bool_query(must=must_clauses, filter=filter_clauses)

# Test
parsed = ParsedQuery(
    intent="search",
    doc_type="Document",
    conditions=[
        {"field": "dc:modified", "operator": ">=", "value": "DATE '2025-08-22'"}
    ]
)

print("=" * 50)
result = build_elasticsearch_query_debug(parsed, "nuxeo")
print("\nFinal ES query:")
print(json.dumps(result, indent=2))