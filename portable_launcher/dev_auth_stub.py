#!/usr/bin/env python3
"""Loopback-only authentication fixture for local yoko RPA development."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse


HOST = "127.0.0.1"
PORT = int(os.environ.get("YOKO_DEV_AUTH_PORT", "19922"))
DEV_AGENT = os.environ.get("YOKO_DEV_AGENT", "dev")
DEV_PASSWORD = os.environ.get("YOKO_DEV_PASSWORD", "dev")
DEV_AGENT_ID = "00000000-0000-4000-8000-000000000001"
DEV_CODE_ID = "00000000-0000-4000-8000-000000000002"
EXPIRES_AT = "2099-12-31T23:59:59+00:00"


def query_value(query: dict[str, list[str]], key: str, default: str = "") -> str:
    value = query.get(key, [default])[0]
    return unquote(value[3:] if value.startswith("eq.") else value)


class DevAuthHandler(BaseHTTPRequestHandler):
    server_version = "YokoDevAuth/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[dev-auth] {self.address_string()} {fmt % args}")

    def send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Content-Range", "0-0/1")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            return {}

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/health":
            self.send_json(200, {"ok": True, "mode": "local-development"})
            return

        if parsed.path == "/rest/v1/device_licenses":
            machine_code = query_value(query, "machine_code", "DEV0-0000-0000-0000")
            self.send_json(
                200,
                [
                    {
                        "id": "00000000-0000-4000-8000-000000000003",
                        "machine_code": machine_code,
                        "activation_code_id": DEV_CODE_ID,
                        "status": "active",
                        "expired_at": EXPIRES_AT,
                        "license_type": "development",
                    }
                ],
            )
            return

        if parsed.path == "/rest/v1/activation_codes":
            self.send_json(
                200,
                [
                    {
                        "id": DEV_CODE_ID,
                        "code": "LOCAL-DEVELOPMENT",
                        "agent_id": DEV_AGENT_ID,
                        "unbind_remain": 999,
                        "status": "active",
                    }
                ],
            )
            return

        if parsed.path == "/rest/v1/agents":
            name = query_value(query, "name", DEV_AGENT)
            self.send_json(
                200,
                [
                    {
                        "id": DEV_AGENT_ID,
                        "name": name,
                        "channel_id": "local-development",
                        "brand_name_cn": "本地开发",
                        "login_password": DEV_PASSWORD,
                    }
                ],
            )
            return

        self.send_json(200, [])

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        payload = self.read_json()

        if parsed.path == "/v1/rpa/auth/verify":
            self.send_json(
                200,
                {
                    "success": True,
                    "data": {
                        "expires_at": EXPIRES_AT,
                        "machine_code": payload.get("machine_code"),
                        "mode": "local-development",
                    },
                },
            )
            return

        if parsed.path == "/v1/rpa/legacy/activate":
            self.send_json(
                200,
                {
                    "valid": True,
                    "message": "local development activation",
                    "data": {
                        "expired_at": EXPIRES_AT,
                        "license_type": "development",
                    },
                },
            )
            return

        if parsed.path == "/v1/rpa/legacy/unbind":
            self.send_json(
                200,
                {"success": True, "message": "local development unbind", "data": {"remain_unbind": 999}},
            )
            return

        self.send_json(200, {"success": True, "data": payload})

    def do_PATCH(self) -> None:
        self.read_json()
        self.send_json(200, [])


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), DevAuthHandler)
    print(f"[dev-auth] listening on http://{HOST}:{PORT}")
    print(f"[dev-auth] agent={DEV_AGENT!r}; started={datetime.now(timezone.utc).isoformat()}")
    server.serve_forever()


if __name__ == "__main__":
    main()
