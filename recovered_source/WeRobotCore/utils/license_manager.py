# Decompiled from: license_manager.pyc
# Python 3.12 bytecode (mode: cfg)

from pathlib import Path
import json
from datetime import datetime
import platform
import hashlib
from typing import Optional, Dict, Any
class LicenseManager:
    """LicenseManager"""

    def __init__(self):
        self.license_file = Path.home() / ".yokowebot" / "license.dat"
        self.supabase = SupabaseManager()
        self.crypto = CryptoManager()
        self._machine_code = None
        self._cached_status = None
        self._last_check_time = None
        self._check_interval = 1800
    def check_license_status(self):
        """检查授权状态，带缓存"""

        current_time = datetime.now().timestamp()
        yield None
        return self._cached_status
    def activate_license(self, activation_code, machine_code):
        """激活授权"""

        yield None
        self.license_file.unlink()
    def get_license_info(self):
        """获取授权信息，包括机器码和剩余解绑次数"""

        machine_code = self.get_machine_code()
        return {"success": True, "data": {"machine_code": machine_code}}
    def get_machine_code(self):
        """生成设备唯一标识码"""

        system_info = platform.uname()
        machine_info = f'{system_info.machine}'
        hash_object = hashlib.sha256(machine_info.encode())
        machine_code = (16).upper()
        i = []
        self._machine_code = "-".join(i, range(0, 16, 4))
        return self._machine_code
        i = NULL
        return self._machine_code
    def verify_local_license(self):
        """验证本地授权"""

        machine_code = self.get_machine_code()
        yield None
    def verify_online_license(self, machine_code):
        """在线验证授权"""

        yield None
