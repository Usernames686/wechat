Yoko RPA local no-verify build
================================

Requirements:
  Windows 10/11 and the desktop WeChat client.
  Python is not required.

Start:
  Double-click start_noverify.cmd

Stop:
  Double-click stop_noverify.cmd

Console:
  http://127.0.0.1:9922/

Development identity:
  Account: dev
  Password: dev

Behavior:
  - Binds the authentication fixture to 127.0.0.1 only.
  - Routes Yoko and Supabase authorization calls to the local fixture.
  - Includes a standalone local authentication component.
  - Does not change the original installed executable or remote databases.
  - Starts the bundled yoko_rpa_mcp.exe in the interactive desktop session.
