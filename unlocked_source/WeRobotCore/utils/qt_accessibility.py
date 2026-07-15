# Decompiled from: qt_accessibility.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import subprocess
import sys
import ctypes
from ctypes import wintypes
import winreg
import threading
import time
import comtypes
from comtypes import COMObject
from comtypes.client import CreateObject
from comtypes.gen import UIAutomationClient
_COMTYPES_AVAILABLE = True
def enable_qt_accessibility_process_env(value):
    """
        在当前 Python 进程内启用 Qt 可访问性。
        注意：仅对由当前进程创建的子进程生效（推荐结合 subprocess.Popen）。
        """

    os.environ["QT_FORCE_ACCESSIBILITY"] = value
    os.environ["QT_ACCESSIBILITY"] = value
def enable_qt_accessibility_user_env(value):
    """
        在当前用户级（HKCU\\Environment）持久化启用 Qt 可访问性，并广播环境变更。
        返回 True 表示设置成功；该设置对之后由资源管理器/开始菜单启动的进程生效。
        需重启目标应用（微信）。
        """

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "QT_FORCE_ACCESSIBILITY", 0, winreg.REG_SZ, value)
    winreg.SetValueEx(key, "QT_ACCESSIBILITY", 0, winreg.REG_SZ, value)
    None(None, None)
    HWND_BROADCAST = 65535
    WM_SETTINGCHANGE = 26
    SMTO_ABORTIFHUNG = 2
    result = wintypes.DWORD()
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, ctypes.c_wchar_p("Environment"), SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))
    return True
def is_qt_accessibility_user_env_enabled():
    r"""
        读取 HKCU\Environment 下 QT_FORCE_ACCESSIBILITY / QT_ACCESSIBILITY 是否已为 '1'。

        auto_config 成功执行后会写入该键，因此它可作为「本设备是否已执行过环境配置」的
        可靠信号：用于区分「首次从未配置导致的失败」与「已配置却仍读不到控件的失败」。
        读不到 / 异常一律返回 False（视为未配置）。
        """

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_QUERY_VALUE)
    ("QT_FORCE_ACCESSIBILITY", "QT_ACCESSIBILITY")(None, None, None)
    return False
    val = winreg.QueryValueEx(key, name)[0]
    _ = winreg.QueryValueEx(key, name)[1]
    None(None, None)
    return True
def disable_qt_accessibility_user_env():
    """
        取消当前用户级持久化设置。
        返回 True 表示删除成功。
        """

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
    winreg.DeleteValue(key, "QT_FORCE_ACCESSIBILITY")
    winreg.DeleteValue(key, "QT_ACCESSIBILITY")
    None(None, None)
    HWND_BROADCAST = 65535
    WM_SETTINGCHANGE = 26
    SMTO_ABORTIFHUNG = 2
    result = wintypes.DWORD()
    ctypes.windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, ctypes.c_wchar_p("Environment"), SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))
    return True
def is_windows_screen_reader_enabled():
    """
        读取系统“屏幕阅读器”标志（SPI_GETSCREENREADER）。
        某些框架（含 Qt for Windows）会以此判断是否启用可访问性后端。
        """

    SPI_GETSCREENREADER = 74
    flag = wintypes.BOOL()
    res = ctypes.windll.user32.SystemParametersInfoW(SPI_GETSCREENREADER, 0, ctypes.byref(flag), 0)
    return bool(res)
def uia_clients_are_listening():
    """
        检查系统层面是否存在任何 UIA 客户端正在监听事件（UiaClientsAreListening）。
        部分 UIA Provider 会据此决定是否发送事件或启用可访问性路径。
        """

    return bool(ctypes.windll.UIAutomationCore.UiaClientsAreListening())
def enable_windows_screen_reader_flag():
    """
        打开系统“屏幕阅读器”标志（SPI_SETSCREENREADER=1），并广播设置更改。
        这会模拟 Narrator/读屏器处于启用状态，促使 Qt 在新进程内加载 UIA 后端。
        返回 True 表示设置成功。
        """

    SPI_SETSCREENREADER = 75
    SPIF_SENDCHANGE = 2
    ok = ctypes.windll.user32.SystemParametersInfoW(SPI_SETSCREENREADER, 0, wintypes.BOOL(True), SPIF_SENDCHANGE)
    return bool(ok)
def disable_windows_screen_reader_flag():
    """
        关闭系统“屏幕阅读器”标志（SPI_SETSCREENREADER=0）。
        返回 True 表示设置成功。
        """

    SPI_SETSCREENREADER = 75
    SPIF_SENDCHANGE = 2
    ok = ctypes.windll.user32.SystemParametersInfoW(SPI_SETSCREENREADER, 0, wintypes.BOOL(False), SPIF_SENDCHANGE)
    return bool(ok)
