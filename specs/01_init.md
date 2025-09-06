

I want to build a MCP Server to expose `tools`/`resources`/`prompts templates` for a Nuxeo Content Repository Server.

I want to build the MCP Server using python and FastMCP.

I want to use pip as a package manager and want to work in a python `venv`.

To access the Nuxeo Server, I want to use the Nuxeo Python Client.

 - can be installed using `python -m pip install -U --user nuxeo`
    - https://doc.nuxeo.com/nxdoc/python-client/
 - python documentation is available here: https://nuxeo.github.io/nuxeo-python-client/latest/index.html

To run the Nuxeo Server, for testing purpose we will use Docker.

   `docker pull nuxeo/nuxeo`

The default Login/Password is Administrator/Administrator

I want to use pytest to define unit tests.
I want the unit test to allow to start Nuxeo via Docker if needed.

As first step:

 - initialize a python virtual env
 - add the needed dependencies
 - initialize an empty MCP Server
 - initialize unit tests 
 - create a ReadMe.md providing all details





