# Usage Guide

This guide provides information for users who want to use the Nuxeo MCP Server.

## Configuration

The Nuxeo MCP Server can be configured using a configuration file or environment variables.

### Configuration File

Create a file named `nuxeo_mcp_config.json` with the following content:

```json
{
  "nuxeo_url": "http://localhost:8080/nuxeo",
  "username": "Administrator",
  "password": "Administrator"
}
```

### Environment Variables

You can also configure the Nuxeo MCP Server using environment variables:

```bash
export NUXEO_URL=http://localhost:8080/nuxeo
export NUXEO_USERNAME=Administrator
export NUXEO_PASSWORD=Administrator
```

## Running the Server

You can run the MCP server using one of the following methods:

```bash
# Using the entry point script
nuxeo-mcp

# Or directly with Python module
python -m nuxeo_mcp

# Or from the source directory
python -m src.nuxeo_mcp.server
```

## Available Tools

The Nuxeo MCP Server provides the following tools:

- `get_repository_info`: Get information about the Nuxeo repository
- `get_children`: Get the children of a document
- `search`: Search for documents
- `get_document`: Get a document by path or ID, with options for blob and renditions
- `create_document`: Create a new document
- `update_document`: Update an existing document
- `delete_document`: Delete a document

## Available Resources

The Nuxeo MCP Server provides the following resources:

- `nuxeo://info`: Basic information about the connected Nuxeo server
- `nuxeo://document/{path}`: Get a document by path
- `nuxeo://document/id/{uid}`: Get a document by ID

## Examples

### Get Repository Information

```python
from fastmcp import use_tool

result = use_tool("nuxeo", "get_repository_info", {})
print(result)
```

### Search for Documents

```python
from fastmcp import use_tool

result = use_tool("nuxeo", "search", {
    "query": "SELECT * FROM Document WHERE ecm:primaryType = 'File'",
    "pageSize": 10,
    "currentPageIndex": 0
})
print(result)
```

### Get a Document

```python
from fastmcp import use_tool

# Get document metadata
result = use_tool("nuxeo", "get_document", {
    "path": "/default-domain/workspaces/My Workspace/My Document"
})
print(result)

# Get document blob
blob = use_tool("nuxeo", "get_document", {
    "path": "/default-domain/workspaces/My Workspace/My Document",
    "blob": True
})

# Get document thumbnail
thumbnail = use_tool("nuxeo", "get_document", {
    "path": "/default-domain/workspaces/My Workspace/My Document",
    "rendition": "thumbnail"
})
```

### Create a Document

```python
from fastmcp import use_tool

result = use_tool("nuxeo", "create_document", {
    "parent_path": "/default-domain/workspaces/My Workspace",
    "name": "My New Document",
    "type": "File",
    "properties": {
        "dc:title": "My New Document",
        "dc:description": "This is a new document"
    }
})
print(result)
```

### Update a Document

```python
from fastmcp import use_tool

result = use_tool("nuxeo", "update_document", {
    "path": "/default-domain/workspaces/My Workspace/My Document",
    "properties": {
        "dc:title": "Updated Title",
        "dc:description": "This document has been updated"
    }
})
print(result)
```

### Delete a Document

```python
from fastmcp import use_tool

result = use_tool("nuxeo", "delete_document", {
    "path": "/default-domain/workspaces/My Workspace/My Document"
})
print(result)
```

## Configuring with Cline

To use the Nuxeo MCP server with Cline, you need to add a configuration to your Cline MCP settings file. Here's an example configuration:

```json
{
  "mcpServers": {
    "nuxeo": {
      "command": "python",
      "args": ["-m", "nuxeo_mcp"]
    }
  }
}
```

For more detailed examples, see the [Nuxeo MCP Server Configuration Examples](./nuxeo_mcp_config.md).

## Troubleshooting

### Connection Issues

If you're having trouble connecting to the Nuxeo server, check the following:

- Make sure the Nuxeo server is running
- Check that the URL, username, and password are correct
- Check that the Nuxeo server is accessible from your machine

### Authentication Issues

If you're having authentication issues, check the following:

- Make sure the username and password are correct
- Check that the user has the necessary permissions
- Try using the Nuxeo web interface to verify your credentials

### Using the MCP Inspector

The MCP Inspector is a tool that helps you debug MCP servers. You can use it to inspect the tools and resources provided by the Nuxeo MCP Server.

To use the MCP Inspector:

1. Install the MCP Inspector:

```bash
npm install -g @modelcontextprotocol/inspector
```

2. Run the MCP Inspector with the Nuxeo MCP Server using the provided configuration file:

```bash
DANGEROUSLY_OMIT_AUTH=true npx @modelcontextprotocol/inspector \
  --config mcp.json \
  --server default
```

Note: The `DANGEROUSLY_OMIT_AUTH=true` flag is used to bypass authentication for local testing. Do not use this in production environments.

3. The MCP Inspector will start a web server that you can access at http://localhost:6277

4. Use the MCP Inspector to explore the tools and resources provided by the Nuxeo MCP Server:
   - View available tools and their input schemas
   - Test tools with different inputs
   - View available resources and their content
   - Monitor requests and responses

The MCP Inspector is particularly useful for:
- Understanding the capabilities of the Nuxeo MCP Server
- Testing tools with different inputs
- Debugging issues with tools and resources
- Learning how to use the Nuxeo MCP Server effectively

### Common Errors

#### "Cannot connect to Nuxeo server"

This error occurs when the MCP server cannot connect to the Nuxeo server. Check that the Nuxeo server is running and that the URL is correct.

#### "Authentication failed"

This error occurs when the MCP server cannot authenticate with the Nuxeo server. Check that the username and password are correct.

#### "Document not found"

This error occurs when the MCP server cannot find a document at the specified path or with the specified ID. Check that the path or ID is correct.

## Best Practices

### Error Handling

Always handle errors when using the Nuxeo MCP Server. Tools and resources may return errors if there are issues with the Nuxeo server or with the input parameters.

```python
from fastmcp import use_tool

try:
    result = use_tool("nuxeo", "get_document", {
        "path": "/default-domain/workspaces/My Workspace/My Document"
    })
    print(result)
except Exception as e:
    print(f"Error: {e}")
```

### Performance Considerations

- Use the `pageSize` and `currentPageIndex` parameters when searching for documents to limit the number of results returned
- Use the `schemas` parameter when getting documents to limit the properties returned
- Use the `enrichers` parameter when getting documents to include additional information
