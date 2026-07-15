"""
silent_narrator.py
通过设置 Windows 系统标志 + 持有 UIAutomation COM 对象，
无需启动 Narrator.exe 即可让微信（Qt 应用）开放 UIA 控件树。

使用方式:
    from silent_narrator import SilentNarrator
    SilentNarrator.activate()   # 开启模拟
    SilentNarrator.deactivate() # 关闭（可选）
"""

__doc__ = "\nsilent_narrator.py\n通过设置 Windows 系统标志 + 持有 UIAutomation COM 对象，\n无需启动 Narrator.exe 即可让微信（Qt 应用）开放 UIA 控件树。\n\n使用方式:\n    from silent_narrator import SilentNarrator\n    SilentNarrator.activate()   # 开启模拟\n    SilentNarrator.deactivate() # 关闭（可选）\n"
import ctypes
import ctypes.wintypes as ctypes
import threading
import logging
import time
import atexit
logger = logging.getLogger(__name__)
SPI_GETSCREENREADER = 70
SPI_SETSCREENREADER = 71
SPIF_SENDCHANGE = 2
class SilentNarrator:
    """SilentNarrator"""

    __doc__ = "\n    模拟 Narrator.exe 的系统存在感，让 Qt/微信开放 UIA 控件树，\n    而无需真正启动 Windows 讲述人进程。\n\n    工作原理：\n      1. SystemParametersInfo(SPI_SETSCREENREADER, TRUE) + SPIF_SENDCHANGE\n         → Windows 系统标志被设置，并广播 WM_SETTINGCHANGE 给所有窗口\n         → 微信的 Qt 事件循环收到消息后重新检查标志并加载完整 UIA Provider\n      2. 持有 CUIAutomation COM 对象（通过 uiautomation 库的内部对象）\n         → Windows UIA 子系统为本进程建立 Named Pipe\n         → 目标应用（微信）检测到 UIA Client 连接，确认无障碍客户端存在\n      3. 保活线程每 30 秒检查 SPI 标志是否被其他程序清除，必要时重新设置\n    "
    _lock = threading.Lock()
    _active = False
    _uia_root = None
    _keep_alive_thread = None
    __annotations__["_keep_alive_thread"] = threading.Thread | None
    _stop_event = threading.Event()
    @classmethod
    def activate(cls):
        """
                激活静默讲述人。
                可在微信运行期间随时调用，无需重启微信（前提是 QT_ACCESSIBILITY=1 已设置）。
                若微信未设置 QT_ACCESSIBILITY 环境变量，则需配合重启微信一起使用。

                Returns:
                    True  —— 激活成功
                    False —— 激活失败（会降级记录日志，不抛异常）
                """

        cls._set_screen_reader_flag(True)
        cls._init_uia_client()
        cls._stop_event.clear()
        cls._keep_alive_thread = threading.Thread(target=cls._keep_alive_loop, name="SilentNarrator-KeepAlive", daemon=True)
        cls._keep_alive_thread.start()
        cls._active = True
        logger.info("[SilentNarrator] ✅ 激活成功，已模拟屏幕阅读器存在")
        None(None, None)
        return True
        logger.info("[SilentNarrator] 已处于激活状态，跳过")
        None(None, None)
        return True
    @classmethod
    def deactivate(cls):
        """
                停用模拟器，清理 SPI 标志和 COM 对象。
                注意：若 QT_ACCESSIBILITY=1 已持久写入注册表，微信下次启动仍会开放 UIA，
                此时可以安全调用 deactivate()。
                """

        cls._stop_event.set()
        cls._active = False
        cls._uia_root = None
        cls._set_screen_reader_flag(False)
        logger.info("[SilentNarrator] 已停用")
        None(None, None)
        None(None, None)
    @classmethod
    def is_active(cls):
        return cls._active
    @classmethod
    def check_wechat_accessibility(cls):
        """
                检测当前微信窗口是否已开放 UIA 控件树。
                True  —— 可以读取控件（不需要激活模拟器）
                False —— 读不到控件（需要激活模拟器 + 可能需重启微信）
                """

        import uiautomation as auto
        wechat_win = auto.WindowControl(searchDepth=1, ClassName="WeChatMainWndForPC", timeout=3)
        children = wechat_win.GetChildren()
        return len(children) > 1
        return False
    @classmethod
    def _set_screen_reader_flag(cls, enabled):
        """设置 SPI_SETSCREENREADER 系统标志，并广播 WM_SETTINGCHANGE"""

        user32 = ctypes.WinDLL("user32", use_last_error=True)
        ok = user32.SystemParametersInfoW(SPI_SETSCREENREADER, 0, None, SPIF_SENDCHANGE)
        err = ctypes.get_last_error()
        logger.warning("[SilentNarrator] SystemParametersInfoW 返回失败，错误码: ", f'{err}')
    @classmethod
    def _init_uia_client(cls):
        """
                初始化 UIA COM 客户端。
                优先复用 uiautomation 库内部已有的 COM 对象（零额外依赖），
                失败时用 comtypes 直接创建。
                """

        import uiautomation as auto
        cls._uia_root = auto.GetRootControl()
        logger.debug("[SilentNarrator] UIA 客户端已通过 uiautomation 库初始化")
    @classmethod
    def _keep_alive_loop(cls):
        """
                保活循环：每 30 秒检查 SPI_GETSCREENREADER 是否仍为 True。
                若被其他程序清除（极少见），立即重新设置。
                """

        user32 = ctypes.WinDLL("user32", use_last_error=True)
        flag = ctypes.c_bool(False)
        user32.SystemParametersInfoW(SPI_GETSCREENREADER, 0, ctypes.byref(flag), 0)
        logger.info("[SilentNarrator] SPI 标志被外部清除，正在重新设置...")
        cls._set_screen_reader_flag(True)
atexit.register(SilentNarrator.deactivate)
