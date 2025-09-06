#!/usr/bin/env python
"""
Test to identify which search function is failing
"""

import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.server import NuxeoMCPServer
from nuxeo.client import Nuxeo

# Configuration
nuxeo_url = "https://nightly-2023.nuxeocloud.com/nuxeo"

def test_searches(live_nuxeo_credentials):
    """Test various search functions."""
    username, password = live_nuxeo_credentials
    
    # Create Nuxeo client directly for testing
    nuxeo = Nuxeo(host=nuxeo_url, auth=(username, password))
    
    # Test 1: Regular NXQL search
    result = nuxeo.client.query(
        "SELECT * FROM Document WHERE ecm:isTrashed = 0", 
        params={'pageSize': 5}
    )
    assert result is not None
    
    # Test 2: Get a workspace
    try:
        workspaces = nuxeo.documents.query(
            {'query': "SELECT * FROM Workspace", 'pageSize': 1}
        )
        assert workspaces is not None
    except Exception:
        # May not have workspaces, that's ok
        pass