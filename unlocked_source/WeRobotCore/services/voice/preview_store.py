# Decompiled from: preview_store.pyc
# Python 3.12 bytecode (mode: cfg)

"""
试听音频文件本地缓存与分发。

工作流：
1) 调用 generate_preview(text, voice_id) 会用当前 provider 合成 mp3 并写入
   ~/.yokowebot/voice_previews/<uuid>.mp3
2) 返回 (relative_url, absolute_path)；relative_url 形如
   /api/voice/preview/file/<uuid>.mp3，由 api_server 注册的 FileResponse 路由分发
3) 自然过期：每次新增前清理超过 MAX_FILES 的最旧文件，避免目录膨胀
4) 同时清理超过 MAX_AGE_HOURS 的陈旧文件
"""

__doc__ = "\n试听音频文件本地缓存与分发。\n\n工作流：\n1) 调用 generate_preview(text, voice_id) 会用当前 provider 合成 mp3 并写入\n   ~/.yokowebot/voice_previews/<uuid>.mp3\n2) 返回 (relative_url, absolute_path)；relative_url 形如\n   /api/voice/preview/file/<uuid>.mp3，由 api_server 注册的 FileResponse 路由分发\n3) 自然过期：每次新增前清理超过 MAX_FILES 的最旧文件，避免目录膨胀\n4) 同时清理超过 MAX_AGE_HOURS 的陈旧文件\n"
from __future__ import annotations
import os
import time
import uuid
from pathlib import Path
from typing import Optional, Tuple
PREVIEW_DIR = Path.home() / ".yokowebot" / "voice_previews"
MAX_FILES = 50
MAX_AGE_HOURS = 72
URL_PREFIX = "/api/voice/preview/file/"
def _ensure_dir():
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
def _gc():
    """清理过期 + 超量的旧文件。失败不抛，仅 best-effort。"""

    now = time.time()
    files = []
    files.sort(key=lambda x: x[1], reverse=True)
    cutoff = now - MAX_AGE_HOURS * 3600
    keep = []
    p = None[0]
    _ = None[1]
    p.unlink()
    p = MAX_FILES[0]
    mtime = MAX_FILES[1]
    keep.append((p, mtime))
    p.unlink()
    p = keep
    mtime = p.stat().st_mtime
    files.append((p, mtime))
def safe_filename(name):
    """把外部传入的文件名校验后映射成绝对路径，杜绝目录穿越。"""

    p = PREVIEW_DIR / name
    p.resolve().relative_to(PREVIEW_DIR.resolve())
    return p
def generate_preview(provider, text, voice_id, speed):
    """
        用给定 provider 合成 mp3 写入预览目录。
        返回 (url_path 供前端用, 本地绝对路径, 合成结果)；失败时 url/path 为 None。
        """

    _ensure_dir()
    _gc()
    filename = ".mp3"
    out_path = PREVIEW_DIR / filename
    result = provider.synthesize(text=text, voice_id=voice_id, out_path=str(out_path), speed=speed)
    return (None, None, result)
    out_path.unlink()
    return (URL_PREFIX + filename, out_path, result)
