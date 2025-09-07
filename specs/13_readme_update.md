# Documentation Update

This specification outlines the updates to the documentation for the Nuxeo MCP project.

## Overview

We will split the documentation into three files:

1. **README.md**: General documentation
2. **DEVELOPER.md**: Documentation on how to build, run tests, and extend the project
3. **USAGE.md**: Documentation on how to use the MCP Server

We will also add GitHub badges for the build/tests and integration tests workflows, and add instructions to use `@modelcontextprotocol/inspector` in the `USAGE.md` file.

## README.md

The `README.md` file will contain general information about the project, including:

- Project name and description
- Features
- Installation
- Quick start
- Links to other documentation files
- License information
- GitHub badges for the build/tests and integration tests workflows

## DEVELOPER.md

The `DEVELOPER.md` file will contain information for developers who want to build, run tests, and extend the project, including:

- Setting up the development environment
- Building the project
- Running tests
- Project structure
- Contributing guidelines
- Code style and conventions

## USAGE.md

The `USAGE.md` file will contain information for users who want to use the MCP Server, including:

- Configuration
- Available tools and resources
- Examples
- Troubleshooting
- Instructions to use `@modelcontextprotocol/inspector`

## GitHub Badges

We will add GitHub badges for the build/tests and integration tests workflows to the `README.md` file. These badges will show the status of the workflows and link to the GitHub Actions page.

## Implementation Details

### README.md

```markdown
# Nuxeo MCP Server

![Build and Unit Tests](https://github.com/tiry/nx-mcp-poc/actions/workflows/build-and-unit-tests.yml/badge.svg)
![Integration Tests](https://github.com/tiry/nx-mcp-poc/actions/workflows/integration-tests.yml/badge.svg)

A Model Context Protocol (MCP) server for Nuxeo Content Repository.

## Features

- Connect to a Nuxeo Content Repository
- Query and retrieve documents
- Execute operations
- Access document blobs and renditions
- Create, update, and delete documents

## Installation

```bash
pip install nuxeo-mcp
```

## Quick Start

```bash
# Start the MCP server
nuxeo-mcp
```

## Documentation

- [Developer Guide](DEVELOPER.md) - How to build, run tests, and extend the project
- [Usage Guide](USAGE.md) - How to use the MCP Server

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### DEVELOPER.md

```markdown
# Developer Guide

This guide provides information for developers who want to build, run tests, and extend the Nuxeo MCP Server.

## Setting Up the Development Environment

1. Clone the repository:

```bash
git clone https://github.com/tiry/nx-mcp-poc.git
cd nx-mcp
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Building the Project

```bash
python -m build
```

## Running Tests

### Unit Tests

```bash
python -m pytest tests/ -v --no-integration
```

### Integration Tests

Integration tests require a running Nuxeo server. You can use Docker to run a Nuxeo server:

```bash
# With standard Docker
python -m pytest tests/ -v --integration

# With Rancher Desktop
python -m pytest tests/ -v --integration --rancher

# With environment variable
USE_RANCHER=true python -m pytest tests/ -v --integration
```

## Project Structure

- `src/nuxeo_mcp/` - Source code
  - `server.py` - MCP server implementation
  - `tools.py` - MCP tools implementation
  - `resources.py` - MCP resources implementation
  - `utility.py` - Utility functions
- `tests/` - Tests
  - `test_basic.py` - Basic tests
  - `test_server.py` - Server tests
  - `test_integration.py` - Integration tests
  - `test_document_tools.py` - Document tools tests
  - `test_utility.py` - Utility tests
- `specs/` - Specifications

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## Code Style and Conventions

- We use [Black](https://black.readthedocs.io/) for code formatting
- We use [isort](https://pycqa.github.io/isort/) for import sorting
- We use [mypy](https://mypy.readthedocs.io/) for type checking
- We use [pytest](https://docs.pytest.org/) for testing
```

### USAGE.md

```markdown
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

## Available Tools

The Nuxeo MCP Server provides the following tools:

- `get_repository_info`: Get information about the Nuxeo repository
- `get_children`: Get the children of a document
- `search`: Search for documents
- `get_document`: Get a document by path or ID
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

result = use_tool("nuxeo", "get_document", {
    "path": "/default-domain/workspaces/My Workspace/My Document"
})
print(result)
```

## Troubleshooting

### Connection Issues

If you're having trouble connecting to the Nuxeo server, check the following:

- Make sure the Nuxeo server is running
- Check that the URL, username, and password are correct
- Check that the Nuxeo server is accessible from your machine

### Using the MCP Inspector

The MCP Inspector is a tool that helps you debug MCP servers. You can use it to inspect the tools and resources provided by the Nuxeo MCP Server.

To use the MCP Inspector:

1. Install the MCP Inspector:

```bash
npm install -g @modelcontextprotocol/inspector
```

2. Run the MCP Inspector with the Nuxeo MCP Server:

```bash
npx @modelcontextprotocol/inspector python -m nuxeo_mcp
```

3. The MCP Inspector will start a web server that you can access at http://localhost:3000

4. Use the MCP Inspector to explore the tools and resources provided by the Nuxeo MCP Server
