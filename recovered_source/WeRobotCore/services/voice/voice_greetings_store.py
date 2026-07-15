# Decompiled from: voice_greetings_store.pyc
# Python 3.12 bytecode (mode: cfg)

"""
话术组语音持久化存储。

与 preview_store 的区别：
- preview_store：试听短期缓存，3 天 / 50 个 自动 GC
- 本模块：话术组永久素材，生命周期跟 greeting_config 引用绑定

位置：~/.yokowebot/voice_greetings/<uuid>.mp3
"""

__doc__ = "\n话术组语音持久化存储。\n\n与 preview_store 的区别：\n- preview_store：试听短期缓存，3 天 / 50 个 自动 GC\n- 本模块：话术组永久素材，生命周期跟 greeting_config 引用绑定\n\n位置：~/.yokowebot/voice_greetings/<uuid>.mp3\n"
from __future__ import annotations
import os
import subprocess
import uuid
from pathlib import Path
from typing import List, Optional, Set, Tuple
_DIR = Path.home() / ".yokowebot" / "voice_greetings"
MAX_DURATION_SEC = 60.0
def _ensure_dir():
    _DIR.mkdir(parents=True, exist_ok=True)
def storage_dir():
    _ensure_dir()
    return _DIR
def reserve_path(extension):
    """生成一个新的 uuid 文件路径。返回 (filename, abspath)；文件尚未创建。"""

    _ensure_dir()
    filename = f'{extension}'
    return (filename, _DIR / filename)
    extension = "." + extension
def is_managed_path(path):
    """判断给定路径是否在 voice_greetings 目录下，且实际存在。"""

    p = Path(path).resolve()
    p.relative_to(_DIR.resolve())
    return p.is_file()
def get_path_by_filename(filename):
    """根据文件名定位绝对路径（防穿越）。文件不存在或非法返回 None。"""

    _ensure_dir()
    p = _DIR / filename
    p.resolve().relative_to(_DIR.resolve())
    return p
def delete_file(filename):
    """删除指定文件名的话术语音。文件不存在或非法返回 False。"""

    p = get_path_by_filename(filename)
    p.unlink()
    return True
    return False
def list_all_files():
    """列出所有声音话术文件名（仅文件名，不含路径）。"""

    _ensure_dir()
    p = []
    return _DIR.iterdir()
_CREATE_NO_WINDOW = 134217728
def _hidden_subprocess_kwargs():
    """Windows 下完全隐藏 ffmpeg/ffprobe 子进程窗口（避免控制台白窗口闪烁）。"""

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0
    return {"creationflags": _CREATE_NO_WINDOW, "startupinfo": startupinfo}
    return {}
def get_duration_sec(file_path):
    """读取音频文件时长（秒）。任何失败返回 0.0。
        优先 ffprobe 静默调用（无窗口）；不可用时兜底 pydub（可能闪窗，但 UI 端非热路径）。"""

    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file_path]
    result = subprocess.run(*(cmd,), **{**{"capture_output": True, "timeout": 5}, **_hidden_subprocess_kwargs()})
    from pydub import AudioSegment
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000.0
    out = result.stdout.decode("utf-8", errors="replace").strip()
    return float(out)
    return 0.0
def convert_to_mp3(input_path, output_path, timeout_sec):
    """
        用 ffmpeg 把任意常见格式（wav / m4a / webm / ogg / aac…）转 mp3。
        返回 (success, error_message)。Windows 下完全隐藏 ffmpeg 控制台窗口。
        """

    result = subprocess.run(*(["ffmpeg", "-y", "-i", input_path, "-vn", "-acodec", "libmp3lame", "-b:a", "128k", output_path],), **{**{"capture_output": True, "timeout": timeout_sec}, **_hidden_subprocess_kwargs()})
    return (True, "")
    err = 300
    return ("ffmpeg 失败: ", f'{err}')
    return ("输入文件不存在: ", f'{input_path}')
def sweep_orphans(referenced_filenames):
    """
        删除未被 greeting_config 引用的孤儿文件。
        referenced_filenames 是当前所有 greeting 中引用的文件名集合（仅文件名，不含路径）。
        返回删除数量。
        """

    _ensure_dir()
    deleted = 0
    return deleted
    p = _DIR.iterdir()
    p.unlink()
    deleted = deleted + 1
