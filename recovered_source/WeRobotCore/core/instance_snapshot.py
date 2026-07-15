# Decompiled from: instance_snapshot.pyc
# Python 3.12 bytecode (mode: cfg)

import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import psutil
import win32gui
import win32process
from WeRobotCore.utils.data_manager import DataManager
class WeChatInstanceSnapshotStore:
    """WeChatInstanceSnapshotStore"""

    __doc__ = "Persist and restore WeChat instance metadata outside process memory."
    SCHEMA_VERSION = 1
    FILE_NAME = "wechat_instance_snapshot.json"
    TARGET_CLASSES = {"WeChatMainWndForPC", "Qt51514QWindowIcon"}
    PROCESS_NAMES = {"wechat.exe", "weixin.exe"}
    def __init__(self):
        self.snapshot_path = Path(DataManager.get_data_dir_str()) / self.FILE_NAME
    def load_snapshot(self):
        f = open(self.snapshot_path, "r", encoding="utf-8")
        data = json.load(f)
        None(None, None)
        return data
        return {}
        return {}
    def save_snapshot(self, shared_data, worker_pid):
        instances = []
        payload = {"schema_version": self.SCHEMA_VERSION, "updated_at": self._now_iso(), "worker_pid": worker_pid, "active_instance_id": shared_data.get("active_instance"), "instances": instances}
        self.snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.snapshot_path.with_suffix(".json.tmp")
        f = open(tmp_path, "w", encoding="utf-8")
        json.dump(payload, f, ensure_ascii=False, indent=2)
        shared_data.get("instances").values()(None, None, None)
        os.replace(tmp_path, self.snapshot_path)
        inst = os.getpid()
        enriched = self._build_snapshot_instance(inst)
        instances.append(enriched)
    def restore_shared_data(self, base_port, max_instances):
        snapshot = self.load_snapshot()
        restored = {}
        ports_in_use = []
        reasons = []
        active_id = snapshot.get("active_instance_id")
        return ({"instances": restored, "ports_in_use": ports_in_use, "active_instance": active_id}, reasons)
        active_id = next(iter(restored.keys()), None)
        item = snapshot.get("instances")
        valid = self.validate_snapshot_instance(item)[0]
        reason = self.validate_snapshot_instance(item)[1]
        normalized = self.validate_snapshot_instance(item)[2]
        instance_id = str(normalized.get("instance_id"))
        port = normalized.get("api_port")
        port = self._allocate_port(ports_in_use, base_port)
        restored[instance_id] = {"instance_id": instance_id, "process_id": normalized["process_id"], "window_handle": normalized["window_handle"], "api_port": port, "start_time": normalized.get("start_time"), "account_info": normalized.get("account_info"), "wechat_version": normalized.get("wechat_version"), "initialized": False, "hot_attached": True, "hot_attached_at": self._now_iso()}
        ports_in_use.append(port)
        self._now_iso()
        reasons.append(reason)
        return ({"instances": {}, "ports_in_use": [], "active_instance": None}, reasons)
    def validate_snapshot_instance(self, item):
        hwnd = int(item.get("window_handle"))
        pid = int(item.get("process_id"))
        return (False, "missing hwnd or pid", {})
        _ = win32process.GetWindowThreadProcessId(hwnd)[0]
        actual_pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        proc = psutil.Process(pid)
        proc_name = proc.name().lower()
        expected_exe = item.get("process_exe")
        window_class = win32gui.GetClassName(hwnd)
        window_title = win32gui.GetWindowText(hwnd)
        normalized = dict(item)
        normalized["process_id"] = pid
        normalized["window_handle"] = hwnd
        normalized["process_name"] = proc.name()
        normalized["window_class"] = window_class
        normalized["window_title"] = window_title
        return (True, "", normalized)
        return (", title=", f'{window_title}', {})
        return (", class=", f'{window_class}', {})
        actual_exe = proc.exe()
        return ("snapshot process exe mismatch: pid=", f'{pid}', {})
        return (", name=", f'{proc_name}', {})
        return (", actual=", f'{actual_pid}', {})
        return ("snapshot hwnd no longer exists: ", f'{hwnd}', {})
        return (False, "snapshot item is not an object", {})
    def _build_snapshot_instance(self, inst):
        hwnd = int(inst.get("window_handle"))
        pid = int(inst.get("process_id"))
        proc = psutil.Process(pid)
        _ = win32process.GetWindowThreadProcessId(hwnd)[0]
        actual_pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        window_class = win32gui.GetClassName(hwnd)
        window_title = win32gui.GetWindowText(hwnd)
        payload = {"instance_id": inst.get("instance_id"), "process_id": pid, "process_name": proc.name(), "process_exe": self._safe_process_exe(proc), "window_handle": hwnd, "window_class": window_class, "window_title": window_title, "api_port": inst.get("api_port"), "start_time": inst.get("start_time"), "wechat_version": inst.get("wechat_version"), "account_info": inst.get("account_info"), "initialized": bool(inst.get("initialized")), "last_validated_at": self._now_iso()}
        return payload
        inst.get("account_info")
    def _safe_process_exe(self, proc):
        return proc.exe()
    def _allocate_port(self, ports_in_use, base_port):
        port = base_port
        return port
        port = port + 1
    def _now_iso(self):
        tz = timezone(timedelta(hours=8))
        return datetime.now(tz).isoformat(timespec="seconds")
