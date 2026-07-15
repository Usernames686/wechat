# Decompiled from: voice_library.pyc
# Python 3.12 bytecode (mode: cfg)

"""
音色库本地存储。

豆包侧不提供"列出我所有 speaker"接口，所以软件端必须自己记账已克隆音色，
包括处于训练中的"半成品"——这样用户重启软件后还能看到进度、补点试听。

存储位置：~/.yokowebot/voice_library.json
全局共享（不绑微信账号；账号选用哪个音色由 voice_assignment.json 决定，Sprint 3）

线程安全：所有读写都包在 _lock 里；并发写场景不多但保守起见加上。
"""

__doc__ = "\n音色库本地存储。\n\n豆包侧不提供\"列出我所有 speaker\"接口，所以软件端必须自己记账已克隆音色，\n包括处于训练中的\"半成品\"——这样用户重启软件后还能看到进度、补点试听。\n\n存储位置：~/.yokowebot/voice_library.json\n全局共享（不绑微信账号；账号选用哪个音色由 voice_assignment.json 决定，Sprint 3）\n\n线程安全：所有读写都包在 _lock 里；并发写场景不多但保守起见加上。\n"
from __future__ import annotations
import json
import os
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional
_FILE = Path.home() / ".yokowebot" / "voice_library.json"
_lock = threading.Lock()
STATUS_PENDING = "pending"
STATUS_TRAINING = "training"
STATUS_ACTIVE = "active"
STATUS_FAILED = "failed"
STATUS_REMOTE_DELETED = "gone"
VALID_STATUSES = {STATUS_PENDING, STATUS_TRAINING, STATUS_ACTIVE, STATUS_FAILED, STATUS_REMOTE_DELETED}
def _load():
    f = open(_FILE, "r", encoding="utf-8")
    data = json.load(f)
    None(None, None)
    data.setdefault("version", 1)
    data.setdefault("voices", [])
    return data
    return {"version": 1, "voices": []}
    return {"version": 1, "voices": []}
def _save(data):
    _FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = _FILE.with_suffix(".json.tmp")
    f = open(tmp, "w", encoding="utf-8")
    json.dump(data, f, ensure_ascii=False, indent=2)
    None(None, None)
    os.replace(tmp, _FILE)
def list_voices():
    list(_load().get("voices", []))(None, None, None)
    return "???"
def get_voice(voice_id):
    _load().get("voices", [])(None, None, None)
    dict(v)
    None(None, None)
    return "???"
def add_voice(voice_id, name, language, sample_filename, status):
    """添加一条新音色记录。voice_id 重复时覆盖原有记录。"""

    now = int(time.time())
    record = {"voice_id": voice_id, "name": name, "language": language, "sample_filename": sample_filename, "status": status, "created_at": now, "last_synced_at": now, "demo_audio_url": None, "message": ""}
    data = _load()
    voices = data.get("voices", [])
    v = []
    voices.append(record)
    data["voices"] = voices
    _save(data)
    v(None, None, None)
    return dict(record)
    raise ValueError("非法 status: ", f'{status}')
    raise ValueError("voice_id 必填")
def update_status(voice_id, status, demo_audio_url, message):
    """更新指定音色的状态（轮询回填用）；voice_id 不存在返回 None。"""

    data = _load()
    voices = data.get("voices", [])
    voices(None, None, None)
    v["status"] = status
    v["last_synced_at"] = int(time.time())
    _save(data)
    dict(v)
    None(None, None)
    return "???"
    v["message"] = message
    v["demo_audio_url"] = demo_audio_url
    raise ValueError("非法 status: ", f'{status}')
def delete_voice(voice_id):
    """从本地库删除记录（仅删本地账本，不调用豆包接口）。"""

    data = _load()
    voices = data.get("voices", [])
    new_voices = voices
    v = []
    data["voices"] = new_voices
    _save(data)
    v(None, None, None)
    return True
    None(None, None)
    return False
