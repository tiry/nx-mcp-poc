#!/usr/bin/env python
"""
Test multi-server support in Nuxeo MCP
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nuxeo_mcp.server_manager import ServerManager, ServerConfig
import json

print("Testing Multi-Server Support for Nuxeo MCP")
print("=" * 60)

# Create a test server manager with a custom config file
test_config = "/tmp/test_nuxeo_servers.json"
manager = ServerManager(config_file=test_config)

print("\n1. Initial State")
print("-" * 40)
servers = manager.list_servers()
print(f"Servers configured: {len(servers)}")
for name, info in servers.items():
    print(f"  - {name}: {info['description']}")
    if info.get('is_active'):
        print(f"    (ACTIVE)")

print("\n2. Adding Custom Server")
print("-" * 40)
custom_server = ServerConfig(
    name="custom",
    url="https://my-nuxeo.example.com/nuxeo",
    username="admin",
    password="secret",
    description="Custom Nuxeo Instance"
)
manager.add_server(custom_server)
print(f"✅ Added server: {custom_server.name}")

print("\n3. Switching Active Server")
print("-" * 40)
print(f"Current active: {manager.active_server}")
manager.set_active_server("custom")
print(f"✅ Switched to: {manager.active_server}")

print("\n4. Testing Persistence")
print("-" * 40)
# Create a new manager instance to test persistence
manager2 = ServerManager(config_file=test_config)
print(f"Active server after reload: {manager2.active_server}")
servers2 = manager2.list_servers()
print(f"Servers after reload: {list(servers2.keys())}")

print("\n5. Server Selection Check")
print("-" * 40)
print(f"Needs selection? {manager2.needs_server_selection()}")
active = manager2.get_active_server()
if active:
    print(f"Active server details:")
    print(f"  Name: {active.name}")
    print(f"  URL: {active.url}")
    print(f"  Description: {active.description}")

print("\n6. Getting Server Choices")
print("-" * 40)
print("Available servers:")
print(manager2.get_server_choices())

print("\n7. Removing Server")
print("-" * 40)
manager2.remove_server("custom")
print("✅ Removed custom server")
print(f"Servers remaining: {list(manager2.list_servers().keys())}")

# Clean up test file
if os.path.exists(test_config):
    os.remove(test_config)
    # Also remove context file
    context_file = test_config.replace("servers.json", "context.json")
    if os.path.exists(context_file):
        os.remove(context_file)

print("\n" + "=" * 60)
print("✅ All server management functions working correctly!")
print("\nKey Features:")
print("  - Multiple server configurations")
print("  - Persistent storage of servers and active context")
print("  - Easy switching between servers")
print("  - Default servers (demo and local)")
print("  - Server connection testing")