# Nuxeo MCP Authentication Guide

## Overview

The Nuxeo MCP server now supports multiple authentication methods to securely connect to your Nuxeo instance:

1. **OAuth2 Authentication** (Recommended) - Browser-based authentication with secure token storage
2. **Basic Authentication** - Traditional username/password authentication
3. **JWT Authentication** (Coming soon) - Token-based authentication for service accounts

## OAuth2 Authentication

### Benefits

- 🔐 **Enhanced Security** - No need to store passwords, uses secure token exchange
- 🔄 **Automatic Token Refresh** - Tokens are refreshed automatically when they expire
- 🔑 **Secure Storage** - Tokens are stored in OS keychain (macOS Keychain, Windows Credential Manager, Linux Secret Service)
- 🌐 **Browser-Based** - Familiar login experience through your browser
- 🛡️ **PKCE Protection** - Uses Proof Key for Code Exchange for enhanced security

### Setup

#### 1. Configure OAuth2 Client in Nuxeo

First, register an OAuth2 client in your Nuxeo server:

1. Log in to your Nuxeo Web UI as an administrator
2. Navigate to **Administration** > **Cloud Services** > **Consumers** tab
3. Click **Add** to create a new OAuth2 consumer
4. Configure the client:
   - **Name**: `nuxeo-mcp`
   - **Client ID**: `nuxeo-mcp-client` (or your preferred ID)
   - **Client Secret**: Generate a secure secret
   - **Redirect URIs**: Add `http://localhost:*` to allow any local port
5. Click **Save**

#### 2. Configure Environment Variables

Set the following environment variables:

```bash
# Required OAuth2 configuration
export NUXEO_URL="https://your-nuxeo-instance.com/nuxeo"
export NUXEO_AUTH_METHOD="oauth2"
export NUXEO_OAUTH_CLIENT_ID="nuxeo-mcp-client"
export NUXEO_OAUTH_CLIENT_SECRET="your-client-secret"

# Optional: Specify a fixed callback port (default: auto-detect)
export NUXEO_OAUTH_REDIRECT_PORT="8888"

# Optional: Custom OAuth2 endpoints (if not using standard Nuxeo endpoints)
export NUXEO_OAUTH_AUTH_ENDPOINT="https://your-nuxeo-instance.com/nuxeo/oauth2/authorize"
export NUXEO_OAUTH_TOKEN_ENDPOINT="https://your-nuxeo-instance.com/nuxeo/oauth2/token"
```

#### 3. Start the MCP Server with OAuth2

```bash
# Start with OAuth2 authentication (browser will open automatically)
nuxeo-mcp --oauth2

# Start without opening browser (manual authentication)
nuxeo-mcp --oauth2 --no-browser

# Or use environment variable
NUXEO_AUTH_METHOD=oauth2 nuxeo-mcp
```

### Authentication Flow

1. When the MCP server starts with OAuth2 enabled, it will:
   - Check for existing valid tokens in secure storage
   - If no valid tokens found, open your default browser
   - Direct you to the Nuxeo login page

2. After successful login:
   - You'll be redirected to a local callback URL
   - The MCP server captures the authorization code
   - Exchanges it for access and refresh tokens
   - Stores tokens securely in your OS keychain
   - The browser window closes automatically

3. For subsequent connections:
   - Tokens are retrieved from secure storage
   - Automatically refreshed when needed
   - No browser interaction required

### Configuration File

You can also use a configuration file for persistent settings:

**Location:**
- macOS: `~/Library/Application Support/nuxeo-mcp/auth_config.json`
- Linux: `~/.config/nuxeo-mcp/auth_config.json`
- Windows: `%APPDATA%\nuxeo-mcp\auth_config.json`

**Example Configuration:**

```json
{
  "servers": {
    "production": {
      "url": "https://prod.nuxeo.com/nuxeo",
      "auth_method": "oauth2",
      "oauth2_config": {
        "client_id": "nuxeo-mcp-client",
        "client_secret": "***",
        "scope": "openid profile email"
      }
    },
    "staging": {
      "url": "https://staging.nuxeo.com/nuxeo",
      "auth_method": "oauth2",
      "oauth2_config": {
        "client_id": "nuxeo-mcp-client-staging",
        "client_secret": "***"
      }
    }
  },
  "default_server": "production",
  "enable_browser_auth": true,
  "token_storage_backend": "keyring"
}
```

**Note:** Client secrets are masked in the config file. Provide them via environment variables:
```bash
export NUXEO_OAUTH_CLIENT_SECRET_PRODUCTION="actual-secret"
export NUXEO_OAUTH_CLIENT_SECRET_STAGING="staging-secret"
```

## Basic Authentication

### Setup

Basic authentication is the default method and requires only username and password:

```bash
# Using environment variables
export NUXEO_URL="http://localhost:8080/nuxeo"
export NUXEO_USERNAME="Administrator"
export NUXEO_PASSWORD="Administrator"

# Start the server
nuxeo-mcp
```

