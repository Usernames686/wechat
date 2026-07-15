# Portable launcher source

This directory contains the auditable launcher and loopback authentication
fixture used by the portable release.

- `start_noverify.cmd` / `start_noverify.ps1`: start the local fixture and RPA.
- `stop_noverify.cmd` / `stop_noverify.ps1`: stop both local processes.
- `dev_auth_stub.py`: source for the standalone `dev_auth_stub.exe` included in
  the release ZIP.
- `mcp.json.example`: generic MCP Streamable HTTP configuration.

The full PyInstaller runtime and executables are distributed as a release asset
instead of being committed to Git history.

The release executable also applies an equal-length bytecode constant patch for
non-GBK log glyphs in `api_server`. This prevents Windows GBK stdout from
interrupting the WeChat 4.1 automatic environment configuration flow. The
reproducible patcher is available at `tools/patch_pyinstaller_gbk_logs.py`.
