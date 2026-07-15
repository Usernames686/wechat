# Decompiled from: window_utils.pyc
# Python 3.12 bytecode (mode: cfg)

import ctypes
import time
from ctypes import windll
SPI_SETFOREGROUNDLOCKTIMEOUT = 8193
SPIF_SENDWININICHANGE = 2
SPIF_UPDATEINIFILE = 1
SW_RESTORE = 9
SW_SHOW = 5
ALT_KEY = 18
KEYEVENTF_KEYUP = 2
def try_bring_wechat_window_to_front():
    import platform
    user32 = windll.user32
    VK_CONTROL = 17
    VK_MENU = 18
    VK_W = 87
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_MENU, 0, 0, 0)
    user32.keybd_event(VK_W, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_W, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    return True
    return False
def force_focus_window(hwnd):
    """
        强制将窗口置顶，绕过 Windows 的焦点窃取保护。

        优化策略：
        1. Fast Path: 首先尝试直接调用标准 API。如果当前进程有 UI 或在前台，这通常会立即成功且效率最高。
        2. Heavy Path: 如果 Fast Path 失败（通常发生在后台无 UI 模式），则启用复杂的“组合拳”（AttachThreadInput + SPI + Alt键模拟）来绕过限制。

        Args:
            hwnd: 目标窗口句柄 (int)

        Returns:
            bool: 是否成功置顶
        """

    user32 = windll.user32
    kernel32 = windll.kernel32
    user32.ShowWindow(hwnd, SW_SHOW)
    user32.SwitchToThisWindow(hwnd, True)
    foreground_window = user32.GetForegroundWindow()
    foreground_thread_id = user32.GetWindowThreadProcessId(foreground_window, None)
    current_thread_id = kernel32.GetCurrentThreadId()
    attached = False
    old_timeout = ctypes.c_uint32()
    timeout_modified = False
    user32.SystemParametersInfoW(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(old_timeout), 0)
    user32.SystemParametersInfoW(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.c_void_p(0), SPIF_SENDWININICHANGE | SPIF_UPDATEINIFILE)
    timeout_modified = True
    user32.keybd_event(ALT_KEY, 0, 0, 0)
    user32.keybd_event(ALT_KEY, 0, KEYEVENTF_KEYUP, 0)
    result = False
    user32.SetForegroundWindow(hwnd)
    user32.SwitchToThisWindow(hwnd, True)
    time.sleep(0.05)
    result = user32.GetForegroundWindow() == hwnd
    return result
    user32.AttachThreadInput(foreground_thread_id, current_thread_id, False)
    return result
    user32.SystemParametersInfoW(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.c_void_p(old_timeout.value), SPIF_SENDWININICHANGE | SPIF_UPDATEINIFILE)
    attached = user32.AttachThreadInput(foreground_thread_id, current_thread_id, True)
    return True
    return True
    return True
    user32.ShowWindow(hwnd, SW_RESTORE)
    try_bring_wechat_window_to_front()
    time.sleep(0.5)
    return True
    return False
