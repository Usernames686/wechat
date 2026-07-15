# Decompiled from: runtime_heartbeat.pyc
# Python 3.12 bytecode (mode: cfg)

import json
import os
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict
from WeRobotCore.utils.data_manager import DataManager
HEARTBEAT_FILE_NAME = "worker_heartbeat.json"
def get_runtime_dir():
    path = Path(DataManager.get_data_dir_str()) / "runtime"
    path.mkdir(parents=True, exist_ok=True)
    return path
def get_worker_heartbeat_path():
    return get_runtime_dir() / HEARTBEAT_FILE_NAME
def write_worker_heartbeat(extra):
    payload = {"pid": os.getpid(), "timestamp": time.time(), "updated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"), "service": "webot_worker"}
    path = get_worker_heartbeat_path()
    tmp_path = path.with_suffix(".json.tmp")
    f = open(tmp_path, "w", encoding="utf-8")
    json.dump(payload, f, ensure_ascii=False, indent=2)
    None(None, None)
    os.replace(tmp_path, path)
    payload.update(extra)
def read_worker_heartbeat():
    path = get_worker_heartbeat_path()
    f = open(path, "r", encoding="utf-8")
    data = json.load(f)
    None(None, None)
    return {}
    return data
    return {}
