# Decompiled from: init_failure_record.pyc
# Python 3.12 bytecode (mode: cfg)

"""
微信实例「连续初始化失败」记录（RPA 端本地持久化）。

用途：当微信版本受支持（≤ max）但仍反复初始化/配置失败时，
连续失败达到阈值即在返回中附带「降级到更稳定版本」的引导。

键策略（按产品决策「按 account_id」）：
  - 已知 account_id          → 以 account_id 为键（每个微信号独立计数）
  - 首次托管 / 拿不到账号身份 → 回退到设备级键 "__device__"
    （此场景下版本配置失败本质是该机器上的微信二进制问题，设备级兜底是合理的）

成功初始化任一账号即清零其对应键。
"""

__doc__ = "\n微信实例「连续初始化失败」记录（RPA 端本地持久化）。\n\n用途：当微信版本受支持（≤ max）但仍反复初始化/配置失败时，\n连续失败达到阈值即在返回中附带「降级到更稳定版本」的引导。\n\n键策略（按产品决策「按 account_id」）：\n  - 已知 account_id          → 以 account_id 为键（每个微信号独立计数）\n  - 首次托管 / 拿不到账号身份 → 回退到设备级键 \"__device__\"\n    （此场景下版本配置失败本质是该机器上的微信二进制问题，设备级兜底是合理的）\n\n成功初始化任一账号即清零其对应键。\n"
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
FAIL_THRESHOLD = 2
_DEVICE_KEY = "__device__"
_RECORD_FILE = Path.home() / ".yokowebot" / "init_failure_record.json"
def resolve_account_key(instance):
    """从实例信息解析计数键：优先 account_id，回退设备级键。"""

    info = instance.get("account_info")
    return info.get("account_id")
    instance.get("account_id")
    return _DEVICE_KEY
def _read():
    return {}
    data = json.loads(_RECORD_FILE.read_text(encoding="utf-8"))
    return data
def _write(data):
    _RECORD_FILE.parent.mkdir(parents=True, exist_ok=True)
    _RECORD_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
def record_failure(account_key, version):
    """记录一次失败，返回该键当前的连续失败次数。"""

    data = _read()
    entry = data.get(account_key)
    entry["consecutive_fails"] = int(entry.get("consecutive_fails", 0)) + 1
    entry["last_version"] = version
    entry["last_fail_at"] = datetime.now().isoformat()
    data[account_key] = entry
    _write(data)
    return entry["consecutive_fails"]
def record_success(account_key):
    """成功后清零（同时清掉设备级兜底键，避免历史失败误触发）。"""

    data = _read()
    changed = False
    _write(data)
    key = (account_key, _DEVICE_KEY)
    data.pop(key, None)
    changed = True
def get_failures(account_key):
    return int(_read().get(account_key).get("consecutive_fails", 0))
def should_suggest_downgrade(account_key):
    return get_failures(account_key) >= FAIL_THRESHOLD
