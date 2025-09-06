#!/usr/bin/env python
"""
Test all operation input types with proper Nuxeo automation API formatting
"""

import sys
import os
import pytest
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo.client import Nuxeo
from nuxeo.documents import Document
import json

# Configuration
url = "https://nightly-2023.nuxeocloud.com/nuxeo"

@pytest.fixture
def nuxeo_client(live_nuxeo_credentials):
    """Create Nuxeo client with prompted credentials."""
    username, password = live_nuxeo_credentials
    return Nuxeo(host=url, auth=(username, password))

# Test 1: Single Document Operation (Move)
def test_single_document(nuxeo_client):
    """Test single document operations with doc: prefix."""
    # Create test document
    doc = Document(
        name="test-single-doc",
        type="File",
        properties={"dc:title": "Single Document Test"}
    )
    
    # Add random suffix to avoid conflicts
    suffix = random.randint(1000000000, 9999999999)
    created = nuxeo_client.documents.create(doc, parent_path="/default-domain/workspaces")
    
    # Test Move operation
    operation = nuxeo_client.operations.new("Document.Move")
    operation.params = {
        "target": "/default-domain/workspaces",
        "name": f"test-dest.{suffix}"
    }
    operation.input_obj = f"doc:{created.uid}"  # Proper format
    
    result = operation.execute()
    assert result is not None
    assert 'path' in result or isinstance(result, Document)

# Test 2: Multiple Documents Operation
def test_multiple_documents(nuxeo_client):
    """Test operations on multiple documents with docs: prefix."""
    # Create test documents
    docs = []
    suffix = random.randint(1000000000, 9999999999)
    for i in range(3):
        doc = Document(
            name=f"test-multi-{i}.{suffix}",
            type="File",
            properties={"dc:title": f"Multi Doc {i}"}
        )
        created = nuxeo_client.documents.create(doc, parent_path="/default-domain/workspaces")
        docs.append(created.uid)
    
    # Test operation on multiple documents
    operation = nuxeo_client.operations.new("Document.Update")
    operation.params = {"properties": {"dc:description": "Batch updated"}}
    operation.input_obj = f"docs:{','.join(docs)}"  # Proper format for multiple
    
    result = operation.execute()
    assert result is not None

# Test 3: Document Path as Input
def test_document_path(nuxeo_client):
    """Test operations using document reference with doc: prefix."""
    # Create test document
    suffix = random.randint(1000000000, 9999999999)
    doc = Document(
        name=f"test-path-doc.{suffix}",
        type="File",
        properties={"dc:title": "Path Input Test"}
    )
    created = nuxeo_client.documents.create(doc, parent_path="/default-domain/workspaces")
    
    # Test operation using UID with Document.Fetch
    operation = nuxeo_client.operations.new("Document.Fetch")
    operation.params = {"value": created.uid}
    result = operation.execute()
    assert result is not None
    assert hasattr(result, 'uid') or 'uid' in result
    
    # Test operation using path with Document.Query
    operation2 = nuxeo_client.operations.new("Document.Query")
    operation2.params = {
        "query": f"SELECT * FROM Document WHERE ecm:path = '{created.path}'"
    }
    result2 = operation2.execute()
    assert result2 is not None

# Test 4: Void Operation (no input)
def test_void_operation(nuxeo_client):
    """Test operations that don't require input (void operations)."""
    # Test operation without input
    operation = nuxeo_client.operations.new("Repository.Query")
    operation.params = {
        "query": "SELECT * FROM Document WHERE ecm:primaryType = 'File' ORDER BY dc:modified DESC",
        "pageSize": 5
    }
    # No input_obj set for void operations
    
    result = operation.execute()
    assert result is not None
    assert 'entries' in result or hasattr(result, 'entries')

# Test 5: Lifecycle Transition
def test_lifecycle_transition(nuxeo_client):
    """Test lifecycle transition operations."""
    # Create test document
    suffix = random.randint(1000000000, 9999999999)
    doc = Document(
        name=f"test-lifecycle.{suffix}",
        type="File",
        properties={"dc:title": "Lifecycle Test"}
    )
    created = nuxeo_client.documents.create(doc, parent_path="/default-domain/workspaces")
    
    # Follow lifecycle transition
    operation = nuxeo_client.operations.new("Document.FollowLifecycleTransition")
    operation.params = {"value": "approve"}
    operation.input_obj = f"doc:{created.uid}"  # Proper format
    
    # Some transitions may not be available, but operation should execute
    result = operation.execute()
    assert result is not None

# Test 6: Copy Document
def test_copy_document(nuxeo_client):
    """Test document copy operations."""
    # Create source document
    suffix = random.randint(1000000000, 9999999999)
    doc = Document(
        name=f"test-copy-source.{suffix}",
        type="File",
        properties={"dc:title": "Document to Copy"}
    )
    created = nuxeo_client.documents.create(doc, parent_path="/default-domain/workspaces")
    
    # Copy document
    operation = nuxeo_client.operations.new("Document.Copy")
    operation.params = {
        "target": "/default-domain/workspaces",
        "name": f"test-copy-dest.{suffix}"
    }
    operation.input_obj = f"doc:{created.uid}"  # Proper format
    
    result = operation.execute()
    assert result is not None