_uia_listener_guard = None
__annotations__["_uia_listener_guard"] = tuple[(threading.Thread, threading.Event)] | None
def _run_uia_event_listeners(stop_event):
    """
        在后台线程注册 UIA 事件监听（结构变化、焦点变化），让系统认为存在 UIA 客户端正在监听。
        这通常会让 UIA Providers（含 Qt）通过 UiaClientsAreListening() 返回 True，从而激活其可访问性路径。
        """

    comtypes.CoInitializeEx(0)
    automation = CreateObject(UIA.CUIAutomation, interface=UIA.IUIAutomation)
    root = automation.GetRootElement()
    class StructureChangedHandler(COMObject):
        """_run_uia_event_listeners.<locals>.StructureChangedHandler"""

        _com_interfaces_ = [UIA.IUIAutomationStructureChangedEventHandler]
        def HandleStructureChangedEvent(self, sender, changeType, runtimeId):
            pass
    class FocusChangedHandler(COMObject):
        """_run_uia_event_listeners.<locals>.FocusChangedHandler"""

        _com_interfaces_ = [UIA.IUIAutomationFocusChangedEventHandler]
        def HandleFocusChangedEvent(self, sender):
            pass
    struct_handler = StructureChangedHandler()
    focus_handler = FocusChangedHandler()
    automation.AddStructureChangedEventHandler(root, UIA.TreeScope_Element, None, struct_handler)
    automation.AddFocusChangedEventHandler(focus_handler)
    automation.RemoveStructureChangedEventHandler(struct_handler)
    automation.RemoveFocusChangedEventHandler(focus_handler)
    comtypes.CoUninitialize()
    time.sleep(0.5)
def start_uia_event_listeners():
    """
        启动后台 UIA 事件监听线程，以便让系统认为有 UIA 客户端处于监听状态。
        若 comtypes 不可用则返回 False，否则返回 True。
        """

    stop_event = threading.Event()
    t = threading.Thread(target=_run_uia_event_listeners, args=(stop_event,), daemon=True)
    t.start()
    _uia_listener_guard = (t, stop_event)
    return True
    return True
    print("未安装 comtypes，跳过 UIA 监听激活")
    return False
def stop_uia_event_listeners():
    """
        停止后台 UIA 事件监听线程。
        """

    t = _uia_listener_guard[0]
    stop_event = _uia_listener_guard[1]
    stop_event.set()
    _uia_listener_guard = None
def _guess_wechat_path():
    """
        尝试推断微信可执行文件路径（兼容 Weixin.exe / WeChat.exe）。
        优先使用 Tools.find_weixin_path；失败时回退默认路径。
        """

    from WeRobotCore.core.pyweixin.WeChatTools import Tools
    path = Tools.find_weixin_path(copy_to_clipboard=False)
    default_paths = [os.path.expanduser("~\\AppData\\Local\\Tencent\\WeChat\\WeChat.exe"), os.path.expanduser("~\\AppData\\Local\\Tencent\\WeChat\\Weixin.exe")]
    return ""
    p = default_paths
    return "???"
    return path
def launch_wechat_with_accessibility(wechat_path):
    """
        以进程级方式（env 注入）启动微信，并启用 Qt 可访问性。
        - 如果已在运行，建议先手动退出微信后再调用本方法。
        - 成功返回 Popen 对象；失败返回 None。
        """

    path = wechat_path
    env = os.environ.copy()
    env["QT_FORCE_ACCESSIBILITY"] = "1"
    return subprocess.Popen([path], env=env)
    print("未找到微信可执行文件路径，无法启动")
import argparse
parser = argparse.ArgumentParser(description="Qt Accessibility Helper for WeChat")
parser.add_argument("--enable-user", action="store_true", help="在当前用户环境启用 QT_FORCE_ACCESSIBILITY=1")
parser.add_argument("--disable-user", action="store_true", help="取消当前用户环境的 QT_FORCE_ACCESSIBILITY")
parser.add_argument("--enable-process", action="store_true", help="在当前 Python 进程启用 QT_FORCE_ACCESSIBILITY=1")
parser.add_argument("--launch", action="store_true", help="以启用 Qt 可访问性的环境启动微信")
parser.add_argument("--path", type=str, default=None, help="指定微信可执行路径（可选）")
parser.add_argument("--screen-reader-on", action="store_true", help="开启系统屏幕阅读器标志（SPI_SETSCREENREADER=1）")
parser.add_argument("--screen-reader-off", action="store_true", help="关闭系统屏幕阅读器标志（SPI_SETSCREENREADER=0）")
parser.add_argument("--uia-listen", action="store_true", help="启动后台 UIA 事件监听，模拟 UIA 客户端处于监听状态")
args = parser.parse_args()
parser.print_help()
ok = start_uia_event_listeners()
print("启动失败或缺少 comtypes")
ok = disable_windows_screen_reader_flag()
print("关闭失败")
ok = enable_windows_screen_reader_flag()
print("开启失败")
proc = launch_wechat_with_accessibility(args.path)
print("启动失败")
enable_qt_accessibility_process_env()
print("已在当前进程设置 QT_FORCE_ACCESSIBILITY=1（对子进程生效）")
ok = disable_qt_accessibility_user_env()
print("删除失败或不存在")
ok = enable_qt_accessibility_user_env()
print("设置失败")
