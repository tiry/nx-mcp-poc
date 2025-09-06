# Multi-Server Support for Nuxeo MCP

## Overview
The Nuxeo MCP now supports connecting to multiple Nuxeo servers and switching between them seamlessly. Server configurations and the active server context are persisted, so you only need to configure servers once.

## Features

### 1. **Persistent Server Storage**
- Server configurations are stored in `~/.nuxeo-mcp/servers.json`
- Active server context is stored in `~/.nuxeo-mcp/context.json`
- Configurations persist between MCP sessions

### 2. **Default Servers**
Two servers are pre-configured:
- **demo**: Demo Nuxeo Server at `https://nightly-2023.nuxeocloud.com/nuxeo`
- **local**: Local Development Server at `http://localhost:8080/nuxeo`

### 3. **Server Management Tools**
The MCP provides several tools for managing servers:

#### `list_servers`
Lists all configured Nuxeo servers and shows which one is active.

#### `get_current_server`
Shows detailed information about the currently active server.

#### `switch_server`
Switch to a different Nuxeo server.
```
switch_server(server_name="demo")
```

#### `add_server`
Add a new Nuxeo server configuration.
```
add_server(
    name="production",
    url="https://nuxeo.company.com/nuxeo",
    username="admin",
    password="secret",
    description="Production Nuxeo Server",
    set_as_active=True
)
```

#### `remove_server`
Remove a server configuration.
```
remove_server(name="old-server")
```

## Usage Examples

### Example 1: Working with Multiple Servers

```python
# List available servers
list_servers()
# Output: Shows demo, local, and any custom servers

# Check current server
get_current_server()
# Output: Shows details of active server

# Switch to demo server
switch_server("demo")

# Create a document on demo server
create_document(
    name="demo-doc",
    type="File",
    properties={"dc:title": "Demo Document"},
    parent_path="/default-domain/workspaces"
)

# Switch to local server
switch_server("local")

# Create a document on local server
create_document(
    name="local-doc",
    type="File",
    properties={"dc:title": "Local Document"},
    parent_path="/default-domain/workspaces"
)
```

### Example 2: Adding a Production Server

```python
# Add production server
add_server(
    name="prod",
    url="https://nuxeo.company.com/nuxeo",
    username="service_account",
    password="secure_password",
    description="Production Nuxeo Instance",
    set_as_active=True
)

# Now all operations will use the production server
search(query="SELECT * FROM Document WHERE dc:creator = 'john'")
```

### Example 3: Context Persistence

```python
# Session 1: Configure and use a server
switch_server("demo")
create_document(...)

# Session 2: Automatically uses the last active server (demo)
# No need to switch again - context is remembered
search(query="SELECT * FROM File")
```

## Architecture

### ServerManager Class
The `ServerManager` class handles:
- Loading/saving server configurations
- Managing active server context
- Server connection testing
- Default server initialization

### ServerConfig Class
Each server is represented by a `ServerConfig` object containing:
- `name`: Unique identifier for the server
- `url`: Full URL to the Nuxeo instance
- `username`: Authentication username
- `password`: Authentication password
- `description`: Human-readable description
- `is_default`: Whether this is a default server

### NuxeoClientContainer
The tools use a `NuxeoClientContainer` that:
- Wraps the Nuxeo client
- Allows dynamic server switching
- Maintains connection state
- Tests connections before switching

## File Locations

Configuration files are stored in the user's home directory:
- `~/.nuxeo-mcp/servers.json` - Server configurations
- `~/.nuxeo-mcp/context.json` - Active server context

Example `servers.json`:
```json
{
  "servers": {
    "demo": {
      "name": "demo",
      "url": "https://nightly-2023.nuxeocloud.com/nuxeo",
      "username": "automated_test_user",
      "password": "**********",
      "description": "Demo Nuxeo Server",
      "is_default": true
    },
    "local": {
      "name": "local",
      "url": "http://localhost:8080/nuxeo",
      "username": "Administrator",
      "password": "Administrator",
      "description": "Local Development Server",
      "is_default": false
    }
  }
}
```

Example `context.json`:
```json
{
  "active_server": "demo"
}
```

## Benefits

1. **No Repeated Configuration**: Configure servers once, use them forever
2. **Quick Switching**: Change servers with a single command
3. **Context Preservation**: The MCP remembers your last active server
4. **Multiple Environments**: Easily work with dev, staging, and production
5. **Team Collaboration**: Share server configurations (without passwords)

## Security Considerations

- Passwords are stored in plain text in the configuration file
- The configuration file has standard file system permissions
- For production use, consider:
  - Using environment variables for sensitive credentials
  - Implementing OAuth2 authentication (already supported by the MCP)
  - Using a secrets management system
  - Restricting file permissions on `~/.nuxeo-mcp/`

## Troubleshooting

### Server Connection Failed
If switching servers fails:
1. Verify the server URL is correct
2. Check username and password
3. Ensure the server is accessible from your network
4. Test with `curl` or browser: `curl -u username:password https://server/nuxeo/api/v1/me`

### Configuration Not Persisting
If settings don't persist:
1. Check file permissions on `~/.nuxeo-mcp/`
2. Ensure the directory is writable
3. Check for disk space issues

### Wrong Server Being Used
If operations use the wrong server:
1. Run `get_current_server()` to verify active server
2. Use `switch_server()` to change to the correct one
3. Check `~/.nuxeo-mcp/context.json` for the active server

## Future Enhancements

Potential improvements for multi-server support:
- Encrypted password storage
- Server groups/tags for organization
- Connection pooling for better performance
- Automatic failover between servers
- Server health checks
- Import/export of server configurations
- Per-server operation history