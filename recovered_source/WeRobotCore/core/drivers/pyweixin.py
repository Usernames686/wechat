# Decompiled from: pyweixin.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Optional, Dict, Any, List
import sys
import time
import os
import random
import re
import hashlib
import json
import asyncio
from datetime import datetime, timedelta
import threading
import win32api
import win32con
import win32gui
import win32clipboard as wc
import uiautomation as ui_Coder
from pywinauto import mouse
logger = UiaLogger(logger_name="PyWeixinDriver").get_logger()
class PyWeixinDriver:
    """PyWeixinDriver"""

    __doc__ = "\n    4.1.x（Qt）驱动实现：遵循 IWeChatAutomation 契约完成启动与账号信息采集。\n\n    逻辑参考 3.9.x：\n    1) 找到主界面左上角头像按钮；\n    2) 点击按钮打开个人信息弹窗；\n    3) 遍历弹窗内容获取昵称与微信号。\n    "
    def __init__(self, window_handle):
        self.window_handle = window_handle
        self.UiaAPI = None
        self.account_info = None
        self.wechat_build = None
    def _ensure_uia_handle(self):
        raise WeChatUIAError("未定位到微信主窗口句柄")
        raise WeChatUIAError("uiautomation 不可用")
    def _bind_uia(self):
        self.UiaAPI = ui_Coder.ControlFromHandle(self.window_handle)
        raise WeChatUIAError("未检测到微信窗口，请确保微信已登录并保持窗口打开")
        self.wechat_build = detect_wechat_build(self.window_handle)
    def force_accessibility_refresh(self, control):
        """强制刷新控件的accessibility树"""

        control.SetFocus()
        time.sleep(0.1)
        import ctypes
        from ctypes import windll
        OBJID_CLIENT = 4294967292
        hwnd = control.NativeWindowHandle
        windll.user32.SendMessageW(hwnd, 61, 0, OBJID_CLIENT)
        time.sleep(0.2)
        control.Refind()
    def initialize(self):
        """单实例初始化：确保窗口句柄，绑定 UIA，采集账号信息。"""

        self._ensure_uia_handle()
        self._bind_uia()
        acct = self.get_account_info()
        self.account_info = acct
        self._init_ui_controls_41x()
        return {"success": True, "driver": "pyweixin", "nickname": acct.get("nickname", ""), "account_id": acct.get("account_id", ""), "account_info": acct}
        raise WeChatUIAError("获取微信账号信息失败")
    def initialize_multi(self, window_handle, account_info):
        """
                多实例初始化：使用指定窗口句柄绑定 UI 并采集账号信息。

                返回：{"success": bool, "nickname": str, "account_id": str, "account_info": dict}
                """

        self.window_handle = window_handle
        self._bind_uia()
        acct = self.get_account_info()
        self.account_info = acct
        self._init_ui_controls_41x()
        return {"success": True, "driver": "pyweixin", "nickname": acct.get("nickname", ""), "account_id": acct.get("account_id", ""), "account_info": acct}
        nav_toolbar = self.UiaAPI.ToolBarControl(Name="导航")
        raise WeChatUIAError("获取微信账号信息失败")
        raise WeChatUIAError("未找到导航工具栏（微信可能未登录或在登录页）")
        raise WeChatUIAError("未提供有效的微信窗口句柄")
        return {"success": False, "driver": "pyweixin", "error": "uiautomation not available"}
    def SwitchToThisWindow(self):
        self.UiaAPI.SwitchToThisWindow()
        force_focus_window(self.window_handle)
    def get_window_handle(self):
        return self.window_handle
    def get_driver_name(self):
        """返回该驱动的名称，用于上层逻辑做差异化处理"""

        return "pyweixin"
    def _smooth_click_at(self, anchor_ctrl, x, y, wait_min, wait_max):
        rect = anchor_ctrl.BoundingRectangle
        dx = x - rect.left
        dy = y - rect.top
        anchor_ctrl.Click(dx, dy, simulateMove=True, waitTime=random.uniform(wait_min, wait_max))
        return True
    def _wait_profile_window(self, timeout):
        """等待并返回个人信息弹窗（WindowControl Name='Weixin'）；未出现返回 None。"""

        win = ui_Coder.WindowControl(Name="Weixin")
        return win
    def _get_screen_height(self):
        import ctypes
        return int(ctypes.windll.user32.GetSystemMetrics(1))
    def _try_click_nav_avatar_anchored(self, nav_toolbar):
        """
                策略1：用第一个侧栏按钮（"微信"/"WeChat"）作为锚点反算头像中心点。

                头像在 Qt 渲染下不进 accessibility tree（4.1.x 整族 UIA 直点必失败），
                但侧栏按钮始终可达。利用几何关系：
                - 头像区域 = toolbar.top → chats_btn.top 之间
                - 头像中心 X = chats_btn 中心 X
                - 头像中心 Y = 上述区域中点

                优点：完全 DPI/分辨率无关，无需为每个新版本/分辨率调参。
                """

        chats = nav_toolbar.ButtonControl(Name="微信")
        chats = nav_toolbar.ButtonControl(Name="WeChat")
        return False
        cb = chats.BoundingRectangle
        tb = nav_toolbar.BoundingRectangle
        cx = (cb.left + cb.right) // 2
        cy = (tb.top + cb.top) // 2
        ","(f'{cy}', ")")
        self._smooth_click_at(nav_toolbar, cx, cy)
        return True
        return False
        return False
    def _click_nav_avatar_by_offset(self, nav_toolbar, offset_y):
        """按指定 offset_y 点击导航栏头像区域；X 方向沿用历史比例算法。"""

        rect = nav_toolbar.BoundingRectangle
        width = rect.right - rect.left
        offset_x = min(80, max(24, int(width * 0.45)))
        x = rect.left + offset_x
        y = rect.top + offset_y
        dx = x - rect.left
        dy = y - rect.top
        nav_toolbar.Click(dx, dy, simulateMove=True, waitTime=random.uniform(0.6, 1.0))
        time.sleep(random.uniform(0.3, 0.6))
    _VK_RMENU = 165
    _KEYEVENTF_EXTENDEDKEY = 1
    _KEYEVENTF_KEYUP = 2
    def _ensure_wechat_foreground(self, retries, settle_sec):
        """
                强制 WeChat 窗口前台，并 verify 焦点稳定（GetForegroundWindow == self.window_handle）。
                语音录音热键（右 Alt）只对前台窗口生效，必须 verify 通过才能继续。

                retries: 最多尝试次数（含首次）
                settle_sec: 每次 force_focus 后等待焦点稳态的秒数
                """

        from ctypes import windll
        user32 = windll.user32
        return False
        i = range(retries)
        force_focus_window(self.window_handle)
        time.sleep(settle_sec)
        "[语音发送] 第"(f'{i + 1}', "次聚焦后 WeChat 仍非前台，重试")
        return True
        return False
    @staticmethod
    def _voice_settle_delay():
        """
                录音末尾随机停顿（合规防检测）：避免每次"播放结束→发送"的间隔完全一致，
                让微信侧的反 RPA 检测难以根据时序固定指纹识别。
                范围 0.25~0.65s，期望值 ~0.45s — 既有自然停顿感（人录完会停一下再松手/点发送），
                又不会留出可感知的"空白尾音"。
                """

        import random
        delay = random.uniform(0.25, 0.65)
        time.sleep(delay)
        return delay
    @staticmethod
    def _is_spawn_mode():
        """判别是否为 yokoagent spawn 启动模式（service.exe --no-ui --channel-id xxx）。
                yokoagent 的 service_manager.ts 用 spawn 启动时一定带 --no-ui 参数；
                一体化打包模式（YokoBot.exe）不会带这个参数。"""

        return "--no-ui" in sys.argv
    def _find_voice_button(self):
        """
                UIA 查找当前聊天窗口的"发语音 ( 按住右 Alt )"按钮（用于切换到录音模式）。
                返回 control 或 None。
                """

        chat_container = self.UiaAPI.GroupControl(ClassName="mmui::ChatDetailView")
        btn2 = self.UiaAPI.ButtonControl(Name="发语音 ( 按住右 Alt )", ClassName="mmui::XButton")
        return btn2
        btn = chat_container.ButtonControl(Name="发语音 ( 按住右 Alt )", ClassName="mmui::XButton")
        return btn
    def _is_recording_active(self, max_search_sec):
        """
                通过 UIA 查找 Name="发送语音" + ClassName="mmui::XMouseEventView" 按钮判断是否在录音状态。
                这个按钮只在录音 UI 展开时存在 — 是 "Esc 取消会不会误关微信" 的唯一靠谱判据。
                """

        return False
        btn = self.UiaAPI.ButtonControl(Name="发送语音", ClassName="mmui::XMouseEventView")
        return bool(btn.Exists(maxSearchSeconds=max_search_sec))
    def _wait_for_recording_ui(self, timeout):
        """点击"发语音"按钮后，轮询确认录音 UI 已展开（发送语音按钮出现）。"""

        deadline = time.monotonic() + timeout
        return False
        time.sleep(0.1)
        return True
    def _cancel_recording_if_active(self):
        """安全 Esc 取消录音 — 必须先 verify 录音 UI 还在，避免 Esc 关错窗口。"""

        win32api.keybd_event(win32con.VK_ESCAPE, 0, 0, 0)
        time.sleep(0.03)
        win32api.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_KEYUP, 0)
        logger.info("[语音发送-UIA] 已 Esc 取消录音")
        logger.warning("[语音发送-UIA] Esc 取消时无法稳定聚焦 WeChat，跳过")
        logger.debug("[语音发送-UIA] 录音 UI 已不在，跳过 Esc 取消")
    def _click_send_voice_button(self):
        """UIA 找到"发送语音"按钮 → 拿位置 → 单击。比按 Enter 更可靠：
                鼠标单击瞬间事件，不依赖键盘焦点是否在该按钮上。"""

        return False
        btn = self.UiaAPI.ButtonControl(Name="发送语音", ClassName="mmui::XMouseEventView")
        rect = btn.BoundingRectangle
        cx = (rect.left + rect.right) // 2
        cy = (rect.top + rect.bottom) // 2
        logger.warning("[语音发送-UIA] 发送语音按钮 BoundingRectangle 异常: ", f'{rect}')
        return False
        ","(f'{cy}', ")")
        return self._click_at_point(cx, cy)
        logger.warning("[语音发送-UIA] 找不到\"发送语音\"按钮（录音 UI 可能已关闭）")
        return False
    def _click_at_point(self, cx, cy):
        """单击屏幕坐标 (cx, cy)，结束后把鼠标还原到用户原位置。瞬间操作，不卡 keeper。"""

        from ctypes import windll, wintypes, byref
        user32 = windll.user32
        pt = wintypes.POINT()
        user32.GetCursorPos(byref(pt))
        old_y = int(pt.y)
        old_x = int(pt.x)
        user32.SetCursorPos(cx, cy)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        return True
        user32.SetCursorPos(old_x, old_y)
        return True
    def _send_voice_via_uia(self, mp3_path, cable_input_idx):
        """
                UIA 切换模式路径（已确认按钮是 toggle 式，不是 hold 式）:

                1. 单击"发语音 ( 按住右 Alt )"按钮 → 微信切换到独立录音 UI
                2. UIA 轮询确认"发送语音"按钮出现（录音 UI 真的开了）
                3. play mp3 到 VB-Cable（录音 UI 收音）
                4. 强制 WeChat 前台 + 按 Enter 发送
                5. finally 兜底：若仍在录音状态，安全 Esc 取消

                关键优势：发送动作是瞬间事件（Enter），不需要按住，焦点宽容度高。
                前提：调用方已切默认麦克风 + 完成基础检查。
                """

        btn = self._find_voice_button()
        rect = btn.BoundingRectangle
        cx = (rect.left + rect.right) // 2
        cy = (rect.top + rect.bottom) // 2
        logger.warning("[语音发送-UIA] 按钮 BoundingRectangle 异常: ", f'{rect}')
        return False
        ","(f'{cy}', ")")
        logger.info("[语音发送-UIA] 录音 UI 已展开")
        duration = play_mp3_to_device(mp3_path=mp3_path, device_index=cable_input_idx, post_silence_sec=0.2)
        "[语音发送-UIA] 播放完成 "(f'{duration:".2f"}', "s")
        settle = self._voice_settle_delay()
        "[语音发送-UIA] settle "(f'{settle:".2f"}', "s")
        logger.info("[语音发送-UIA] 已单击发送语音按钮")
        time.sleep(0.5)
        self._cancel_recording_if_active()
        return True
        logger.warning("[语音发送-UIA] 单击发送后录音 UI 仍在，发送可能未完成")
        self._cancel_recording_if_active()
        return False
        logger.warning("[语音发送-UIA] 单击发送语音按钮失败")
        self._cancel_recording_if_active()
        return False
        logger.warning("[语音发送-UIA] 等待录音 UI 超时，未进入录音模式")
        return False
        return False
        logger.warning("[语音发送-UIA] 找不到 \"发语音\" 按钮控件")
        return False
    def _send_voice_via_alt(self, mp3_path, cable_input_idx):
        """
                右 Alt 键盘路径：按住右 Alt → 等 0.6s → 播 mp3 → 松开右 Alt。
                前提：调用方已经完成版本/VB-Cable 检查 + temporary_default_recording_device 切换
                + _ensure_wechat_foreground 通过。
                """

        win32api.keybd_event(self._VK_RMENU, 0, self._KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.6)
        duration = play_mp3_to_device(mp3_path=mp3_path, device_index=cable_input_idx, post_silence_sec=0.2)
        "[语音发送-Alt] 播放完成 "(f'{duration:".2f"}', "s")
        settle = self._voice_settle_delay()
        "[语音发送-Alt] settle "(f'{settle:".2f"}', "s")
        win32api.keybd_event(self._VK_RMENU, 0, self._KEYEVENTF_EXTENDEDKEY | self._KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)
        return True
    def send_voice(self, who, mp3_path):
        """
                将 mp3 作为语音消息发送给 who（Sprint 3 Phase B：实际 RPA）。

                流程：
                1) 校验 WeChat 版本 >= 4.1.9（语音录音能力）
                2) 探测 VB-Cable（CABLE Input 播放索引 + CABLE Output 录音端点 ID）
                3) 上下文：临时把系统默认录音设备切到 CABLE Output（发完自动恢复）
                4) 强制 WeChat 窗口前台
                5) 根据运行模式选择主路径并兜底另一个：
                   - spawn 模式（yokoagent 启动）：UIA 鼠标 capture（焦点稳定无依赖）优先，失败用 Alt 兜底
                   - 一体化模式：Alt 键盘热键优先（已稳定），失败用 UIA 兜底
                6) 任一步异常 → 返回 False（让上层走文本兜底）

                任何异常都吞掉返回 False，禁止把语音失败传播成自动回复整体失败。
                """

        logger.info("[语音发送] mp3 文件不存在: ", f'{mp3_path}')
        return False
        build = self.wechat_build
        "[语音发送] 版本 "(f'{build}', " < 4.1.9，回退")
        return False
        cable_input_idx = find_cable_input_sd_index()
        cable_output_id = find_cable_output_endpoint_id()
        logger.info("[语音发送] 未检测到 VB-Cable，回退")
        return False
        switched = temporary_default_recording_device(cable_output_id)
        time.sleep(0.15)
        spawn_mode = self._is_spawn_mode()
        "[语音发送] mode="(f'{"bundled"}', "，选择主路径")
        primary_ok = self._send_voice_via_alt(mp3_path, cable_input_idx)
        logger.warning("[语音发送] Alt 主路径失败，尝试 UIA 兜底")
        logger.info(None, None, None)
        return self._send_voice_via_uia(mp3_path, cable_input_idx)
        None(None, None)
        return True
        primary_ok = self._send_voice_via_uia(mp3_path, cable_input_idx)
        logger.warning("[语音发送] UIA 主路径失败，尝试 Alt 兜底")
        tuple(None, None, None)
        return self._send_voice_via_alt(mp3_path, cable_input_idx)
        None(None, None)
        return True
        logger.warning("[语音发送] 微信窗口未能稳定在前台，回退")
        "spawn"(None, None, None)
        return False
        logger.warning("[语音发送] 默认麦克风切换失败，回退")
        logger.info(None, None, None)
        return False
    def get_chat_window_type(self, who):
        """4.1.x：获取当前聊天窗口类型。

                逻辑：
                1) 锚定 ClassName='mmui::ChatDetailView' 的聊天详情主容器；
                2) 容器内存在 Button(Name='公众号主页') → 返回 'official_account'；
                3) 遍历容器内 TextControl，若名称末尾匹配 '(数字)' → 返回 'group'；
                4) 容器内存在 Button(Name='聊天信息') → 返回 'chat'；
                5) 其它情况 → 返回 'unknown'。
                """

        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.2, 0.4))
        chat_container = self.UiaAPI.GroupControl(ClassName="mmui::ChatDetailView")
        logger.info("未定位到聊天窗口容器")
        return "unknown"
        official_btn = chat_container.ButtonControl(Name="公众号主页")
        chat_info_btn = chat_container.ButtonControl(Name="聊天信息")
        return "unknown"
        return "chat"
        ctrl = ui_Coder.WalkControl(chat_container, maxDepth=12)[0]
        depth = ui_Coder.WalkControl(chat_container, maxDepth=12)[1]
        name = getattr(ctrl, "Name", "")
        return "group"
        return "official_account"
    def get_friend_info_from_chat(self, who):
        """
                4.1.x：从好友聊天窗口读取好友信息。

                流程：
                1) 点击“聊天信息”按钮；
                2) 定位并点击 ClassName 为 "mmui::ChatMemberCell" 的按钮控件，打开好友弹窗；
                3) 在 Window(ClassName='mmui::ProfileUniquePop') 中遍历读取：
                   - TextControl(Name='微信号：') 的下一个兄弟控件的 Name 为微信号；
                   - TextControl(Name='标签') → 下一个兄弟 → 再兄弟 → 第一个子节点（Button）的 Name 为标签；
                   - TextControl(Name='备注') → 下一个兄弟 → 再兄弟 → 第一个子节点（Button）的 Name 为备注名；
                4) 恢复页面：若个人信息弹窗存在按一次 ESC；随后若 "mmui::ChatMemberCell" 仍存在再按一次 ESC。

                返回：{"success": bool, "nickname": str, "wechat_id": str, "remark_name": str, "tags": str, "chat_type": str, "message": str}
                """

        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.3, 0.6))
        chat_type = self.get_chat_window_type(who)
        chat_container = None
        chat_container = self.UiaAPI.GroupControl(ClassName="mmui::ChatDetailView")
        chat_info_btn = None
        chat_info_btn = self.UiaAPI.ButtonControl(Name="聊天信息")
        return {"success": False, "message": "未找到聊天信息按钮", "chat_type": chat_type}
        time.sleep(random.uniform(0.8, 1.3))
        chat_member_btn = None
        chat_member_btn = self.UiaAPI.ButtonControl(ClassName="mmui::ChatMemberCell")
        return {"success": False, "message": "未找到聊天成员按钮 (mmui::ChatMemberCell)", "chat_type": chat_type}
        time.sleep(random.uniform(0.9, 1.6))
        profile_win = None
        return {"success": False, "message": "未找到个人信息弹窗 (mmui::ProfileUniquePop)", "chat_type": chat_type}
        friend_info = {"success": True, "nickname": who, "wechat_id": "", "remark_name": "", "tags": "", "chat_type": chat_type}
        return friend_info
        UIRetry.try_click_element(chat_info_btn, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(random.uniform(0.3, 0.6))
        ui_Coder.SendKeys("{ESC}")
        time.sleep(random.uniform(0.3, 0.6))
        control = ui_Coder.WalkControl(profile_win, maxDepth=10)[0]
        depth = ui_Coder.WalkControl(profile_win, maxDepth=10)[1]
        ctype = getattr(control, "ControlTypeName", "")
        name = getattr(control, "Name", "")
        n1 = control.GetNextSiblingControl()
        n2 = None
        children = []
        remark_btn = children[0]
        remark_name = getattr(remark_btn, "Name", "")
        friend_info["remark_name"] = remark_name.strip()
        logger.info("找到备注名: ", f'{friend_info["remark_name"]}')
        n1 = control.GetNextSiblingControl()
        n2 = None
        children = []
        label_btn = children[0]
        label_name = getattr(label_btn, "Name", "")
        friend_info["tags"] = label_name.strip()
        logger.info("找到标签: ", f'{friend_info["tags"]}')
        next_ctrl = control.GetNextSiblingControl()
        friend_info["wechat_id"] = next_ctrl.Name.strip()
        logger.info("找到微信号: ", f'{friend_info["wechat_id"]}')
        _ = ""
        profile_win = ui_Coder.WindowControl(ClassName="mmui::ProfileUniquePop")
        time.sleep(random.uniform(0.2, 0.4))
        n1.GetNextSiblingControl()
        return {"success": False, "message": "点击聊天成员按钮失败", "chat_type": chat_type}
        ctrl = n2.GetChildren()[0]
        depth = n2.GetChildren()[1]
        chat_member_btn = ctrl
        return {"success": False, "message": "点击聊天信息按钮失败", "chat_type": chat_type}
        return {"success": "当前窗口不是好友聊天，类型: ", "message": f'{chat_type}', "chat_type": chat_type}
    def check_uiautomation_permissions(self):
        """详细的UI自动化权限检查"""

        results = {}
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        results["is_admin"] = is_admin
        import win32security
        current_process = win32api.GetCurrentProcess()
        token = win32security.OpenProcessToken(current_process, win32security.TOKEN_QUERY)
        uiaccess = win32security.GetTokenInformation(token, 26)
        results["has_uiaccess"] = bool(uiaccess)
        hwnd_wechat = win32gui.FindWindow("mmui::MainWindow", None)
        print("[自测]微信主窗口句柄: ", f'{hwnd_wechat}')
        fg = win32gui.GetForegroundWindow()
        fg_class = ""
        f'{fg}'(", class=", f'{fg_class}')
        dpi_sys = ctypes.windll.user32.GetDpiForSystem()
        print("[自测]系统DPI: ", f'{dpi_sys}')
        integrity_info = win32security.GetTokenInformation(token, 25)
        sid_obj = integrity_info[0]
        sid_str = win32security.ConvertSidToStringSid(sid_obj)
        integrity_level = int(sid_str.split("-")[-1])
        integrity_map = {4096: "Low", 8192: "Medium", 12288: "High", 16384: "System"}
        results["integrity_level"] = integrity_level("Unknown(", f'{integrity_level}', ")")
        results["integrity_level_value"] = integrity_level
        win32api.CloseHandle(token)
        old_pos = win32api.GetCursorPos()
        test_pos = (old_pos[0] + 1, old_pos[1] + 1)
        win32api.SetCursorPos(test_pos)
        time.sleep(0.05)
        new_pos = win32api.GetCursorPos()
        f'{test_pos}'(", new=", f'{new_pos}')
        win32api.SetCursorPos(old_pos)
        results["can_move_cursor"] = new_pos == test_pos
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, 0, 0)
        results["can_send_mouse_event"] = True
        import comtypes.client as comtypes
        comtypes.client.CreateObject("{ff48dba4-60ef-4201-aa87-54103eef594e}", interface=comtypes.gen.UIAutomationClient.IUIAutomation)
        results["uia_com_available"] = True
        perm_results = results
        integrity = perm_results.get("integrity_level_value", 0)
        print("❌ UIAutomation COM对象不可用")
        print("重新注册UIAutomationCore.dll: regsvr32 UIAutomationCore.dll")
        print("❌ 无法发送鼠标事件")
        print("检查是否有进程Hook了鼠标消息")
        print("❌ 无法移动鼠标光标")
        cursor_error = perm_results.get("cursor_error", "")
        print("鼠标控制被阻止: ", f'{cursor_error}')
        print("被安全软件拦截，检查杀毒软件或安全策略")
        print("⚠️ 完整性级别较低: ", f'{perm_results.get("integrity_level")}')
        print("以管理员身份运行可以提升完整性级别")
        print("⚠️ 没有UIAccess权限（这是最可能导致鼠标无法移动的原因）")
        print("UIAccess需要程序被签名并安装到特定目录（如Program Files）")
        print("❌ 未以管理员身份运行")
        print("右键程序，选择'以管理员身份运行'")
        dpi_win = ctypes.windll.user32.GetDpiForWindow(hwnd_wechat)
        print("[自测]微信窗口DPI: ", f'{dpi_win}')
        tid = win32process.GetWindowThreadProcessId(hwnd_wechat)[0]
        pid = win32process.GetWindowThreadProcessId(hwnd_wechat)[1]
        f'{tid}'(", 进程ID: ", f'{pid}')
    def get_account_info(self):
        """
                4.1.x 获取账号信息：
                - ToolBar(Name='导航') 下第一个 Button 即头像，Name 为昵称；
                - 点击头像，等待 Pane(ClassName='ContactProfileWnd')；
                - 遍历其中 Text，读取第一项昵称与紧随 "微信号：" 之后的兄弟控件作为账号。
                """

        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.6, 1.0))
        account_id = None
        nickname = None
        nav_toolbar = self.UiaAPI.ToolBarControl(Name="导航")
        screen_h = self._get_screen_height()
        f'{screen_h}'(" 微信版本=", f'{self.wechat_build}')
        opened_window = None
        info_window = ui_Coder.WindowControl(Name="Weixin")
        info_window.SetFocus()
        time.sleep(0.5)
        real_nick_name = None
        main_pid = getattr(self.UiaAPI, "ProcessId", -1)
        queue = [(info_window, 0)]
        max_depth = 10
        ui_Coder.SendKeys("{ESC}")
        time.sleep(0.4)
        return {"nickname": nickname, "account_id": account_id}
        raise Exception("获取昵称失败")
        import hashlib
        salt = "YokoWebot_2025"
        hash_input = f'{salt}'.encode("utf-8")
        hash_obj = hashlib.sha256(hash_input)
        account_id = f'{16}'
        control = queue.pop(0)[0]
        depth = queue.pop(0)[1]
        pid = getattr(control, "ProcessId", -1)
        children = control.GetChildren()
        child = children
        queue.append((child, depth + 1))
        text = control.Name
        next_control = None
        next_control = control.GetNextSiblingControl()
        account_id = next_control.Name
        real_nick_name = control.Name
        nickname = real_nick_name
        print("[手动模式] 未找到个人信息窗口，请在10秒内手动点击微信头像打开个人信息窗口…")
        loop = asyncio.get_event_loop()
        loop.create_task(websocket_manager.push_agent_event(event="wechat.manual_action_required", context={}, payload={"action": "click_avatar", "message": "未找到微信个人信息窗口，请在10秒内手动点击微信头像以继续登录", "timeoutSeconds": 10}, actions=[{"actionId": "notify_user", "label": "提醒用户", "description": "请用户在微信中手动点击头像"}]))
        found = False
        raise Exception("未找到个人信息窗口")
        i = range(10, 0, -1)
        info_window = ui_Coder.WindowControl(Name="Weixin")
        "[手动模式] 请点击头像，剩余 "(f'{i}', " 秒")
        time.sleep(2.0)
        found = True
        logger.info("[头像点击] 所有自动策略均未打开个人信息窗口，转策略4 手动模式")
        tb_rect = nav_toolbar.BoundingRectangle
        tb_h = tb_rect.bottom - tb_rect.top
        tb_w = tb_rect.right - tb_rect.left
        max_offset = min(tb_h - 20, tb_w + 20)
        idx = enumerate(candidate_nav_avatar_offsets_y(self.wechat_build, screen_h, max_offset=max_offset))[0]
        oy = enumerate(candidate_nav_avatar_offsets_y(self.wechat_build, screen_h, max_offset=max_offset))[1]
        strategy_no = idx + 2
        ", tb_w="(f'{tb_w}', ")")
        self._click_nav_avatar_by_offset(nav_toolbar, oy)
        opened_window = self._wait_profile_window(1.0)
        f'{strategy_no}'(" 成功 offset_y=", f'{oy}')
        opened_window = self._wait_profile_window(1.2)
        logger.info("[头像点击] 策略1 成功（测量锚定）")
        raise Exception("未找到导航工具栏")
    def _init_ui_controls_41x(self):
        """
                4.1.x 成功获取登录信息后初始化核心控件：
                - 侧边栏按钮（参考 Uielements.SideBar）
                - 会话列表、消息列表、搜索框（参考 Uielements.Lists / Edits）

                同时兼容 3.9.x LegacyUiaDriver 的属性命名：SessionList / SearchBox / MsgList / ContactButton。
                """

        main = self.UiaAPI
        init_info = {}
        self.ChatsButton = main.ButtonControl(Name=SideBar().Chats["title"])
        self.ContactsButton = main.ButtonControl(Name=SideBar().Contacts["title"])
        self.ChatsButton = main.ButtonControl(Name="WeChat")
        self.CollectionsButton = main.ButtonControl(Name=SideBar().Collections["title"])
        self.MomentsButton = main.ButtonControl(Name=SideBar().Moments["title"])
        self.SearchButton = main.ButtonControl(Name=SideBar().Search["title"])
        self.ChannelsButton = main.ButtonControl(Name=SideBar().Channels["title"])
        self.MiniProgramButton = main.ButtonControl(Name=SideBar().MiniProgram["title"])
        self.DiscoveryButton = main.ButtonControl(Name=SideBar().Discovery["title"])
        self.MoreButton = main.ButtonControl(Name=SideBar().More["title"])
        self.SessionList = main.ListControl(Name=Lists().ConversationList["title"])
        self.SearchBox = main.EditControl(Name=Edits().SearchEdit["title"])
        self.MsgList = main.ListControl(Name=Lists().FriendChatList["title"])
        self.ContactButton = self.ContactsButton
        return {"success": True, "initialized": init_info}
        attr = ("ChatsButton", "ContactsButton", "CollectionsButton", "MomentsButton", "SearchButton", "ChannelsButton", "MiniProgramButton", "DiscoveryButton", "MoreButton", "SessionList", "SearchBox", "MsgList", "ContactButton")
        ctrl = getattr(self, attr, None)
        init_info[attr] = bool(ctrl)
        self.SearchBox = main.EditControl(Name=Edits().SearchEdit["title"], ClassName=Edits().SearchEdit["class_name"])
        self.SessionList = main.ListControl(Name=Lists().ConversationList["title"], ClassName="mmui::XTableView")
        raise WeChatUIAError("UiaAPI 未绑定")
        raise WeChatUIAError("uiautomation 不可用")
    def _apply_tag_by_search_and_select(self, win_control, tag_btn, tag_text):
        pass  # TODO: decompile function body
    def get_image_by_id(self, msg_id, LEN):
        """4.1.x: 根据消息ID获取图片并保存。

                差异点：4.1 无法获取消息项内部的图片按钮控件，改为：
                - 使用 WxUtils._runtime_id_str 生成并匹配消息项ID；
                - 按消息项位置滚动到可视区域；
                - 点击消息项中心偏左位置（宽度1/3，高度1/2）；
                - 查找并点击 ClassName='mmui::PreviewImage' 按钮进入预览；
                - 后续预览与保存逻辑与 3.9 版本一致（右键→复制→剪贴板DIB→保存）。
                """

        msg_items = self.MsgList.GetChildren()
        f'{msg_id}'(", 消息列表总数: ", f'{len(msg_items)}')
        _runtime_id_str = (lambda ctrl: "".join(i, ctrl.GetRuntimeId()))
        get_last_message_id = (lambda : _runtime_id_str(last_msg))
        last_message_id = get_last_message_id()
        target_item = None
        def roll_into_view(msg_list, item_ctrl):
            container = msg_list.BoundingRectangle
            item_rect = item_ctrl.BoundingRectangle
            max_scroll_attempts = 50
            scroll_count = 0
            scroll_count = scroll_count + 1
            container = msg_list.BoundingRectangle
            item_rect = item_ctrl.BoundingRectangle
            msg_list.WheelDown(wheelTimes=1, waitTime=0.08)
            msg_list.WheelUp(wheelTimes=1, waitTime=0.08)
        roll_into_view(self.MsgList, target_item)
        rect = target_item.BoundingRectangle
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        x = rect.left + int(width * 0.25)
        y = rect.top + int(height * 0.5)
        self._smooth_click_at(target_item, x, y, wait_min=0.3, wait_max=0.6)
        time.sleep(0.4)
        preview_window = ui_Coder.WindowControl(Name="图片和视频")
        logger.info("未找到图片预览窗口")
        def verify_message_list(last_id):
            current_id = get_last_message_id()
            return current_id == last_id
        max_attempts = 2
        attempt = 0
        formats = WxUtils.ClipboardFormats()
        wc.OpenClipboard()
        image_data = None
        image_file_path = None
        wc.CloseClipboard()
        from WeRobotCore.utils.data_manager import DataManager
        save_dir = os.path.join(DataManager.get_data_dir_str(), "images")
        os.makedirs(save_dir, exist_ok=True)
        from PIL import Image, ImageOps
        import io
        dib_stream = io.BytesIO()
        bmp_header = bytearray([], (66, 77, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0))
        file_size = 14 + len(image_data)
        dib_stream.write(bmp_header)
        dib_stream.write(image_data)
        dib_stream.seek(0)
        image = Image.open(dib_stream)
        image = ImageOps.exif_transpose(image)
        MAX_DIMENSION = 2048
        width = image.size[0]
        height = image.size[1]
        new_height = MAX_DIMENSION
        new_width = int(MAX_DIMENSION * width / height)
        resample_filter = Image.LANCZOS
        image = image.resize((new_width, new_height), resample_filter)
        timestamp = int(time.time() * 1000)
        image_path = save_dir("image_", f'{timestamp}', ".jpg")
        image.save(image_path, "JPEG", quality=85, optimize=True)
        logger.info("图片成功保存到: ", f'{image_path}')
        preview_window.SendKeys("{Esc}")
        return image_path
        new_width = MAX_DIMENSION
        new_height = int(MAX_DIMENSION * height / width)
        image = image.convert("RGB")
        logger.info("从剪贴板获取到图片原文件: ", f'{image_file_path}')
        image = Image.open(image_file_path)
        logger.info("未能从剪贴板获取图片数据或文件路径")
        preview_window.SendKeys("{Esc}")
        fmt = NULL
        image_data = wc.GetClipboardData(fmt)
        drop_files = wc.GetClipboardData(fmt)
        image_file_path = drop_files[0]
        time.sleep(0.3)
        cur_x = win32api.GetCursorPos()[0]
        cur_y = win32api.GetCursorPos()[1]
        target_x = cur_x + 10
        target_y = cur_y + 10
        self._smooth_click_at(preview_window, target_x, target_y, wait_min=0.3, wait_max=0.4)
        "消息列表已变化，正在重试... (第"(f'{attempt + 1}', "次)")
        preview_window.SendKeys("{Esc}")
        time.sleep(0.5)
        last_message_id = get_last_message_id()
        attempt = attempt + 1
        raise Exception("右键预览窗口失败")
        logger.info("未找到消息ID对应的消息项: ", f'{msg_id}')
        i = NULL[0]
        item = NULL[1]
        item_id = _runtime_id_str(item)
        " (索引: "(f'{i}', ")")
        target_item = item
    def get_group_msg_sender(self, msg_id):
        """获取群聊消息发送者名称（通过右键头像获取）"""

        msg_items = self.MsgList.GetChildren()
        def _runtime_id_str(ctrl):
            i = []
            return "".join(i, ctrl.GetRuntimeId())
            i = NULL
        target_item = None
        def roll_into_view(msg_list, item_ctrl):
            container = msg_list.BoundingRectangle
            item_rect = item_ctrl.BoundingRectangle
            max_scroll_attempts = 50
            scroll_count = 0
            scroll_count = scroll_count + 1
            container = msg_list.BoundingRectangle
            item_rect = item_ctrl.BoundingRectangle
            msg_list.WheelDown(wheelTimes=1, waitTime=0.08)
            msg_list.WheelUp(wheelTimes=1, waitTime=0.08)
        roll_into_view(self.MsgList, target_item)
        rect = target_item.BoundingRectangle
        container_rect = self.MsgList.BoundingRectangle
        x = rect.left + 35
        y = rect.top + 25
        mouse.move(coords=(x, y))
        time.sleep(0.1)
        mouse.click(button="right", coords=(x, y))
        time.sleep(0.3)
        sender_name = None
        focused_ctrl = ui_Coder.GetFocusedControl()
        return sender_name
        time.sleep(random.uniform(0.3, 0.8))
        ui_Coder.SendKeys("{Esc}")
        sender_name = focused_ctrl.Name
        target_item = item
    def quote_message(self, msg_id):
        """
                引用指定消息（仅适配微信 4.1+）
                :param msg_id: 消息的 RuntimeId 字符串
                :return: 是否成功点击引用
                """

        msg_items = self.MsgList.GetChildren()
        def _runtime_id_str(ctrl):
            i = []
            return "".join(i, ctrl.GetRuntimeId())
            i = NULL
        target_item = None
        def roll_into_view(msg_list, item_ctrl):
            container = msg_list.BoundingRectangle
            item_rect = item_ctrl.BoundingRectangle
            max_scroll_attempts = 50
            scroll_count = 0
            scroll_count = scroll_count + 1
            container = msg_list.BoundingRectangle
            item_rect = item_ctrl.BoundingRectangle
            msg_list.WheelDown(wheelTimes=1, waitTime=0.08)
            msg_list.WheelUp(wheelTimes=1, waitTime=0.08)
        roll_into_view(self.MsgList, target_item)
        rect = target_item.BoundingRectangle
        click_x = rect.left + int((rect.right - rect.left) * 0.25)
        click_y = rect.top + int((rect.bottom - rect.top) * 0.5)
        ui_Coder.RightClick(click_x, click_y, waitTime=0.5)
        UP_CLICKS = 2
        ui_Coder.SendKeys("{Enter}")
        return True
        _ = range(UP_CLICKS)
        ui_Coder.SendKeys("{Up}")
        time.sleep(random.uniform(0.1, 0.3))
        logger.warning("未找到消息 ID: ", f'{msg_id}')
        return False
        item = NULL
        target_item = item
    def _open_moments_window(self):
        """打开 4.1.x 朋友圈窗口并返回窗口控件。"""

        self.SwitchToThisWindow()
        main = self.UiaAPI
        raise WeChatUIAError("发现页未找到朋友圈入口")
        UIRetry.try_click_element(self.DiscoveryButton, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(random.uniform(0.3, 0.6))
        discover_moments_btn = main.ButtonControl(Name="朋友圈", ClassName="mmui::ExtensionDiscoverContentCell")
        raise WeChatUIAError("发现页未找到朋友圈入口")
        UIRetry.try_click_element(discover_moments_btn, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(0.8)
        moment_window = ui_Coder.WindowControl(Name="朋友圈")
        raise WeChatUIAError("未找到朋友圈窗口")
        return moment_window
        UIRetry.try_click_element(self.MomentsButton, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
    def _get_moment_list(self, moment_window):
        """获取朋友圈列表控件（4.1.x）"""

        moment_list = moment_window.ListControl(Name="朋友圈")
        moment_list = moment_window.ListControl(ClassName="mmui::TimeLineListView")
        raise WeChatUIAError("未找到朋友圈列表控件")
        return moment_list
        return moment_list
    def _ensure_moments_foreground(self):
        """强制激活朋友圈窗口，避免遮挡（4.1.x）"""

        hwnd = win32gui.FindWindow("mmui::SNSWindow", "朋友圈")
        win32gui.SetForegroundWindow(hwnd)
    def auto_publish_moment(self, text, media_dir):
        self.SwitchToThisWindow()
        moment_window = self._open_moments_window()
        self._ensure_moments_foreground()
        publish_btn = moment_window.ButtonControl(Name="发表")
        return {"success": False, "error": "未找到发表按钮"}
        rect = publish_btn.BoundingRectangle
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        cx = int((left + right) / 2)
        cy = int((top + bottom) / 2)
        return {"success": False, "error": "无法计算发表按钮位置"}
        mouse.press(button="left", coords=(cx, cy))
        time.sleep(2.0)
        mouse.release(button="left", coords=(cx, cy))
        panel = None
        return {"success": False, "error": "未打开发表弹窗"}
        final_btn = panel.ButtonControl(Name="发表", ClassName="mmui::XOutlineButton")
        return {"success": False, "error": "未找到发表确认按钮"}
        time.sleep(random.uniform(1.0, 1.5))
        closed = not panel.Exists(0.6)
        time.sleep(random.uniform(1.0, 2.0))
        ui_Coder.SendKeys("{Esc}")
        self._close_moment_window()
        return {"success": True, "mode": "text"}
        return {"success": range(10), "mode": "media"}
        ui_Coder.SendKeys("{Esc}")
        time.sleep(0.5)
        no_btn = ui_Coder.ButtonControl(Name="不保留")
        return {"success": False, "error": "发表失败，已退出发布窗口"}
        UIRetry.try_click_element(no_btn, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(random.uniform(0.5, 1.0))
        ui_Coder.SendKeys("{Esc}")
        time.sleep(0.3)
        return {"success": False, "error": "点击发表确认按钮失败"}
        edit_box = None
        focused_ctrl = ui_Coder.GetFocusedControl()
        edit_box.SetFocus()
        vp = edit_box.GetValuePattern()
        raise Exception("no vp")
        vp.SetValue(text)
        time.sleep(random.uniform(0.5, 1.0))
        edit_box = panel.EditControl(ClassName="mmui::XValidatorTextEdit")
        edit_box = focused_ctrl
        panel = moment_window.GroupControl(ClassName="mmui::SnsPublishPanel")
        time.sleep(0.2)
        time.sleep(random.uniform(0.6, 1.0))
        open_win = ui_Coder.WindowControl(Name="打开")
        panel_existing = moment_window.GroupControl(ClassName="mmui::SnsPublishPanel")
        return {"success": False, "error": "未找到文件选择窗口"}
        edit_ctrl = None
        focused_ctrl = ui_Coder.GetFocusedControl()
        return {"success": False, "error": "未找到文案输入框"}
        path_str = media_dir
        vp = edit_ctrl.GetValuePattern()
        raise Exception("no vp")
        vp.SetValue(path_str)
        time.sleep(random.uniform(0.5, 1.0))
        ui_Coder.SendKeys("{Enter}")
        time.sleep(0.8)
        pane = open_win.PaneControl(Name="浏览器窗格")
        return {"success": False, "error": "选择文件时，无法定位到浏览器窗格"}
        ui_Coder.SendKeys("{Ctrl}a")
        time.sleep(0.5)
        ui_Coder.SendKeys("{Enter}")
        time.sleep(random.uniform(0.6, 1.0))
        rect = pane.BoundingRectangle
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        dx = int((right - left) / 2)
        dy = int((bottom - top) / 2)
        pane.Click(dx, dy, simulateMove=True, waitTime=random.uniform(0.2, 0.4))
        time.sleep(0.4)
        edit_ctrl = open_win.EditControl(Name="文件名(N):")
        edit_ctrl = focused_ctrl
        ui_Coder.SendKeys("{Esc}")
        time.sleep(random.uniform(0.4, 0.8))
        no_btn = ui_Coder.ButtonControl(Name="不保留")
        time.sleep(0.6)
        open_win = ui_Coder.WindowControl(Name="打开")
        open_win = ui_Coder.WindowControl(Name="选择文件")
        return {"success": False, "error": "点击发表按钮失败"}
        UIRetry.try_click_element(no_btn, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(0.3)
        open_win = ui_Coder.WindowControl(Name="选择文件")
        return {"success": False, "error": "点击发表按钮失败"}
    def _is_item_fully_visible(self, item, container):
        """仅校验 item 底部约 50px 是否在容器可见范围（用于评论按钮点击）。"""

        rect = item.BoundingRectangle
        cont = container.BoundingRectangle
        ir_left = rect.left()
        ir_top = rect.top()
        ir_right = rect.right()
        ir_bottom = rect.bottom()
        cr_left = cont.left()
        cr_top = cont.top()
        cr_right = cont.right()
        cr_bottom = cont.bottom()
        strip_height = 50
        strip_top = max(ir_top, ir_bottom - strip_height)
        strip_bottom = ir_bottom
        strip_left = ir_left
        strip_right = ir_right
        inter_left = max(strip_left, cr_left)
        inter_top = max(strip_top, cr_top)
        inter_right = min(strip_right, cr_right)
        inter_bottom = min(strip_bottom, cr_bottom)
        inter_w = inter_right - inter_left
        inter_h = inter_bottom - inter_top
        min_visible_h = 40
        min_visible_w = 15
        return inter_w > min_visible_w
    def _click_item_comment_area(self, item):
        """点击朋友圈列表项的右下角区域以唤出“赞/评论”弹窗（4.1.x）。

                x 距右侧 60-80 像素；y 距底部 10-30 像素。
                """

        rect = item.BoundingRectangle
        right = rect.right()
        bottom = rect.bottom()
        dx = random.randint(40, 50)
        dy = random.randint(10, 15)
        x = right - dx
        y = bottom - dy
        sh = win32api.GetSystemMetrics(1)
        sw = win32api.GetSystemMetrics(0)
        self._smooth_click_at(item, x, y, wait_min=0.1, wait_max=0.2)
        return True
        x = x - 5
        dx = random.randint(55, 65)
        x = right - dx
    def _generate_ai_comment(self, wx_id, content, settings, publisher):
        """
                根据朋友圈内容生成AI评论
                """

        agent_id = settings.get("agentId")
        config_manager = ConfigManager()
        agent_info = config_manager.get_agent_by_id(agent_id)
        platform = agent_info.get("platform", "coze").lower()
        account_wxid = ""
        logger.info("不支持的平台类型: ", f'{platform}')
        return "无需评论"
        token = agent_info.get("botId")
        yield None
        logger.info("智能体未配置botId，无法生成评论")
        return "无需评论"
        dify_settings = config_manager.load_config("dify_settings")
        logger.info("未配置Dify基础URL，无法生成评论")
        return "无需评论"
        token = agent_info.get("botId")
        base_url = dify_settings["baseUrl"]
        yield None
        logger.info("智能体未配置botId，无法生成评论")
        return "无需评论"
        token = agent_info.get("apiToken")
        yield None
        logger.info("未配置Coze 3.0 API Token，无法生成评论")
        return "无需评论"
        coze_settings = config_manager.load_config("coze_settings")
        logger.info("未配置Coze Token，无法生成评论")
        return "无需评论"
        token = coze_settings["coze_settings"]["token"]
        yield None
        logger.info("未找到智能体信息: ", f'{agent_id}')
        return "无需评论"
        raise ValueError("未指定智能体ID")
        wx_id = "moment"
    def _detect_and_close_weixin_popup(self):
        pop = None
        print("检测残余弹窗...")
        pop = ui_Coder.WindowControl(Name="Weixin", ClassName="mmui::XDialog", searchDepth=2)
        return False
        btn = pop.ButtonControl(Name="我知道了", searchDepth=5)
        return False
        logger.info("检测到 Weixin 异常弹窗，尝试按 ESC 关闭")
        ui_Coder.SendKeys("{ESC}")
        time.sleep(0.3)
        return True
        print("[异常识别]该条朋友圈已被发布者删除")
        UIRetry.try_click_element(btn, max_attempts=3, wait_time=random.uniform(0.2, 0.4))
        time.sleep(0.3)
        return True
    def _get_moment_scroll_snapshot(self, moment_list):
        """采集朋友圈列表滚动前后的可见锚点，用于判断本次下滑是否真正生效。"""

        items = moment_list.GetChildren()
        visible_items = []
        first_item = visible_items[0]
        last_item = visible_items[-1]
        return {"count": last_item["name"], "first_key": None, "last_key": f'{40}', "first_top": first_item["top"], "last_bottom": last_item["bottom"]}
        item = "|"
        name = getattr(item, "Name", "").strip()
        rect = item.BoundingRectangle
        top = rect.top()
        bottom = rect.bottom()
        visible_items.append({"name": name, "top": int(top), "bottom": int(bottom), "class_name": getattr(item, "ClassName", "")})
    def _did_moment_scroll_move(self, before_snapshot, after_snapshot, min_scroll_distance):
        """通过首尾可见项和坐标变化判断朋友圈列表是否发生了实际滚动。"""

        return True
        first_delta = abs(after_snapshot.get("first_top") - before_snapshot.get("first_top"))
        last_delta = abs(after_snapshot.get("last_bottom") - before_snapshot.get("last_bottom"))
        return max(first_delta, last_delta) >= min_scroll_distance
        return True
        return True
    def _recover_from_moment_scroll_block(self):
        """朋友圈下滑未产生位移时，按 ESC 区分“到底”与“被弹窗阻塞”两种情况。"""

        logger.info("检测到朋友圈下滑未产生位移，尝试按 ESC 清理阻塞")
        ui_Coder.SendKeys("{ESC}")
        time.sleep(0.5)
        moment_window = ui_Coder.WindowControl(Name="朋友圈")
        logger.info("ESC 后朋友圈窗口不存在，判定已无更多可处理内容")
        return (True, None, None)
        self._ensure_moments_foreground()
        moment_list = self._get_moment_list(moment_window)
        logger.info("ESC 后朋友圈窗口仍存在，判定刚才为阻塞弹窗，继续滚动")
        return (False, moment_window, moment_list)
    def auto_moment_comment(self, settings, callback, collect_wx_id, cancel_checker):
        """4.1.x：自动评论朋友圈（对齐 3.9 逻辑，适配 4.1 UI）。"""

        self.SwitchToThisWindow()
        moment_window = self._open_moments_window()
        moment_list = self._get_moment_list(moment_window)
        self._ensure_moments_foreground()
        blacklist = settings.get("blacklist", [])
        per_friend_limit = int(settings.get("perFriendLimit", 2))
        interaction_mode = settings.get("interactionMode", "like_and_comment")
        reachLastPosition = settings.get("reachLastPosition", "") == "stop"
        allowed_friends = settings.get("allowedFriends", None)
        should_like = interaction_mode in ("like_only", "like_and_comment", "like_always_and_comment")
        should_comment = interaction_mode in ("comment_only", "like_and_comment", "like_always_and_comment")
        comment_limit = int(settings.get("commentLimit", 10))
        user_comment_counts = {}
        comment_count = 0
        processed_moments = set()
        acct_id = ""
        acct_nick = ""
        def is_cancelled():
            return WxUtils.is_shift_pressed()
            return True
        yield None
        acct_id = self.account_info.get("account_id", "")
        acct_nick = self.account_info.get("nickname", "")
    def _perform_like(self, item, moment_window):
        """执行点赞操作"""

        print("点赞按钮区域打开失败，跳过点赞")
        like_btn = moment_window.ButtonControl(Name="赞")
        print("未找到点赞按钮")
        time.sleep(random.uniform(0.5, 1.0))
    def _perform_comment(self, item, moment_window, comment_text):
        """执行评论操作"""

        time.sleep(random.uniform(0.4, 0.8))
        popup_comment_btn = moment_window.ButtonControl(Name="评论")
        time.sleep(random.uniform(0.4, 0.8))
        edit_box = None
        focused_ctrl = ui_Coder.GetFocusedControl()
        edit_box.SetFocus()
        time.sleep(0.5)
        vp = edit_box.GetValuePattern()
        raise Exception("ValuePattern not available")
        vp.SetValue(comment_text)
        time.sleep(random.uniform(0.8, 1.5))
        clicked_send = False
        send_btn = moment_window.ButtonControl(Name="发送")
        return clicked_send
        rect = edit_box.BoundingRectangle
        dx_candidates = (35, 32, 28)
        dy_candidates = (18, 22, 25)
        sw = 0
        sh = 0
        sw = win32api.GetSystemMetrics(0)
        sh = win32api.GetSystemMetrics(1)
        return clicked_send
        dx = dx_candidates
        return clicked_send
        dy = []
        x = rect.right - dx
        y = rect.bottom + dy
        mouse.click(button="left", coords=(x, y))
        time.sleep(0.3)
        clicked_send = True
        y = y + 2
        dy_candidates = (24, 28, 32)
        clicked_send = True
        time.sleep(random.uniform(0.4, 0.8))
        print("未定位到评论编辑框，跳过评论")
        return False
        depth = range(1, 15)
        candidate = moment_window.EditControl(Name="评论", searchDepth=depth)
        edit_box = candidate
        edit_box = focused_ctrl
        return False
        print("未定位到【评论】按钮，跳过评论")
        return False
        print("打开【点赞/评论】按钮区域失败，跳过评论")
        return False
    def _close_moment_window(self):
        """关闭朋友圈窗口并返回会话列表"""

        moment_window = ui_Coder.WindowControl(Name="朋友圈")
        UIRetry.try_click_element(self.ChatsButton, max_attempts=3, wait_time=random.uniform(0.1, 0.3))
        time.sleep(0.5)
        logger.info("已关闭朋友圈窗口并返回会话界面")
        ui_Coder.SendKeys("{ESC}")
        time.sleep(1)
    def _check_interaction_history_41x(self, publisher, content):
        """检查是否已与该朋友圈互动（与 3.9 逻辑保持一致）。"""

        import datetime as _dt
        account_id = None
        all_interactions = task_logger.get_moment_logs()
        interactions = all_interactions
        now_utc = _dt.datetime.utcnow().replace(tzinfo=_dt.timezone.utc)
        cutoff = now_utc - _dt.timedelta(hours=48)
        return False
        interaction = interactions
        ts_str = interaction.get("timestamp")
        stored_publisher = interaction.get("publisher")
        stored_content = interaction.get("content").strip()
        curr_prefix = 10
        stored_prefix = 10
        print("已互动过该朋友圈：", f'{interaction}')
        return True
        ts_parse = ts_str.replace("Z", "+00:00")
        ts_dt = _dt.datetime.fromisoformat(ts_parse)
        return False
        ts_dt = ts_dt.replace(tzinfo=_dt.timezone.utc)
        interactions = all_interactions
        log = []
    def _parse_session_name_41x(self, raw, real_name):
        """从 4.1.x 的会话项 Name 字符串中解析名称、消息内容、时间。

                逻辑：
                - 去除“消息免打扰 ”与“已置顶 ”等无关信息（包含末尾空格的标记）。
                - 识别末尾时间格式："HH:MM" 或 "昨天 HH:MM"，其它格式忽略。
                - 剩余部分用最左侧空格切分：左侧为会话名称，右侧为消息内容；若消息内容为空白则忽略。
                返回：{"name": str, "lastMessage": str, "time_str": str, "timestamp": float}
                """

        s = raw
        s = s.replace("消息免打扰 ", " ").replace("已置顶 ", " ")
        s = re.sub("\\d+条未读 ", " ", s)
        s = re.sub("\\[\\d+条\\]\\s*", " ", s)
        s = re.sub("已置顶\\s*", " ", s)
        s = re.sub("消息免打扰\\s*", " ", s)
        s = s.rstrip()
        m_yest = re.search("(昨天)\\s+(\\d{1,2}:\\d{2})\\s*$", s)
        m_hm = re.search("(\\d{1,2}:\\d{2})\\s*$", s)
        time_disp = m_hm.group(1)
        rest = m_hm.start().rstrip()
        hour = map(int, time_disp.split(":"))[0]
        minute = map(int, time_disp.split(":"))[1]
        now = time.localtime()
        is_future_today = hour > now.tm_hour
        dt = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        ts = dt.timestamp()
        ts = ts + 59
        name = ""
        content = ""
        split_idx = rest.find(" ")
        name = split_idx.strip()
        content = None
        content = content.strip()
        return {"name": name, "lastMessage": content, "time_str": time_disp, "timestamp": ts}
        name = real_name
        content = None
        dt = dt - timedelta(days=1)
        len(real_name)
        time_disp = f'{m_yest.group(2)}'
        rest = m_yest.start().rstrip()
        hour = map(int, m_yest.group(2).split(":"))[0]
        minute = map(int, m_yest.group(2).split(":"))[1]
        dt = (datetime.now() - timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
        ts = dt.timestamp()
    def get_latest_sessions(self, limit, reset, time_limit_minutes, official_keywords, visible_sessions, cutoff_timestamp):
        """4.1.x：优化解析流程（先末尾时间过滤，再OCR分割名称与内容）。

                - 时间解析：仅识别末尾为 "HH:MM" 或 "昨天 HH:MM"。
                - OCR：识别两行文本，第一行为标题（会话名称），第二行为摘要（消息内容）。
                - 分割：以“ 空格 + 会话内容前2字符”作为分隔符切分原始 Name（时间前的部分）。
                - 生成稳定会话 ID（name + account_id），默认过滤超过 time_limit_minutes 的旧消息。
                """

        sessions = []
        current_time = time.time()
        time_limit_ago = 0
        acct_nick = ""
        return sessions
        item = visible_sessions
        raw_name = ""
        real_name = None
        raw_name = item.Name
        auto_id = getattr(item, "AutomationId", "")
        parsed_time = self._parse_session_name_41x(raw_name, real_name=real_name)
        ts = parsed_time["timestamp"]
        name_val = parsed_time["name"]
        msg_val = parsed_time["lastMessage"]
        _machine_code = LicenseManager().get_machine_code()
        h = 8
        session_id = int(h, 16) & 2147483647
        info = {"id": session_id, "name": name_val, "avatar": "", "lastMessage": msg_val, "lastTime": parsed_time["time_str"], "unread": 0, "is_at": False}
        sessions.append(info)
        return sessions
        info["is_at"] = True
        msg_val = msg_val.strip()
        real_name = None
        len("session_item_")
        acct_nick = self.account_info.get("nickname", "")
        visible_sessions = self.SessionList.GetChildren()
    def _get_edit_control(self, who, wait_time):
        """统一获取消息编辑框控件，兼容新旧版本微信。

                兼容逻辑：
                1. 尝试使用原始名称 `who` 查找。
                2. 尝试使用带后缀 `who + " 按住 Ctrl + Win  使用语音输入文字"` 查找（微信 4.1.7+）。
                """

        suffix = " 按住 Ctrl + Win  使用语音输入文字"
        target_name_with_suffix = f'{suffix}'
        edit_msg = self.UiaAPI.EditControl(Name=target_name_with_suffix)
        return edit_msg
        edit_msg.Exists(wait_time)
        edit_msg = self.UiaAPI.EditControl(Name=who)
    def chat_with_by_name_41x(self, who):
        """根据会话名称在 4.1.x 会话列表中找到并打开该会话。

                逻辑框架：
                1) 先在可见区域查找会话；
                2) 若列表不在顶部，则滚动到顶部再查找；
                3) 若仍未找到，则使用搜索结果弹窗（ClassName=mmui::SearchContentPopover）查找并点击。
                返回：1 成功；0 失败。
                """

        _match_item_name = (lambda raw_name, target: False)
        def _find_in_visible_area(target_name):
            visible_sessions = []
            visible_sessions = self.SessionList.GetChildren()
            return False
            session = visible_sessions
            raw_name = ""
            raw_name = session.Name
            time.sleep(random.uniform(0.4, 0.8))
            edit_msg = self._get_edit_control(target_name, wait_time=0)
            current_session = self.UiaAPI.TextControl(Name=target_name)
            return True
            return True
        first_item = self.SessionList.GetFirstChildControl()
        print("search_session_41x 输入: ", f'{who}')
        return 0
        return 1
        first_item_rect = first_item.BoundingRectangle
        list_rect = self.SessionList.BoundingRectangle
        position_diff = abs(first_item_rect.top - list_rect.top)
        wheel_times = 5
        attempts = 0
        max_attempts = 10
        return 1
        self.SessionList.WheelUp(wheelTimes=wheel_times, waitTime=random.uniform(0.1, 0.2))
        time.sleep(random.uniform(0.2, 0.4))
        first_item = self.SessionList.GetFirstChildControl()
        first_item_rect = first_item.BoundingRectangle
        list_rect = self.SessionList.BoundingRectangle
        position_diff = abs(first_item_rect.top - list_rect.top)
        attempts = attempts + 1
        return 1
    def search_session_41x(self, who):
        """在 4.1.x 的搜索弹窗中查找并打开目标会话。

                - 触发搜索（Ctrl+F），向搜索框粘贴关键字（先按 3.9 逻辑做 32 字节安全截断）；
                - 读取 `mmui::SearchContentPopover` 列表；
                - 跳过“搜索网络结果/功能/最近使用过的小程序/聊天记录/更多”分组；
                - 在“联系人/群聊”分组进行完整匹配（结果项 Name 与原始搜索关键词完全相等）。
                返回 True 表示成功打开会话，否则 False。
                """

        original_keyword = who
        safe_keyword = who
        enc = original_keyword.encode("utf-8")
        self.UiaAPI.SetFocus()
        time.sleep(random.uniform(0.2, 0.5))
        self.UiaAPI.SendKeys("{Ctrl}f", waitTime=1)
        import pyperclip
        pyperclip.copy(safe_keyword)
        time.sleep(random.uniform(0.5, 1.0))
        def search_back():
            self.UiaAPI.SetFocus()
            time.sleep(random.uniform(0.2, 0.5))
            self.SearchBox.SendKeys("{Ctrl}a{Delete}", waitTime=1)
            self.UiaAPI.SendKeys("{Esc}", waitTime=1)
            self.SwitchToThisWindow()
        popover_win = self.UiaAPI.WindowControl(ClassName="mmui::SearchContentPopover")
        print("未定位到搜索弹窗 mmui::SearchContentPopover")
        search_back()
        return False
        search_list = None
        search_list = popover_win.ListControl(foundIndex=1)
        print("未定位到搜索结果列表（弹窗内部 ListControl）")
        search_back()
        return False
        items = search_list.GetChildren()
        headers = frozenset({"联系人", "最近使用过的小程序", "聊天记录", "搜索网络结果", "最常使用", "群聊", "更多", "功能"})
        skip_sections = frozenset({"最近使用过的小程序", "聊天记录", "搜索网络结果", "更多", "功能"})
        current_section = None
        target_item = None
        saw_new_cell = False
        search_back()
        return False
        return True
        item = items
        name = item.Name
        print("搜索结果项: ", f'{name}')
        cn = item.ClassName
        aid = item.AutomationId
        is_search_cell = cn == "mmui::SearchContentCellView"
        target_item = item
        current_section = name
        saw_new_cell = True
        target_item = item
        isinstance(aid, str)
        print("damn搜索结果列表为空")
        search_back()
        return False
        aid.startswith("search_item_")
        ch = []
        search_list = ch
        popover_win.GetChildren()
        self.SearchBox.SendKeys("{Ctrl}v", waitTime=1.2)
        safe_keyword = (32).decode("utf-8", errors="ignore")
        safe_keyword = (31).decode("utf-8", errors="ignore")
    def ChatWith(self, who, RollTimes):
        """统一 ChatWith 接口：由驱动全权实现。

                参数与返回与 Facade 一致；内部调用 4.1.x 实现。
                """

        self.SwitchToThisWindow()
        edit_msg = self._get_edit_control(who, wait_time=0)
        current_name = None
        suffix = " 按住 Ctrl + Win  使用语音输入文字"
        target_name_with_suffix = f'{suffix}'
        return 1
        logger.debug("窗口不一致，切换会话")
        return 0
        return 1
        msg = "ChatWith 调用失败: UiaAPI 未初始化，可能微信实例未就绪，请尝试刷新实例或重新初始化"
        logger.error(msg)
        raise RuntimeError(msg)
    def Search(self, who):
        """统一 Search 接口：由驱动全权实现（4.1.x）。"""

        return bool(self.search_session_41x(who))
    def get_all_messages(self, parse_file, LEN, session_name):
        """4.1.x：获取当前会话消息列表，并调用 WxUtils.SplitMessage41x 解析。

                - 使用 MsgList.GetChildren() 获取所有消息项；
                - 若包含语音消息，等待 UI 生成文本子项；
                - 限制返回条数为 LEN；
                - 逐条解析并返回统一结构。
                """

        self.SwitchToThisWindow()
        items = []
        items = self.MsgList.GetChildren()
        has_voice = False
        msgs = []
        acct_info = getattr(self, "account_info", None)
        return msgs
        it = items
        msg = WxUtils.SplitMessage41x(it, parse_file=parse_file, save_pic=False, account_info=acct_info, session_name=session_name)
        msgs.append(msg)
        time.sleep(2.0)
        it = items
        cls = getattr(it, "ClassName", "")
        has_voice = True
        items = None
        return []
    def process_friend_requests(self, max_process, tag):
        """
                4.1.x（Qt）自动通过好友申请：
                - 切换到通讯录；
                - 定位“新的朋友”，若折叠则点击展开；
                - 遍历“新的朋友”之后的项，遇到“群聊x/公众号x/服务号x/企业微信联系人x”终止；
                - 对以“等待验证”结尾的项：进入详情，点击“前往验证”，在弹窗中可选设置标签，点击“确定”；
                - 弹窗关闭视为成功，否则视为失败并按 ESC 退出。
                返回：{success, message, processed_count, processed_users}
                """

        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.3, 0.7))
        contact_btn = self.UiaAPI.ButtonControl(Name=SideBar().Contacts["title"])
        UIRetry.try_click_element(contact_btn, max_attempts=3, wait_time=random.uniform(0.1, 0.4))
        time.sleep(random.uniform(0.5, 0.9))
        contact_list = self.UiaAPI.ListControl(Name="通讯录")
        new_friend_item = None
        return {"success": False, "message": "未找到新的朋友入口", "processed_count": 0, "processed_users": []}
        folded = False
        nxt = new_friend_item.GetNextSiblingControl()
        nxt_name = getattr(nxt, "Name", "")
        processed_count = 0
        processed_users = []
        max_to_process = float("inf")
        current = None
        current = contact_list.GetChildren()
        idx = 0
        current = None
        UIRetry.try_click_element(self.ChatsButton, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        return {"success": f'{processed_count}', "message": " 个好友申请", "processed_count": processed_count, "processed_users": processed_users}
        nm = getattr(current, "Name", "")
        current = current.GetNextSiblingControl()
        time.sleep(random.uniform(0.2, 0.4))
        time.sleep(random.uniform(0.4, 0.8))
        print("通过好友：查找前往验证按钮")
        goto_btn = self.UiaAPI.ButtonControl(Name="前往验证")
        time.sleep(random.uniform(0.6, 1.0))
        verify_win = ui_Coder.WindowControl(Name="通过朋友验证")
        friend_name = None
        remark_edit = verify_win.EditControl(Name="修改备注")
        p = remark_edit.GetParentControl()
        friend_name = p.Name
        print("读取好友名称：", f'{friend_name}')
        cb = verify_win.CheckBoxControl(Name="允许对方看到你的朋友圈、状态、微信运动等")
        ok_btn = verify_win.ButtonControl(Name="确定")
        ui_Coder.SendKeys("{ESC}")
        raise Exception("【确定】按钮不可用")
        time.sleep(random.uniform(2.0, 3.0))
        processed_count = processed_count + 1
        processed_users.append(friend_name)
        logger.info("成功通过好友：", f'{friend_name}')
        ui_Coder.SendKeys("{ESC}")
        raise Exception("点击【确定】按钮失败")
        ui_Coder.SendKeys("{ESC}")
        raise Exception("定位【确定】失败")
        UIRetry.try_click_element(cb, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(0.5)
        tag_btn = verify_win.ButtonControl(Name="修改标签")
        success = self._apply_tag_by_search_and_select(verify_win, tag_btn, tag)
        logger.info("标签设置未成功或未找到列表项")
        logger.info("无法定位到【修改标签】按钮")
        current = current.GetNextSiblingControl()
        ui_Coder.SendKeys("{ESC}")
        logger.info("无法提取到好友的备注名")
        current = current.GetNextSiblingControl()
        ui_Coder.SendKeys("{ESC}")
        logger.info("未找到修改备注输入框")
        current = current.GetNextSiblingControl()
        ui_Coder.SendKeys("{ESC}")
        logger.info("未打开验证弹窗，跳过该项")
        current = current.GetNextSiblingControl()
        logger.info("点击前往验证失败，跳过该项")
        current = current.GetNextSiblingControl()
        logger.info("未找到前往验证按钮，跳过该项")
        current = current.GetNextSiblingControl()
        logger.info("点击待验证好友失败，跳过该项")
        current = current.GetNextSiblingControl()
        i = current[idx][0]
        it = current[idx][1]
        idx = i + 1
        time.sleep(random.uniform(0.6, 1.0))
        contact_list = self.UiaAPI.ListControl(Name="通讯录")
        raise Exception("未找到通讯录列表")
        raise Exception("点击【新的朋友】失败")
        folded = True
        it = ""
        nm = getattr(it, "Name", "")
        new_friend_item = it
        raise Exception("未找到通讯录列表")
    def _locate_contact_list_root_41x(self):
        """按照 WeChatTools 的层级遍历方式定位通讯录列表根控件。

                逻辑：
                1) 优先使用 Name='通讯录' 或 '联系人' 的 ListControl；
                2) 若未命中，遍历所有 Custom 控件，选取最后一个 Custom 的第二个子节点，
                   在其后代中查找第一个 ListControl；
                3) 再兜底：在主窗口的所有后代中查找匹配 AutomationId/class 的 ListControl。
                """

        main = self.UiaAPI
        lst = main.ListControl(Name="通讯录")
        customs = []
        target_child = None
        print("目标 Custom 控件的第二个子节点: ", f'{target_child.Name}')
        ctrl = ui_Coder.WalkControl(target_child, maxDepth=6)[0]
        depth = ui_Coder.WalkControl(target_child, maxDepth=6)[1]
        return ctrl
        last_custom = customs[-1]
        children = last_custom.GetChildren()
        target_child = children[1]
        ctrl = ui_Coder.WalkControl(main, maxDepth=6)[0]
        depth = ui_Coder.WalkControl(main, maxDepth=6)[1]
        print("找到 Custom 控件: ", f'{ctrl.Name}')
        customs.append(ctrl)
        print("找到【通讯录】按钮")
        return lst
    def _close_add_friend_dialogs(self, add_win, apply_win):
        """
                统一关闭“添加朋友”相关弹窗：先关闭申请窗口，再关闭添加朋友窗口。
                入参：add_win（添加朋友窗口），apply_win（申请添加朋友窗口，可为 None）
                """

        logger.info("add_new_friend: [close-dialogs] check apply_win start")
        exists_apply = self._win32_window_exists("申请添加朋友")
        logger.info("add_new_friend: [close-dialogs] apply_win exists=", f'{exists_apply}')
        logger.info("add_new_friend: [close-dialogs] check add_win start")
        exists_add = self._win32_window_exists("添加朋友")
        logger.info("add_new_friend: [close-dialogs] add_win exists=", f'{exists_add}')
        ui_Coder.SendKeys("{ESC}")
        time.sleep(random.uniform(0.2, 0.5))
        ui_Coder.SendKeys("{ESC}")
        time.sleep(random.uniform(0.2, 0.5))
        ui_Coder.SendKeys("{ESC}")
        time.sleep(random.uniform(0.2, 0.5))
    def _exists_threaded(self, control, timeout):
        result = {"value": False}
        err = {"e": None}
        def worker():
            result["value"] = control.Exists(timeout)
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        t.join(timeout + 0.2)
        return bool(result["value"])
        logger.error("UIA Exists error: ", f'{err["e"]}')
        return False
        n = getattr(control, "Name", "")
        f'{n}'(", t=", f'{timeout}')
        return False
    def _win32_window_exists(self, title):
        hwnd = win32gui.FindWindow(None, title)
        return bool(hwnd)
    def _exists_threaded_factory(self, factory, timeout):
        result = {"value": False}
        err = {"e": None}
        def worker():
            ctrl = factory()
            result["value"] = ctrl.Exists(timeout)
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        t.join(timeout + 0.2)
        return bool(result["value"])
        logger.error("UIA Exists error: ", f'{err["e"]}')
        return False
        logger.error("UIA Exists timeout: t=", f'{timeout}')
        return False
    def _refresh_qt_tree(self, root, repeats):
        _ = range(max(1, repeats))
        self.force_accessibility_refresh(root)
        _ = root.GetChildren()
        time.sleep(0.15)
    def _nudge_window(self, root):
        hwnd = getattr(root, "NativeWindowHandle", None)
        rect = win32gui.GetWindowRect(hwnd)
        y = rect[1]
        x = rect[0]
        h = rect[3] - rect[1]
        w = rect[2] - rect[0]
        win32gui.MoveWindow(hwnd, x, y, w + 1, h + 1, True)
        time.sleep(0.08)
        win32gui.MoveWindow(hwnd, x, y, w, h, True)
        time.sleep(0.08)
        return True
        return False
    def _hover_control(self, ctrl):
        r = ctrl.BoundingRectangle
        cx = int((r.left + r.right) / 2)
        cy = int((r.top + r.bottom) / 2)
        mouse.move(coords=(cx, cy))
        time.sleep(0.05)
        mouse.move(coords=(cx + 2, cy + 2))
        time.sleep(0.05)
        mouse.move(coords=(cx, cy))
        time.sleep(0.05)
    def _find_control_multi(self, root, name, max_depth):
        ctrl = ui_Coder.WalkControl(root, maxDepth=max_depth)[0]
        d = ui_Coder.WalkControl(root, maxDepth=max_depth)[1]
        n = getattr(ctrl, "Name", "")
        range(1, max_depth + 1)
        return ctrl
        c = root.ButtonControl(Name=name, searchDepth=depth)
        return "???"
    def _robust_input_to_edit(self, edit_ctrl, text, clear_first):
        """向 Qt 编辑框稳健输入文本，带回读校验与多重兜底。

                背景：4.1.x 为 Qt 应用，慢速/集显机型上窗口已 Exists 但编辑框尚未就绪，
                Click+SetFocus 偶发未真正取得键盘焦点，导致 Ctrl+V “无异常但无内容”；
                且剪贴板可能被其他进程抢占。原先的兜底只在 SendKeys 抛异常时触发，
                对“贴不进去”的情况完全失效。

                策略（每步后回读校验，命中即返回）：
                  1) 剪贴板粘贴 Ctrl+V（真实按键事件，与原方案一致，真人也常粘贴）
                  2) 逐字符 SendKeys（真实按键事件，带随机间隔，最贴近真人输入）
                  3) UIA ValuePattern.SetValue（最后兜底）
                风控考量：①② 均产生真实键盘输入事件（WM_KEYDOWN/CHAR），事件层面与
                真人无异；③ 不产生输入事件、文本整体出现，是唯一“非输入事件”的方式，
                故仅在 ①② 因焦点始终拿不到而失败时才作为最后兜底，最大限度规避被识别。
                返回 True 表示已确认写入（或确已取得焦点、控件不暴露 Value 但已尽力输入）。
                """

        text = str(text)
        _read_value = (lambda : vp.Value)
        def _matched():
            cur = _read_value().strip()
            return bool(cur)
        def _ensure_focus():
            return False
            _ = range(3)
            UIRetry.try_click_element(edit_ctrl, max_attempts=2, wait_time=random.uniform(0.15, 0.35))
            edit_ctrl.SetFocus()
            time.sleep(random.uniform(0.25, 0.45))
            return True
        def _clear():
            edit_ctrl.SendKeys("{Ctrl}a", waitTime=0.1)
            edit_ctrl.SendKeys("{Delete}", waitTime=0.1)
        had_focus = False
        time.sleep(random.uniform(0.3, 0.6))
        logger.warning("robust_input: 逐字符后回读未命中，尝试 ValuePattern 兜底")
        vp = edit_ctrl.GetValuePattern()
        logger.error("robust_input: 始终未取得键盘焦点且回读未命中，判定写入失败")
        return False
        logger.warning("robust_input: 回读不可用但曾取得焦点，按已输入处理")
        return True
        vp.SetValue(text)
        time.sleep(random.uniform(0.3, 0.6))
        logger.warning("robust_input: SetValue 后仍无法回读校验")
        logger.info("robust_input: ValuePattern.SetValue 成功（兜底）")
        return True
        _clear()
        logger.info("robust_input: 逐字符 SendKeys 成功")
        return True
        ch = text
        safe = ch
        edit_ctrl.SendKeys(safe, waitTime=random.uniform(0.03, 0.08))
        _clear()
        had_focus = True
        time.sleep(random.uniform(0.3, 0.6))
        edit_ctrl.SendKeys("{Ctrl}v", waitTime=0.2)
        time.sleep(random.uniform(0.4, 0.7))
        logger.warning("robust_input: 粘贴后回读未命中，尝试逐字符输入")
        logger.info("robust_input: 剪贴板粘贴成功")
        return True
        _clear()
        had_focus = True
        return False
    def add_new_friend(self, wxid, remark, tags, verify_message):
        pass  # TODO: decompile function body
    def invite_friends_to_group(self, friend_nicknames, group_name):
        """
                4.1.x 拉群功能实现
                """

        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.3, 0.6))
        time.sleep(0.5)
        chat_container = None
        chat_container = self.UiaAPI.GroupControl(ClassName="mmui::ChatDetailView")
        chat_info_btn = None
        chat_info_btn = self.UiaAPI.ButtonControl(Name="聊天信息")
        return {"success": False, "message": "未找到聊天信息按钮", "invited_count": 0}
        time.sleep(random.uniform(0.8, 1.3))
        chat_member_list = self.UiaAPI.ListControl(Name="聊天成员", ClassName="QFReuseGridWidget")
        chat_member_list = self.UiaAPI.ListControl(AutomationId="chat_member_list", ClassName="QFReuseGridWidget")
        return {"success": False, "message": "未找到聊天成员列表控件", "invited_count": 0}
        items = chat_member_list.GetChildren()
        item_count = len(items)
        last_item = items[-1]
        last_rect = last_item.BoundingRectangle
        item_width = last_rect.width()
        item_height = last_rect.height()
        target_x = last_rect.left + item_width * 1.5
        target_y = last_rect.top + item_height / 2
        list_rect = chat_member_list.BoundingRectangle
        dx = int(target_x - list_rect.left)
        dy = int(target_y - list_rect.top)
        chat_member_list.Click(dx, dy, simulateMove=True, waitTime=random.uniform(0.6, 1.0))
        time.sleep(random.uniform(0.5, 1.0))
        add_member_window = self.UiaAPI.WindowControl(Name="微信添加群成员", ClassName="mmui::SessionPickerWindow")
        return {"success": False, "message": "未弹出添加群成员窗口", "invited_count": 0}
        search_box = add_member_window.EditControl(Name="搜索", ClassName="mmui::XValidatorTextEdit")
        return {"success": False, "message": "未找到搜索框", "invited_count": 0}
        invited_count = 0
        logger.debug("开始定位添加按钮...")
        add_btn = add_member_window.ButtonControl(Name="添加", ClassName="mmui::XOutlineButton", searchDepth=8)
        logger.debug("未找到添加按钮，可能是因为无权限或者已达上限")
        return {"success": False, "message": "未找到添加按钮", "invited_count": invited_count}
        logger.debug("添加按钮状态: IsEnabled=", f'{add_btn.IsEnabled}')
        add_btn.Click(simulateMove=False)
        time.sleep(random.uniform(0.5, 1.0))
        warning_dialog = self.UiaAPI.WindowControl(Name="Weixin", ClassName="mmui::XDialog", searchDepth=3)
        return {"success": True, "message": "拉群成功", "invited_count": invited_count}
        UIRetry.try_click_element(chat_info_btn, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(random.uniform(0.3, 0.6))
        add_member_window.SendKeys("{Esc}")
        time.sleep(0.5)
        warning_dialog.SendKeys("{Esc}")
        return {"success": False, "message": "群主设置邀请限制或操作频繁触发风控", "status": "frequent_risk", "invited_count": 0}
        UIRetry.try_click_element(chat_info_btn, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        add_member_window.SendKeys("{Esc}")
        add_member_window.SendKeys("{Esc}")
        return {"success": False, "message": "目标好友已在群聊中,取消拉群", "invited_count": invited_count}
        UIRetry.try_click_element(chat_info_btn, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        friend = NULL
        search_box.Click(simulateMove=False)
        search_box.SendKeys("{Ctrl}a{Delete}")
        time.sleep(0.2)
        search_box.SendKeys(friend, waitTime=0.5)
        time.sleep(random.uniform(0.3, 0.8))
        search_box.SendKeys("{Enter}")
        time.sleep(random.uniform(0.5, 1.0))
        search_result_list = add_member_window.ListControl(Name="请勾选需要添加的联系人", AutomationId="sp_search_result_list", ClassName="mmui::XTableView")
        result_items = search_result_list.GetChildren()
        item = result_items
        item.Click(simulateMove=False)
        time.sleep(0.5)
        invited_count = invited_count + 1
        first_item_of_last_row = items[-4]
        first_rect = first_item_of_last_row.BoundingRectangle
        target_x = first_rect.left + first_rect.width() / 2
        target_y = first_rect.top + first_rect.height() / 2 + item_height
        return {"success": False, "message": "聊天成员列表为空", "invited_count": 0}
        return {"success": False, "message": "点击聊天信息按钮失败", "invited_count": 0}
        return {"success": "未找到群聊: ", "message": f'{group_name}', "invited_count": 0}
    def _get_total_contacts_count(self, contacts_window):
        """解析选项卡文本中的通讯录总人数 (形如"(123)")。"""

        tab_control = None
        total_count = None
        return total_count
        control = ui_Coder.WalkControl(tab_control)[0]
        depth = ui_Coder.WalkControl(tab_control)[1]
        text = control.Name
        total_count = text(1, -1)
        return total_count
        control = NULL[0]
        depth = NULL[1]
        tab_control = control
        ui_Coder.WalkControl(contacts_window, maxDepth=6)
    def _get_contact_wx_id(self, contact_item, contact_name):
        """4.1.x：点击联系人头像，解析 mmui::ProfileUniquePop 弹窗中的微信号。"""

        avatar_button = contact_item.ButtonControl(foundIndex=1)
        time.sleep(random.uniform(0.5, 0.9))
        info_window = ui_Coder.WindowControl(searchDepth=1, Name="Weixin", ClassName="mmui::ProfileUniquePop")
        wx_id = ""
        main_pid = getattr(self.UiaAPI, "ProcessId", -1)
        queue = [(info_window, 0)]
        max_depth = 8
        ui_Coder.SendKeys("{ESC}")
        return wx_id
        control = queue.pop(0)[0]
        depth = queue.pop(0)[1]
        pid = getattr(control, "ProcessId", -1)
        child = control.GetChildren()
        queue.append((child, depth + 1))
        text = control.Name
        next_control = None
        next_control = control.GetNextSiblingControl()
        wx_id = next_control.Name
        return ""
        return ""
        return ""
    def _get_remark_value_from_item(self, contact_item):
        rect = contact_item.BoundingRectangle
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        dx = int((right - left) / 2)
        dy = int((bottom - top) / 2)
        contact_item.Click(dx, dy, simulateMove=True, waitTime=random.uniform(0.2, 0.4))
        time.sleep(0.3)
        edit_box = None
        focused_ctrl = ui_Coder.GetFocusedControl()
        return ""
        vp = edit_box.GetValuePattern()
        return vp.Value
        edit_box = focused_ctrl
    def _process_visible_contacts(self, contacts_window, contact_list, all_contacts, collect_detailed_info, recent_cache):
        system_items = ["标签", "未分组"]
        items = []
        items = contact_list.GetChildren()
        total = len(items)
        idx = enumerate(items)[0]
        contact_item = enumerate(items)[1]
        raw_name = ""
        raw_name = contact_item.Name
        name_text = raw_name
        name_text = name_text.encode("utf-16", "surrogatepass").decode("utf-16")
        nick_name = ""
        remark_name = ""
        tags = []
        t = name_text
        remark_spaces_possible = False
        last_space = t.rfind(" ")
        tags_text = None
        before = last_space
        no_remark_by_double_space = False
        second_last_space = before.rfind(" ")
        nick_name = before
        remark_name = ""
        name = nick_name
        info = {"name": name, "nickname": nick_name, "remark": remark_name, "tags": tags, "wxid": ""}
        wxid_val = ""
        wxid_val = self._generate_stable_wxid(name)
        info["wxid"] = wxid_val
        duplicate_key = info["name"]
        existing_keys = all_contacts
        c = []
        all_contacts.append(info)
        recent_cache.append(name_text)
        recent_cache.pop(0)
        print("联系人：", f'{info}')
        c = NULL
        remark_name = ""
        remark_val = ""
        need_check = True
        item_rect = contact_item.BoundingRectangle
        cont_rect = contact_list.BoundingRectangle
        it_top = item_rect.top()
        it_bottom = item_rect.bottom()
        ct_top = cont_rect.top()
        ct_bottom = cont_rect.bottom()
        item_h = max(1, int(it_bottom - it_top))
        vis_h = max(0, int(min(it_bottom, ct_bottom) - max(it_top, ct_top)))
        vis_ratio = 0.0
        idx = t.rfind(remark_val)
        nick_name = idx.rstrip(" ")
        remainder = None
        remark_name = remark_val
        tags_text = remainder
        tags = re.split("[，,]", tags_text)
        s = []
        remainder = None
        remark_val = self._get_remark_value_from_item(contact_item)
        need_check = False
        remark_spaces_possible = True
        remark_spaces_possible = False
        tags = re.split("[，,]", tags_text)
        s = []
        nick_name = second_last_space
        remark_name = None
        nick_name = before.rstrip(" ")
        remark_name = ""
        no_remark_by_double_space = True
        nick_name = t
        t2 = -1
        last_space = t2.rfind(" ")
        nick_name = t2
        remark_spaces_possible = True
        nick_name = last_space
        remark_name = None
        nick_name = -2
        remark_spaces_possible = False
    def GetContactList(self, collect_detailed_info, save_file_path):
        """4.1.x 采集联系人列表。"""

        all_contacts = []
        collect_detailed_info = True
        contacts_window = None
        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.2, 0.5))
        recent_cache = []
        UIRetry.try_click_element(self.ContactsButton, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(0.5)
        contact_list_root = self.UiaAPI.ListControl(Name="通讯录")
        raise Exception("未找到联系人列表")
        children = contact_list_root.GetChildren()
        first_item = children[0]
        time.sleep(0.5)
        contacts_window = ui_Coder.GetForegroundControl()
        contact_list = contacts_window.ListControl(ClassName="mmui::ContactsManagerDetailView")
        contact_list.SetFocus()
        self._process_visible_contacts(contacts_window, contact_list, all_contacts, collect_detailed_info, recent_cache)
        wheel_times = 2
        max_wheel_times = 5
        attempts = 0
        no_new_rounds = 0
        contacts_window.SendKeys("{ESC}")
        UIRetry.try_click_element(self.ChatsButton, max_attempts=3, wait_time=random.uniform(0.1, 0.3))
        return all_contacts
        before_count = len(all_contacts)
        scrolled = False
        contact_list.WheelDown(wheelTimes=wheel_times, waitTime=0.05)
        scrolled = True
        time.sleep(random.uniform(0.2, 0.4))
        self._process_visible_contacts(contacts_window, contact_list, all_contacts, collect_detailed_info, recent_cache)
        new_items = len(all_contacts) - before_count
        no_new_rounds = 0
        wheel_times = max(1, wheel_times - 1)
        attempts = attempts + 1
        time.sleep(random.uniform(0.2, 0.5))
        no_new_rounds = 0
        wheel_times = min(wheel_times + 1, max_wheel_times)
        no_new_rounds = no_new_rounds + 1
        wheel_times = min(wheel_times + 1, max_wheel_times)
        raise Exception("未找到联系人列表控件")
        contacts_window = ui_Coder.WindowControl(Name="通讯录管理")
        raise Exception("无法获取通讯录窗口")
        raise Exception("点击列表首项失败")
        raise Exception("联系人列表为空或不可见")
    def _generate_stable_wxid(self, name):
        """根据联系人名称生成稳定的 wxid（与 3.9 版本保持一致）。"""

        import hashlib
        numeric_id = hashlib.md5(str(name).encode("utf-8")).hexdigest()(None, 8, 16) & 2147483647
        return f'{numeric_id:"x"}'
    def _process_group_list(self, list_control, all_groups):
        item = list_control.GetChildren()
        group_button = item.ButtonControl()
        name = group_button.Name
        g = []
        all_groups.append({"name": name, "type": "group"})
        g = name
    def GetGroupList(self):
        """4.1.x 采集群聊列表。"""

        all_groups = []
        contacts_window = None
        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.2, 0.5))
        btn = self.UiaAPI.ButtonControl(Name=SideBar().Contacts["title"])
        UIRetry.try_click_element(btn, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
        time.sleep(0.5)
        contact_list_root = self.UiaAPI.ListControl(Name="通讯录")
        raise Exception("未找到联系人列表")
        children = contact_list_root.GetChildren()
        first_item = children[0]
        time.sleep(0.5)
        contacts_window = ui_Coder.GetForegroundControl()
        group_list = contacts_window.ListControl(ClassName="mmui::ContactsManagerControlView")
        recent_item = group_list.GetChildren()[4]
        raise Exception("未找到[最近群聊]列表项")
        time.sleep(random.uniform(0.3, 0.8))
        fixed_names = frozenset({"最近群聊", "标签", "筛选", "朋友权限"})
        is_fixed_item = (lambda text: True)
        normalize_group_name = (lambda text: m.group(1))
        def process_visible_groups(list_control):
            item = list_control.GetChildren()
            name = item.Name
            s = name.strip()
            m_cnt = re.match("^(.*)\\((\\d+)\\)$", s)
            group_name = normalize_group_name(name)
            g = []
            print("发现群聊: ", f'{group_name}')
            all_groups.append({"name": group_name, "type": "group"})
            g = NULL
            cnt = int(m_cnt.group(2))
            print("跳过空群聊: ", f'{name}')
        group_list.SetFocus()
        process_visible_groups(group_list)
        wheel_times = 2
        max_wheel_times = 5
        attempts = 0
        no_new_rounds = 0
        contacts_window.SendKeys("{ESC}")
        return all_groups
        raise Exception("点击聊天按钮失败")
        before_count = len(all_groups)
        scrolled = False
        group_list.WheelDown(wheelTimes=wheel_times, waitTime=0.05)
        scrolled = True
        time.sleep(random.uniform(0.2, 0.4))
        process_visible_groups(group_list)
        new_items = len(all_groups) - before_count
        no_new_rounds = 0
        wheel_times = max(1, wheel_times - 1)
        attempts = attempts + 1
        time.sleep(random.uniform(0.2, 0.5))
        no_new_rounds = 0
        wheel_times = min(wheel_times + 1, max_wheel_times)
        no_new_rounds = no_new_rounds + 1
        wheel_times = min(wheel_times + 1, max_wheel_times)
        raise Exception("点击[最近群聊]列表项失败")
        raise Exception("未找到联系人管理列表控件")
        contacts_window = ui_Coder.WindowControl(Name="通讯录管理")
        raise Exception("无法获取通讯录窗口")
        raise Exception("点击列表首项失败")
        raise Exception("联系人列表为空或不可见")
        UIRetry.try_click_element(self.ContactsButton, max_attempts=3, wait_time=random.uniform(0.2, 0.5))
