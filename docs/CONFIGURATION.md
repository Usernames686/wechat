# Configuration

## Portable build

The portable release is the recommended way to run the recovered application.
It includes the application runtime and a standalone loopback authentication
component, so system Python and cloud licensing services are not required.

1. Download `yoko_rpa_mcp_noverify.zip` from the latest release.
2. Extract the complete ZIP to a writable directory.
3. Start the desktop WeChat client and sign in.
4. Double-click `start_noverify.cmd`.
5. The console opens at `http://127.0.0.1:9922/`.

The startup window prints the MCP endpoint and the generated MCP pairing token.
The token is also stored at `%USERPROFILE%\.yokowebot\mcp_token.dat`.

To stop the service, double-click `stop_noverify.cmd`.

## MCP host configuration

Copy `portable_launcher/mcp.json.example` into the MCP configuration format used
by your host and replace `MCP_TOKEN` with the token printed at startup.

The transport stays local:

```text
MCP host -> http://127.0.0.1:9922/mcp -> Yoko RPA -> desktop WeChat
```

## Source configuration

For continued source reconstruction, copy `.env.example` to `.env` and fill only
the integrations you use. Empty customer integration values keep those adapters
disabled. The unlocked license path does not require Supabase or Yoko cloud
values.

Optional Coze, Dify, Fireflow, Doubao voice, and similar provider credentials are
configured through the application console and belong to the user running the
application.

## Important source status

`recovered_source` and `unlocked_source` are decompiler output. The portable
release is runnable, while the complete recovered source tree still requires
manual control-flow reconstruction before it can be rebuilt independently.
