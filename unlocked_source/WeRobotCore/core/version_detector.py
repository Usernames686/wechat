# Decompiled from: version_detector.pyc
# Python 3.12 bytecode (mode: cfg)

import os
from enum import Enum
from typing import Optional, Tuple
import uiautomation as auto
import psutil
import win32process
import win32api
class WeChatVersion(Enum):
    """WeChatVersion"""

    LEGACY_3_9 = "3.9.x"
    MODERN_4_1 = "4.1.x"
WeChatBuild = Tuple[(int, int, int, int)]
def read_exe_file_version(exe_path):
    """
        读取指定 exe 的 FileVersion 资源段，返回 (major, minor, patch, build) 四元组。
        无路径 / 文件不存在 / 资源段缺失（精简版/部分破解版）/ pywin32 不可用时返回 None。
        """

    info = win32api.GetFileVersionInfo(exe_path, "\\")
    ms = info["FileVersionMS"]
    ls = info["FileVersionLS"]
    return (ms >> 16 & 65535, ms & 65535, ls >> 16 & 65535, ls & 65535)
def format_build(build):
    """把 (4,1,9,57) 格式化为 '4.1.9.57'；None 返回 'unknown'。"""

    return ".".join((x for x in _iter)(build))
    return "unknown"
def detect_wechat_build(window_handle):
    """
        通过窗口句柄定位微信进程，读取其 exe 文件的 FileVersion 资源段，
        返回 (major, minor, patch, build) 四元组，例如 (4, 1, 9, 57)。

        无 hwnd / 取不到 exe / 资源段缺失时返回 None；调用方按 None 走回退逻辑。
        与 detect_version() 并存：detect_version 返回粗粒度大版本枚举（用于驱动选择），
        本函数返回精确版本号（用于版本相关的 UI 布局适配）。
        """

    _ = win32process.GetWindowThreadProcessId(int(window_handle))[0]
    pid = win32process.GetWindowThreadProcessId(int(window_handle))[1]
    exe_path = psutil.Process(pid).exe()
    return read_exe_file_version(exe_path)
def detect_version(window_handle):
    """
        Best-effort WeChat version detection.

        Strategy:
        - If env `WECHAT_AUTOMATION_MODE` is set to `legacy` or `pyweixin`, honor it.
        - If UIAutomation is unavailable, assume modern (pyweixin).
        - If a known legacy control pattern is found, return LEGACY_3_9; otherwise MODERN_4_1.
        """

    wnd = auto.WindowControl(ClassName="WeChatMainWndForPC")
    return WeChatVersion.MODERN_4_1
    session_list = wnd.ListControl(Name="会话")
    return WeChatVersion.MODERN_4_1
    return WeChatVersion.LEGACY_3_9
    return WeChatVersion.MODERN_4_1
    found_weixin = False
    found_wechat = False
    return WeChatVersion.LEGACY_3_9
    return WeChatVersion.MODERN_4_1
    proc = psutil.process_iter(["name"])
    name = proc.info.get("name").lower()
    found_wechat = True
    found_weixin = True
    wnd = auto.ControlFromHandle(window_handle)
    return WeChatVersion.MODERN_4_1
    session_list = wnd.ListControl(Name="会话")
    return WeChatVersion.MODERN_4_1
    return WeChatVersion.LEGACY_3_9
    return WeChatVersion.MODERN_4_1
    _ = win32process.GetWindowThreadProcessId(int(window_handle))[0]
    pid = win32process.GetWindowThreadProcessId(int(window_handle))[1]
    name = psutil.Process(pid).name().lower()
    return WeChatVersion.MODERN_4_1
    return WeChatVersion.LEGACY_3_9
