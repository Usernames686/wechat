# Unlocked source changes

This directory is a copy of the recovered application source with the recovered
license-verification paths replaced by local development responses. The original
recovered source remains unchanged in `../recovered_source`.

## Changed files

- `WeRobotCore/utils/license_manager.py`
  - Removed remote license requests and local license-file validation.
  - `check_license_status()` always reports an active local development license.
  - Activation, local verification, online verification, and license information
    return a consistent `local_source` record expiring at the end of 2099.
  - Machine-code generation remains local and deterministic for the current host.
- `api_server.py`
  - The HTTP license middleware now records `local_source` attribution and passes
    requests directly to the application.
  - Recovered agent login, existence, and activation-code endpoints return local
    development records.
- `mcp_gateway.py`
  - `_resolve_license()` no longer calls Supabase or reads an activation record.
  - MCP attribution is populated from the local machine code and reports active.

## Verification performed

The three changed Python files pass CPython compilation with `python -m
py_compile`. `LicenseManager` was also imported independently and exercised to
confirm the local status and license-data responses.

## Recovered-source limitation

This tree was reconstructed from PyInstaller CPython 3.12 bytecode. It is an
inspection and reconstruction artifact, not the original build tree. Some other
recovered modules still contain decompiler output such as misplaced `return`
statements, malformed call expressions, and lost control-flow structure. Those
modules need manual reconstruction from `../disassembly/cpython312` and
`../bytecode` before this entire tree can be packaged as a replacement EXE.

The runnable local fixture and extracted binary artifacts are intentionally not
included in this source-only repository.