Or pass directly when starting:

```bash
NUXEO_USERNAME="admin" NUXEO_PASSWORD="secret" nuxeo-mcp
```

### Security Considerations

⚠️ **Warning:** Basic authentication sends credentials with every request. Use OAuth2 for production environments.

## Token Storage

### Secure Storage Backends

1. **OS Keychain** (Default)
   - macOS: Keychain Access
   - Windows: Credential Manager
   - Linux: Secret Service (gnome-keyring, KWallet)

2. **Encrypted File** (Fallback)
   - Used when keychain is unavailable
   - Stored in user's data directory
   - Encrypted with user-specific key
   - File permissions set to owner-only (600)

### Managing Stored Tokens

To clear stored tokens:

```python
from nuxeo_mcp.token_store import TokenManager

# Clear all tokens
token_manager = TokenManager()
token_manager.clear_all_tokens()

# Clear tokens for specific server
token_manager.delete_token("https://prod.nuxeo.com/nuxeo")
```

## Troubleshooting

### OAuth2 Issues

**Browser doesn't open:**
- Check if `NUXEO_OAUTH_CLIENT_ID` and `NUXEO_OAUTH_CLIENT_SECRET` are set
- Try manual authentication with `--no-browser` flag
- Verify the OAuth2 client is properly configured in Nuxeo

**Authentication fails:**
- Verify redirect URI in Nuxeo matches `http://localhost:*`
- Check client ID and secret are correct
- Ensure user has proper permissions in Nuxeo

**Token refresh fails:**
- Tokens may have expired completely
- Run `nuxeo-mcp --oauth2` to re-authenticate
- Check network connectivity to Nuxeo server

### Storage Issues

**Keyring not available:**
- Install keyring dependencies for your OS
- Falls back to encrypted file storage automatically
- Check file permissions in `~/.local/share/nuxeo-mcp/tokens/`

**Permission denied errors:**
- Ensure you have write access to config directory
- Check file ownership and permissions
- Try clearing corrupted token storage

## Security Best Practices

1. **Use OAuth2 for Production**
   - Never use basic auth over unencrypted connections
   - OAuth2 provides better security with token rotation

2. **Protect Client Secrets**
   - Never commit secrets to version control
   - Use environment variables or secure vaults
   - Rotate secrets regularly

3. **Token Security**
   - Tokens are automatically encrypted at rest
   - Use OS keychain when available
   - Set appropriate file permissions for fallback storage

4. **Network Security**
   - Always use HTTPS in production
   - Verify SSL certificates
   - Use VPN for additional security when needed

## Migration from Basic Auth

To migrate existing setups from basic authentication to OAuth2:

1. Register OAuth2 client in Nuxeo (see setup above)
2. Update environment variables:
   ```bash
   # Change from:
   export NUXEO_USERNAME="admin"
   export NUXEO_PASSWORD="password"
   
   # To:
   export NUXEO_AUTH_METHOD="oauth2"
   export NUXEO_OAUTH_CLIENT_ID="your-client-id"
   export NUXEO_OAUTH_CLIENT_SECRET="your-secret"
   ```
3. Run `nuxeo-mcp --oauth2` to authenticate
4. Tokens will be stored securely for future use

## Advanced Configuration

### Custom OAuth2 Endpoints

For non-standard Nuxeo installations:

```bash
export NUXEO_OAUTH_AUTH_ENDPOINT="https://custom-auth.example.com/authorize"
export NUXEO_OAUTH_TOKEN_ENDPOINT="https://custom-auth.example.com/token"
export NUXEO_OAUTH_OPENID_URL="https://custom-auth.example.com/.well-known/openid-configuration"
```

### Multiple Nuxeo Instances

Use the configuration file to manage multiple instances:

```python
from nuxeo_mcp.config import MCPAuthConfig, NuxeoServerConfig, OAuth2Config

config = MCPAuthConfig()

# Add production server
prod_oauth = OAuth2Config(
    client_id="prod-client",
    client_secret="prod-secret"
)
config.add_server("production", NuxeoServerConfig(
    url="https://prod.nuxeo.com/nuxeo",
    auth_method=AuthMethod.OAUTH2,
    oauth2_config=prod_oauth
))

# Add staging server
staging_oauth = OAuth2Config(
    client_id="staging-client",
    client_secret="staging-secret"
)
config.add_server("staging", NuxeoServerConfig(
    url="https://staging.nuxeo.com/nuxeo",
    auth_method=AuthMethod.OAUTH2,
    oauth2_config=staging_oauth
))

config.default_server = "production"
config.save()
```

## Support

For issues or questions:
- Check the [troubleshooting section](#troubleshooting)
- Review [Nuxeo OAuth2 documentation](https://doc.nuxeo.com/nxdoc/using-oauth2/)
- Open an issue on GitHub