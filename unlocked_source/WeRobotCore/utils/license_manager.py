from __future__ import annotations

import hashlib
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class LicenseManager:
    """Local source-build license provider with remote verification removed."""

    def __init__(self) -> None:
        self.license_file = Path.home() / ".yokowebot" / "license.dat"
        self._machine_code: str | None = None
        self._cached_status = True
        self._last_check_time = datetime.now(timezone.utc).timestamp()
        self._check_interval = 1800

    async def check_license_status(self) -> bool:
        return True

    async def activate_license(
        self,
        activation_code: str,
        machine_code: str,
    ) -> dict[str, Any]:
        return {
            "valid": True,
            "message": "local source build",
            "data": self._license_data(machine_code),
        }

    async def get_license_info(self) -> dict[str, Any]:
        return {
            "success": True,
            "data": {
                "machine_code": self.get_machine_code(),
                "unbind_remain": 999,
                "license_type": "local_source",
            },
        }

    def get_machine_code(self) -> str:
        if self._machine_code:
            return self._machine_code

        system_info = platform.uname()
        machine_info = f"{system_info.node}-{system_info.processor}-{system_info.machine}"
        digest = hashlib.sha256(machine_info.encode()).hexdigest()[:16].upper()
        self._machine_code = "-".join(digest[index : index + 4] for index in range(0, 16, 4))
        return self._machine_code

    async def verify_local_license(self) -> dict[str, Any]:
        return {
            "valid": True,
            "message": "local source build",
            "data": self._license_data(self.get_machine_code()),
        }

    async def verify_online_license(self, machine_code: str) -> dict[str, Any]:
        return {
            "valid": True,
            "message": "remote verification disabled",
            "data": self._license_data(machine_code),
        }

    @staticmethod
    def _license_data(machine_code: str) -> dict[str, Any]:
        return {
            "machine_code": machine_code,
            "activated_at": datetime.now(timezone.utc).isoformat(),
            "expired_at": "2099-12-31T23:59:59+00:00",
            "license_type": "local_source",
            "agent_id": "local-source",
            "activation_code": "LOCAL-SOURCE",
        }
