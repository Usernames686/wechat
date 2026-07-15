# Decompiled from: WeChatType.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import time
from datetime import datetime
import re
from pathlib import Path
import random
import json
from typing import Optional, Dict, List
import hashlib
import uiautomation as ui_Coder
import threading
import win32clipboard
import win32clipboard as wc
import win32con
import win32api
import win32gui
import win32process
COPYDICT = {}
logger = UiaLogger().get_logger()
class WeChat:
    """WeChat"""

    _instances = {}
    _account_handle_mapping = {}
    def __new__(cls, account_id, window_handle):
        import os
        pid = os.getpid()
        logger = UiaLogger(logger_name="WeChat").get_logger()
        active_handle = cls._get_active_window_handle(logger)
        logger.warning("🎯 [智能兼容] 未找到活跃窗口句柄，请明确指定window_handle参数")
        raise ValueError("未找到活跃的微信窗口，可能微信掉线了！请先在欢迎页刷新账号再试")
        return cls._get_or_create_by_handle(active_handle, logger)
        window_handle = cls._get_handle_by_account_id(account_id, logger)
        raise ValueError("未找到活跃的微信窗口，可能微信掉线了！请先刷新账号查找可用微信窗口")
        return cls._get_or_create_by_handle(window_handle, logger)
        return cls._get_or_create_by_handle(window_handle, logger)
    def _init_attributes(self):
        """初始化实例属性"""

        self.UiaAPI = None
        self.SessionList = None
        self.SearchBox = None
        self.MsgList = None
        self.ContactButton = None
        self._driver = None
        self.db_manager = None
        self.account_info = {"nickname": None, "account_id": None, "encrypted_account_id": None}
        self.db_path = None
        self.window_handle = None
        self._initialized = False
        self._is_virtual_machine = False
        self._bound_account_id = None
        self._bound_window_handle = None
    _get_or_create_by_handle = classmethod((lambda cls, window_handle, logger: instance))
    def _ensure_driver(self):
        """确保 driver 已按绑定句柄初始化。"""

        self._driver = create_driver(window_handle=self.window_handle)
    @classmethod
    def _get_handle_by_account_id(cls, account_id, logger):
        """根据账号ID获取窗口句柄"""

        instance_manager = InstanceManagerV2()
        instances = instance_manager.list_instances()
        "🔧 [映射查找] 未找到账号 "(f'{account_id}', " 的窗口句柄")
        instance = logger.warning
        account_info = instance.get("account_info", {})
        window_handle = instance["window_handle"]
        cls._account_handle_mapping[account_id] = window_handle
        return window_handle
        window_handle = cls._account_handle_mapping[account_id]
        return window_handle
    @classmethod
    def _get_active_window_handle(cls, logger):
        """获取当前活跃的窗口句柄。

                若活跃实例已被用户标记为"退出托管"，返回 None（
                调用方 __new__ 会抛出 ValueError），以阻止自动化任务
                在已退出托管的实例上执行。

                注：WeChat(window_handle=hwnd) 和 WeChat(account_id=id) 两种
                显式调用不经过此方法，不受影响（用于重连/系统操作）。
                """

        instance_manager = InstanceManagerV2()
        active_instance = instance_manager.get_active_instance()
        logger.info("🔧 [活跃句柄] 未找到活跃窗口句柄")
        window_handle = active_instance["window_handle"]
        return window_handle
        logger.warning("🔧 [活跃句柄] 当前活动实例已退出托管，拒绝自动化创建 WeChat()")
    @classmethod
    def update_account_handle_mapping(cls, account_id, window_handle):
        """更新账号ID与窗口句柄的映射关系"""

        cls._account_handle_mapping[account_id] = window_handle
    def __init__(self, account_id, window_handle):
        pass
    def SwitchToThisWindow(self):
        self.UiaAPI.SwitchToThisWindow()
        force_focus_window(self.window_handle)
    def get_group_msg_sender(self, msg_id):
        """获取群消息发送者名称（仅4.1版本需要，3.9版本返回None）"""

        get_sender_func = getattr(self._driver, "get_group_msg_sender", None)
        return get_sender_func(msg_id)
    def initialize_multi(self, window_handle, account_info):
        """初始化微信实例（支持多实例，通过指定窗口句柄）"""

        self._initialized = False
        self.UiaAPI = None
        self.window_handle = window_handle
        WxParam.init_resolution()
        self._ensure_driver()
        drv_result = self._driver.initialize_multi(self.window_handle, account_info=account_info)
        self.UiaAPI = getattr(self._driver, "UiaAPI", None)
        self.SessionList = getattr(self._driver, "SessionList", None)
        self.SearchBox = getattr(self._driver, "SearchBox", None)
        self.MsgList = getattr(self._driver, "MsgList", None)
        self.ContactButton = getattr(self._driver, "ContactButton", None)
        self.db_manager = WeChatDBManager()
        drv_acct = None
        drv_acct = None
        self._setup_database_path()
        self.db_manager.save_account(self.account_info["nickname"], self.account_info["account_id"])
        self._initialized = True
        self._machine_code = LicenseManager().get_machine_code()
        return {"success": True, "nickname": self.account_info["nickname"], "account_id": self.account_info["account_id"]}
        import base64
        self.account_info["encrypted_account_id"] = base64.b64encode(str(self.account_info["account_id"]).encode()).decode()
        self._register_as_account_instance(self.account_info["account_id"])
        self.account_info = drv_acct
        raise Exception("LegacyUiaDriver 初始化失败: ", f'{drv_result.get("error", "未知错误")}')
        raise Exception("未检测到微信进程或 driver 初始化失败，请确保微信应用已启动！")
        logger.info("检测到虚拟机环境..")
        self._is_virtual_machine = True
        return {"success": True, "nickname": self.account_info.get("nickname", ""), "account_id": self.account_info.get("account_id", "")}
        raise Exception("未提供有效的微信窗口句柄")
    def _register_as_account_instance(self, account_id):
        """将实例注册为基于账号的实例（新架构：使用映射关系而非直接缓存）"""

        import os
        logger = UiaLogger(logger_name="WeChat").get_logger()
        logger.warning("🔧 [实例注册] 实例缺少窗口句柄，无法建立映射关系 - 账号: ", f'{account_id}')
        self.update_account_handle_mapping(account_id, self._bound_window_handle)
        self._bound_account_id = account_id
    @classmethod
    def get_instance_by_account(cls, account_id):
        """根据账号ID获取实例（新架构：通过映射关系查找）"""

        import os
        logger = UiaLogger(logger_name="WeChat").get_logger()
        "🔧 [实例查找] 查找账号 "(f'{account_id}', " 的实例")
        window_handle = cls._get_handle_by_account_id(account_id, logger)
        "🔧 [实例查找] 未找到账号 "(f'{account_id}', " 的实例")
        instance = cls._instances[window_handle]
        bound_account = getattr(instance, "_bound_account_id", None)
        f'{window_handle}'(", 绑定: ", f'{bound_account}')
        return instance
    list_all_instances = classmethod((lambda cls: instances))
    @classmethod
    def cleanup_invalid_instances(cls):
        """清理无效的实例"""

        import os
        pid = os.getpid()
        invalid_keys = []
        "清理了 "(f'{len(invalid_keys)}', " 个无效实例")
        key = logger.info
        del cls._instances[key]
        key = NULL[0]
        instance = NULL[1]
        invalid_keys.append(key)
        invalid_keys.append(key)
    def _is_instance_valid(self):
        """检查实例是否有效"""

        return False
        return self.UiaAPI.Exists(1)
    def check_connection_status(self):
        """检查微信连接状态"""

        current_windows = []
        target_classes = {"WeChatMainWndForPC", "Qt51514QWindowIcon"}
        def callback(hwnd, windows):
            return True
            class_name = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            windows.append((hwnd, title))
        win32gui.EnumWindows(callback, current_windows)
        logger.info("微信界面无响应，重新初始化...")
        return {"connected": False, "reason": "微信界面无响应"}
        version = detect_version(self.window_handle)
        return {"connected": True}
        nav_toolbar = self.UiaAPI.ToolBarControl(Name="导航")
        children = nav_toolbar.GetChildren()
        avatar_button = children[0]
        current_nickname = avatar_button.Name
        "，头像显示账号："(f'{current_nickname}', "，如果切换了微信号务必重新登录下！！")
        logger.info("未找到微信窗口，尝试切换")
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
        win32api.keybd_event(ord("W"), 0, 0, 0)
        win32api.keybd_event(ord("W"), 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)
        win32gui.EnumWindows(callback, current_windows)
        logger.info("未检测到微信窗口，重新初始化...")
        return {"connected": False, "reason": "未检测到微信窗口"}
        return {"connected": False, "reason": "微信窗口已关闭"}
    def _wait_for_wechat_window(self, max_retries, interval):
        """等待并获取微信窗口句柄，带重试机制"""

        _ = range(max_retries)
        windows = []
        target_classes = {"WeChatMainWndForPC", "Qt51514QWindowIcon"}
        def callback(hwnd, windows):
            return True
            class_name = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            windows.append((hwnd, title))
        win32gui.EnumWindows(callback, windows)
        "/"(f'{max_retries}', ")")
        time.sleep(random.uniform(0.8, 1.2))
        return windows[0][0]
        hwnd = windows[0]
        title = windows[1]
        return hwnd
    def get_image_by_id(self, msg_id, LEN):
        """根据消息ID获取图片"""

        msg_items = self.MsgList.GetChildren()
        f'{msg_id}'(", 消息列表总数: ", f'{len(msg_items)}')
        all_msg_ids = []
        truncated_ids = []
        get_last_message_id = (lambda : temp_id)
        last_message_id = get_last_message_id()
        target_item = None
        img_button = target_item.ButtonControl(Name="")
        def verify_message_list(last_id):
            """验证消息列表是否有新消息"""

            current_id = get_last_message_id()
            return current_id == last_id
        def roll_into_view(msg_list, img_button):
            max_scroll_attempts = 50
            scroll_count = 0
            scroll_count = scroll_count + 1
            msg_list.WheelDown(wheelTimes=1, waitTime=0.1)
            scroll_count = scroll_count + 1
            msg_list.WheelUp(wheelTimes=1, waitTime=0.1)
        max_attempts = 3
        attempt = 0
        time.sleep(0.5)
        copy_menu = preview_window.MenuItemControl(Name="复制")
        time.sleep(0.5)
        formats = WxUtils.ClipboardFormats()
        wc.OpenClipboard()
        image_data = None
        wc.CloseClipboard()
        from WeRobotCore.utils.data_manager import DataManager
        save_dir = os.path.join(DataManager.get_data_dir_str(), "images")
        os.makedirs(save_dir, exist_ok=True)
        from PIL import Image
        import io
        dib_stream = io.BytesIO()
        bmp_header = bytearray([], (66, 77, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0, 0))
        file_size = 14 + len(image_data)
        dib_stream.write(bmp_header)
        dib_stream.write(image_data)
        dib_stream.seek(0)
        image = Image.open(dib_stream)
        timestamp = int(time.time() * 1000)
        image_path = save_dir("image_", f'{timestamp}', ".jpg")
        image.save(image_path, "JPEG", quality=85, optimize=True)
        logger.info("图片成功保存到: ", f'{image_path}')
        preview_window.SendKeys("{Esc}")
        return image_path
        logger.info("未能从剪贴板获取图片数据")
        preview_window.SendKeys("{Esc}")
        fmt = NULL
        image_data = wc.GetClipboardData(fmt)
        raise Exception("点击复制按钮失败")
        logger.info("未找到复制菜单项")
        preview_window.SendKeys("{Esc}")
        preview_window.SendKeys("{Esc}")
        raise Exception("右击【复制】按钮失败")
        logger.info("达到最大重试次数，继续执行...")
        roll_into_view(self.MsgList, img_button)
        time.sleep(0.5)
        preview_window = ui_Coder.WindowControl(ClassName="ImagePreviewWnd", Name="图片查看")
        "消息列表已变化，正在重试... (第"(f'{attempt + 1}', "次)")
        preview_window.SendKeys("{Esc}")
        time.sleep(0.5)
        last_message_id = get_last_message_id()
        attempt = attempt + 1
        logger.info("未找到图片预览窗口")
        raise Exception("【get_image_by_id】点击图片失败")
        logger.info("未找到图片按钮控件")
        logger.warning("未找到消息ID对应的消息项: ", f'{msg_id}')
        "可能原因: 1)消息ID不在最后"(f'{len(msg_items)}', "条消息中 2)消息列表已更新 3)ID格式不匹配")
        i = logger.warning[0]
        item = logger.warning[1]
        j = []
        item_id = "".join(j, item.GetRuntimeId())
        " (索引: "(f'{i}', ")")
        target_item = item
        j = "找到消息ID对应的消息项: "
        i = str(j)[0]
        item = str(j)[1]
        j = []
        item_id = "".join(j, item.GetRuntimeId())
        f'{i}'("]", f'{item_id}')
        j = "["
        i = str(j)[0]
        item = str(j)[1]
        j = []
        item_id = "".join(j, item.GetRuntimeId())
        f'{i}'("]", f'{item_id}')
        j = "["
        return self._driver.get_image_by_id(msg_id)
    def _setup_database_path(self):
        """设置数据库路径，兼容老版本"""

        from WeRobotCore.utils.data_manager import DataManager
        data_dir = DataManager.get_data_dir_str()
        os.makedirs(data_dir, exist_ok=True)
        account_id = ""
        from WeRobotCore.core.instance_manager_v2 import InstanceManagerV2
        instance_manager = InstanceManagerV2()
        active_instance = instance_manager.get_active_instance()
        legacy_db = os.path.join(data_dir, "wechat_contacts.db")
        self.db_path = data_dir("wechat_contacts_", f'{self.window_handle}', ".db")
        self.db_path = data_dir("wechat_contacts_", f'{account_id}', ".db")
        account_id = self.account_info.get("account_id", "")
        self.db_path = legacy_db
        account_id = active_instance["account_info"].get("account_id", "")
    def _has_other_instances(self):
        """检查是否存在其他微信实例"""

        from WeRobotCore.utils.data_manager import DataManager
        data_dir = DataManager.get_data_dir_str()
        db_files = os.listdir(data_dir)
        f = []
        return len(db_files) > 0
        return False
    def _get_instance_window(self):
        """获取当前实例对应的微信窗口句柄"""

        target_classes = {"WeChatMainWndForPC", "Qt51514QWindowIcon"}
        def callback(hwnd, windows):
            return True
            class_name = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            windows.append(hwnd)
        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows[0]
        hwnd = windows
        title = win32gui.GetWindowText(hwnd)
        _ = win32process.GetWindowThreadProcessId(hwnd)[0]
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        return hwnd
        return windows[0]
    def get_current_user(self):
        """获取当前登录用户信息（供前端调用）"""

        return {"nickname": self.account_info["nickname"], "account_id": self.account_info["account_id"]}
    def get_user_id(self):
        """获取当前登录用户的ID"""

        raise WeChatUIAError("未能获取到微信账号信息")
        return self.account_info["account_id"]
        print("尝试获取账号信息")
        self.account_info = self._get_account_info()
    def _get_account_info(self):
        """获取当前登录的微信账号信息"""

        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.7, 1.2))
        account_id = None
        nickname = None
        nav_toolbar = self.UiaAPI.ToolBarControl(Name="导航")
        children = nav_toolbar.GetChildren()
        avatar_button = children[0]
        logger.info("找到头像昵称: ", f'{avatar_button.Name}')
        nickname = avatar_button.Name
        time.sleep(random.uniform(1.0, 2.0))
        time.sleep(1)
        max_retry = 3
        info_window = ui_Coder.PaneControl(ClassName="ContactProfileWnd")
        real_nick_name = None
        ui_Coder.SendKeys("{ESC}")
        time.sleep(0.5)
        f'{nickname}'(":", f'{account_id}')
        return {"nickname": nickname, "account_id": account_id}
        raise Exception("获取昵称失败")
        import hashlib
        salt = "YokoWebot_2025"
        hash_input = f'{salt}'.encode("utf-8")
        hash_obj = hashlib.sha256(hash_input)
        account_id = f'{16}'
        logger.info("未找到微信号，已生成唯一ID: ", f'{account_id}')
        control = NULL[0]
        depth = NULL[1]
        text = control.Name
        next_control = control.GetNextSiblingControl()
        account_id = next_control.Name
        logger.info("找到微信号: ", f'{account_id}')
        real_nick_name = control.Name
        logger.info("用户昵称已修改，更新为: ", f'{real_nick_name}')
        nickname = real_nick_name
        retry_count = NULL
        raise Exception("点击登录用户头像按钮失败")
        raise Exception("未找到个人信息窗口")
        raise Exception("点击登录用户头像按钮失败")
        raise Exception("第一个控件不是按钮类型")
        raise Exception("导航工具栏中未找到任何控件")
        raise Exception("未找到导航工具栏")
    def _get_total_contacts_count(self, contacts_window):
        """
                从通讯录窗口获取通讯录总人数
                通过查找选项卡控件(TabControl)及其子文本控件来获取总人数
                """

        tab_control = None
        total_count = None
        return total_count
        control = ui_Coder.WalkControl(tab_control)[0]
        depth = ui_Coder.WalkControl(tab_control)[1]
        text = control.Name
        count_str = -1
        count = int(count_str)
        total_count = count
        logger.info("好友通讯录总人数: ", f'{count}')
        return total_count
        logger.warning("未找到选项卡控件，无法获取通讯录总人数")
        control = 1[0]
        depth = 1[1]
        tab_control = control
    def GetContactList(self, collect_detailed_info, existing_names):
        all_contacts = []
        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.2, 0.5))
        time.sleep(0.5)
        contact_list = self.UiaAPI.ListControl(Name="联系人")
        max_scroll_attempts = 5
        scroll_attempts = 0
        time.sleep(random.uniform(0.2, 0.5))
        time.sleep(0.5)
        contacts_window = ui_Coder.GetForegroundControl()
        contact_list = contacts_window.ListControl()
        scroll = contact_list.GetScrollPattern()
        self._process_visible_contacts(contacts_window, contact_list, all_contacts, collect_detailed_info=collect_detailed_info, last_processed_marker=None, existing_names=existing_names)
        contacts_window.SendKeys("{ESC}")
        time.sleep(0.5)
        chat_button = self.UiaAPI.ButtonControl(Name="聊天")
        "共找到 "(f'{len(all_contacts)}', " 个联系人")
        return all_contacts
        raise Exception("点击聊天按钮失败")
        total_contacts_count = self._get_total_contacts_count(contacts_window)
        last_processed_marker = None
        initial_count = len(all_contacts)
        last_processed_marker = self._process_visible_contacts(contacts_window, contact_list, all_contacts, collect_detailed_info=collect_detailed_info, last_processed_marker=last_processed_marker, existing_names=existing_names)
        visible_items = len(all_contacts) - initial_count
        logger.info("当前可见联系人数量: ", f'{visible_items}')
        items_per_screen = 9
        current_pos = 0.0
        last_contacts_count = len(all_contacts)
        before_scroll_count = len(all_contacts)
        current_pos = current_pos + scroll_step
        scroll.SetScrollPercent(-1, min(current_pos, 1.0))
        time.sleep(random.uniform(0.2, 0.4))
        new_marker = self._process_visible_contacts(contacts_window, contact_list, all_contacts, collect_detailed_info=collect_detailed_info, last_processed_marker=last_processed_marker, existing_names=existing_names)
        new_items = len(all_contacts) - before_scroll_count
        print("新增联系人: ", f'{new_items}')
        last_contacts_count = len(all_contacts)
        logger.info("已到达列表底部")
        last_processed_marker = new_marker
        scroll_step = min(items_per_screen / total_contacts_count, 0.2)
        "根据总人数计算的滚动步长: "(f'{scroll_step * 100:".2f"}', "%")
        logger.warning("通讯录总人数为0，中止通讯录读取")
        return all_contacts
        raise Exception("未找到联系人列表控件")
        raise Exception("点击通讯录管理按钮失败")
        raise Exception("未找到通讯录管理按钮，请确保按钮可见")
        contact_manager = contact_list.ButtonControl(Name="通讯录管理")
        contact_list.WheelUp(wheelTimes=3)
        time.sleep(0.3)
        scroll_attempts = scroll_attempts + 1
        list_rect = contact_list.BoundingRectangle
        button_rect = contact_manager.BoundingRectangle
        raise Exception("未找到联系人列表")
        raise Exception("点击通讯录按钮失败")
        return self._driver.GetContactList(collect_detailed_info=collect_detailed_info)
    def _process_visible_contacts(self, contacts_window, contact_list, all_contacts, collect_detailed_info, last_processed_marker, existing_names):
        """处理当前可见的联系人列表
                Args:
                    contacts_window: 联系人窗口
                    contact_list: 联系人列表控件
                    all_contacts: 已收集的联系人列表
                    collect_detailed_info: 是否采集详细信息
                    last_processed_marker: 上次处理的最后一个联系人标记 {'runtime_id': str, 'name': str}
                    existing_names: 已存在的好友名称列表，用于增量同步。如果为None，则执行全量同步
                Returns:
                    dict: 本次处理的最后一个联系人标记，格式同last_processed_marker
                """

        system_items = ["标签", "未分组"]
        existing_wxids = all_contacts
        contact = set()
        batch_processed = 0
        start_processing = False
        current_marker = None
        contact_items = contact_list.GetChildren()
        list_rect = contact_list.BoundingRectangle
        list_bottom = list_rect.bottom
        f'{last_processed_marker.get("runtime_id", "")}'(", Name=", f'{last_processed_marker.get("name", "")}')
        skipped_count = 0
        return current_marker
        "增量同步：已跳过 "(f'{skipped_count}', " 个已存在的联系人")
        i = logger.info[0]
        contact_item = logger.info[1]
        i = []
        current_runtime_id = "".join(i, contact_item.GetRuntimeId())
        text_control = contact_item.TextControl()
        nick_name = text_control.Name
        remark_control = contact_item.ButtonControl(foundIndex=2)
        remark_name = ""
        name = nick_name
        tag_control = contact_item.ButtonControl(foundIndex=3)
        tags = []
        contact_info = {"name": name, "nickname": nick_name, "remark": remark_name, "tags": tags, "wxid": ""}
        contact_info["wxid"] = self._generate_stable_wxid(name)
        duplicate_key = name
        current_marker = {"runtime_id": current_runtime_id, "name": name}
        c = []
        all_contacts.append(contact_info)
        f'{tags}'(", 微信号: ", f'{contact_info["wxid"]}')
        existing_wxids.add(contact_info["wxid"])
        c = ", 标签: "
        wx_id = self._get_contact_wx_id(contacts_window, contact_item, name)
        contact_info["wxid"] = wx_id
        batch_processed = batch_processed + 1
        tags_text = tag_control.Name
        tags = tags_text.split("，")
        tag = []
        item_rect = contact_item.BoundingRectangle
        item_height = item_rect.bottom - item_rect.top
        visible_height = list_bottom - item_rect.top
        logger.info("最后一个联系人项被遮挡超过40%，跳过处理，等待下次滚动")
        tag.strip()
        skipped_count = skipped_count + 1
        current_marker = {"runtime_id": current_runtime_id, "name": name}
        start_processing = True
        start_processing = True
        name = name.encode("utf-16", "surrogatepass").decode("utf-16")
        remark_name = ""
        i = remark_control.Name
        start_processing = True
        contact = str(i)
    def _generate_stable_wxid(self, name):
        """
                根据联系人名称生成稳定的wxid

                Args:
                    name: 联系人名称

                Returns:
                    生成的wxid，格式为wxid_开头加上8位十六进制数字
                """

        import hashlib
        numeric_id = hashlib.md5(name.encode("utf-8")).hexdigest()(None, 8, 16) & 2147483647
        wxid = f'{numeric_id:"x"}'
        return wxid
    def _get_contact_wx_id(self, contacts_window, contact_item, contact_name):
        """获取联系人的微信号

                Args:
                    contact_item: 联系人项控件
                    contact_name: 联系人姓名

                Returns:
                    str: 微信号，获取失败返回空字符串
                """

        info_pane = None
        avatar_button = contact_item.ButtonControl(foundIndex=1)
        time.sleep(random.uniform(0.5, 0.8))
        info_pane = contacts_window.PaneControl(Name="微信")
        wx_id = ""
        time.sleep(0.3)
        return wx_id
        ui_Coder.SendKeys("{ESC}")
        control = ui_Coder.WalkControl(info_pane)[0]
        depth = ui_Coder.WalkControl(info_pane)[1]
        text = control.Name
        next_control = control.GetNextSiblingControl()
        wx_id = next_control.Name
        "采集通讯录，未找到个人信息面板，跳过获取 "(f'{contact_name}', " 的微信号")
        return ""
        "采集通讯录，未找到通讯录窗口，跳过获取 "(f'{contact_name}', " 的微信号")
        return ""
        "采集通讯录，点击联系人 "(f'{contact_name}', " 的头像失败")
        return ""
        "未找到联系人 "(f'{contact_name}', " 的头像按钮")
        return ""
    def sync_contacts(self, collect_detailed_info, existing_names):
        """
                同步当前微信账号的所有联系人到数据库

                Args:
                    collect_detailed_info: 是否采集详细信息，默认为True
                    existing_names: 已存在的好友名称列表，用于增量同步。如果为None，则执行全量同步

                Returns:
                    dict: 同步结果，包含成功状态和同步统计信息
                """

        sync_mode = "全量同步"
        "开始"(f'{sync_mode}', "通讯录")
        contacts = self.GetContactList(collect_detailed_info=collect_detailed_info, existing_names=existing_names)
        is_incremental = sync_mode == "增量同步"
        self.db_manager.save_friends(self.account_info["account_id"], contacts, is_incremental=is_incremental)
        return {"success": f'{len(contacts)}', "message": " 个好友到数据库", "contacts_count": len(contacts)}
        logger.warning(f'{sync_mode}', "获取联系人列表为空，跳过保存")
        return {"success": f'{sync_mode}', "message": "获取联系人列表为空", "contacts_count": 0}
    def GetGroupList(self):
        logger.info("开始同步群聊列表")
        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.2, 0.5))
        time.sleep(0.5)
        contact_list = self.UiaAPI.ListControl(Name="联系人")
        contact_manager = contact_list.ButtonControl(Name="通讯录管理")
        time.sleep(0.5)
        contacts_window = ui_Coder.GetForegroundControl()
        recent_groups_pane = contacts_window.PaneControl(Name="最近群聊")
        time.sleep(0.5)
        next_pane = recent_groups_pane.GetNextSiblingControl()
        raise Exception("未找到群聊列表所在窗格")
        child_pane = next_pane.PaneControl()
        group_list = child_pane.ListControl()
        all_groups = []
        process_group_list = (lambda list_control: ...)
        find_group_list = (lambda pane: ...)
        find_group_list(next_pane)
        "共找到 "(f'{len(all_groups)}', " 个群聊")
        contacts_window.SendKeys("{ESC}")
        time.sleep(0.5)
        chat_button = self.UiaAPI.ButtonControl(Name="聊天")
        return all_groups
        raise Exception("点击聊天按钮失败")
        list_controls = []
        raise Exception("未找到群聊列表控件")
        group_list = list_controls[0]
        control = child_pane.GetChildren()
        rect = control.BoundingRectangle
        list_controls.append(control)
        raise Exception("未找到群聊列表子窗格")
        raise Exception("点击最近群聊按钮失败")
        raise Exception("未找到最近群聊窗格")
        raise Exception("点击通讯录管理按钮失败")
        logger.info("未找到通讯录管理按钮，尝试滚动获取")
        max_scroll_attempts = 5
        scroll_attempts = 0
        raise Exception("未找到通讯录管理按钮，请确保按钮可见")
        contact_list.WheelUp(wheelTimes=3)
        time.sleep(0.3)
        scroll_attempts = scroll_attempts + 1
        list_rect = contact_list.BoundingRectangle
        button_rect = contact_manager.BoundingRectangle
        raise Exception("未找到联系人列表")
        raise Exception("点击通讯录按钮失败")
        return self._driver.GetGroupList()
    def _process_visible_groups(self, group_list_control, all_groups):
        """处理当前可见的群聊列表"""

        group_item = group_list_control.GetChildren()
        text_control = group_item.TextControl()
        group_name = text_control.Name
        g = []
        group_info = {"name": group_name, "type": "group"}
        all_groups.append(group_info)
        logger.info("找到群聊: ", f'{group_name}')
        g = NULL
    def sync_groups(self):
        """同步当前微信账号的所有群聊到数据库"""

        groups = self.GetGroupList()
        self.db_manager.save_groups(self.account_info["account_id"], groups)
        "成功同步 "(f'{len(groups)}', " 个群聊到数据库")
        config_manager = ConfigManager(self.account_info["account_id"])
        config_manager.update_group_cache(True)
        return True
        logger.warning("获取群聊列表为空，跳过保存")
        return True
        logger.info("未能获取到当前微信账号信息")
        return False
    def get_latest_sessions(self, limit, reset, time_limit_minutes, official_keywords, visible_sessions, cutoff_timestamp):
        """
                通用的会话列表解析方法，支持不同的时间限制和过滤条件

                Args:
                    limit (int): 限制扫描的会话数量，默认10条
                    reset (bool): 是否重置会话列表缓存
                    time_limit_minutes (int): 时间限制（分钟），0表示不限制时间，默认5分钟
                    official_keywords (List[str]): 需要过滤的官方账号关键词列表，None使用默认列表
                    visible_sessions (List): 可见会话列表，None则自动获取

                Returns:
                    list: 会话列表，每个会话包含 name, lastMessage, lastTime, unread 等信息
                """

        bound_account = getattr(self, "_bound_account_id", None)
        session_list = []
        current_time = time.time()
        time_limit_ago = 0
        "分钟前 ("(f'{time_limit_ago}', ")")
        return session_list
        session = limit
        original_name = session.Name
        logger.info("原始会话名称: ", f'{original_name}')
        clean_name = None
        button = session.ButtonControl()
        session_id = f'{clean_name}'("_", f'{self._machine_code}'.encode("utf-8")).hexdigest()(None, 8, 16) & 2147483647
        session_info = {"id": session_id, "name": clean_name, "avatar": "", "lastMessage": "", "lastTime": "", "unread": 0, "is_at": False}
        ui_Coder.SetGlobalSearchTimeout(0.1)
        text_controls = []
        second_text = text_controls[1].Name
        time_str = ""
        last_message = ""
        time_str = second_text
        "忽略会话 "(f'{clean_name}', ": 缺少消息内容或时间")
        ui_Coder.SetGlobalSearchTimeout(5.0)
        session_info["lastMessage"] = last_message
        session_info["lastTime"] = time_str
        msg_time = WxUtils._parse_wx_time(time_str, current_time)
        f'{datetime.fromtimestamp(msg_time).strftime("%Y-%m-%d %H:%M:%S")}'("),当前时间：", f'{current_time}')
        ") 晚于时间限制 ("(f'{time_limit_ago}', ")")
        session_list.append(session_info)
        ui_Coder.SetGlobalSearchTimeout(5.0)
        suffix = original_name.replace(clean_name, "")
        unread_match = re.search("(\\d+)条新消息$", suffix)
        logger.info("无法从后缀提取未读消息数: ", f'{suffix}')
        session_info["unread"] = int(unread_match.group(1))
        ") 早于时间限制 ("(f'{time_limit_ago}', ")")
        nickname = self.account_info["nickname"]
        session_info["is_at"] = True
        last_message = re.sub("^\\[有人@我\\]", "", last_message).strip()
        session_info["is_at"] = True
        ui_Coder.SetGlobalSearchTimeout(5.0)
        last_message = text_controls[2].Name
        last_message = text_controls[3].Name
        time_str = text_controls[2].Name
        "忽略会话 "(f'{clean_name}', ": 文本控件数量不足")
        "忽略会话 "(f'{clean_name}', ": 文本控件数量不足")
        ui_Coder.SetGlobalSearchTimeout(5.0)
        control = print[0]
        depth = print[1]
        text_controls.append(control)
        clean_name = re.sub("(\\d+条新消息|已置顶)$", "", original_name).strip()
        logger.info("会话名称: ", f'{clean_name}')
        candidate_name = button.Name
        clean_name = candidate_name
        visible_sessions = self.SessionList.GetChildren()
        time_limit_ago = cutoff_timestamp
        " ("(f'{datetime.fromtimestamp(time_limit_ago).strftime("%Y-%m-%d %H:%M:%S")}', ")")
        return self._driver.get_latest_sessions(limit=limit, reset=reset, time_limit_minutes=time_limit_minutes, official_keywords=official_keywords, visible_sessions=visible_sessions, cutoff_timestamp=cutoff_timestamp)
        official_keywords = ("订阅号", "服务号", "微信支付", "微信游戏", "已停用的微信用户", "微信团队", "微信广告助手", "微信小店助手", "微信支付助手", "服务通知", "公众号", "腾讯充值", "折叠置顶聊天")
    def _parse_wx_time(self, time_str, current_time):
        """
                解析微信时间显示格式为时间戳

                Args:
                    time_str: 微信显示的时间文本 (如："12:30"、"昨天"、"星期一"等)
                    current_time: 当前时间戳

                Returns:
                    float: 消息时间戳，解析失败返回None
                """

        current_date = time.localtime(current_time)
        weekday = current_date.tm_wday
        days_map = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6}
        day = days_map.items()[0]
        offset = days_map.items()[1]
        target_weekday = offset
        days_diff = weekday - target_weekday
        return current_time - days_diff * 86400
        days_diff = days_diff + 7
        return current_time - 86400
        hour = map(int, time_str.split(":"))[0]
        minute = map(int, time_str.split(":"))[1]
        msg_time = time.mktime((current_date.tm_year, current_date.tm_mon, current_date.tm_mday, hour, minute, 0, 0, 0, 0))
        return msg_time + 59
        msg_time = msg_time - 86400
        a = map(int, time_str.split("/"))[0]
        b = map(int, time_str.split("/"))[1]
        c = map(int, time_str.split("/"))[2]
        year = None
        month = None
        day = None
        day = c
        month = b
        year = 2000 + a
        msg_time = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        return msg_time
        day = b
        month = a
        year = 2000 + c
        day = a
        month = b
        year = 2000 + c
        day = b
        month = a
        year = c
        day = a
        month = b
        year = c
        day = c
        month = b
        year = a
        parts = time_str.strip().split()
        period = parts[0]
        time_part = parts[1]
        hour = int(time_part)
        minute = 0
        msg_time = time.mktime((current_date.tm_year, current_date.tm_mon, current_date.tm_mday, hour, minute, 0, 0, 0, 0))
        return msg_time
        hour = 0
        hour = 0
        hour = hour + 12
        hour = hour + 12
        hour = map(int, time_part.split(":"))[0]
        minute = map(int, time_part.split(":"))[1]
        raise ValueError("无效的时间格式: ", f'{time_str}')
        return current_time
    def Search(self, keyword):
        """
                查找微信好友或关键词
                keywords: 要查找的关键词，str   * 最好完整匹配，不完全匹配只会选取搜索框第一个
                """

        self.UiaAPI.SetFocus()
        time.sleep(random.uniform(0.2, 0.5))
        self.UiaAPI.SendKeys("{Ctrl}f", waitTime=1)
        import pyperclip
        original_keyword = keyword
        pyperclip.copy(keyword)
        self.SearchBox.SendKeys("{Ctrl}v", waitTime=1.5)
        time.sleep(random.uniform(0.2, 0.5))
        def search_back():
            self.UiaAPI.SetFocus()
            time.sleep(random.uniform(0.2, 0.5))
            self.SearchBox.SendKeys("{Ctrl}a{Delete}", waitTime=1)
            self.UiaAPI.SendKeys("{Esc}", waitTime=1)
            self.SwitchToThisWindow()
        time.sleep(random.uniform(0.5, 1.0))
        search_list = None
        search_list = self.UiaAPI.ListControl(Name="@str:IDS_FAV_SEARCH_RESULT:3780")
        search_items = search_list.GetChildren()
        logger.info("未找到精确匹配的会话: ", f'{keyword}')
        search_back()
        return False
        item = NULL
        real_name = None
        button = item.ButtonControl()
        real_name = button.Name
        logger.info("搜索找到会话: ", f'{real_name}')
        return True
        raise Exception("点击搜索好友item失败")
        first_item = search_items[0]
        return True
        raise Exception("点击搜索好友item失败")
        logger.info("未找到匹配的会话")
        search_back()
        return False
        logger.info("未找到任何搜索结果")
        search_back()
        return False
        logger.info("未找到搜索结果列表控件")
        return False
        encoded = keyword.encode("utf-8")
        keyword = (32).decode("utf-8", errors="ignore")
        logger.info("昵称过长，已安全截取: ", f'{keyword}')
        keyword = (31).decode("utf-8", errors="ignore")
    def get_chat_window_type(self, who):
        """
                获取当前聊天窗口的类型
                Args:
                    who: str, 会话的名称
                Returns:
                    str: 聊天窗口类型
                        - "official_account": 服务号/公众号
                        - "group": 群聊
                        - "chat": 好友
                        - "unknown": 未知类型或获取失败
                """

        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.2, 0.4))
        official_btn = self.UiaAPI.ButtonControl(Name="公众号主页")
        chat_info_btn = self.UiaAPI.ButtonControl(Name="聊天信息")
        logger.info("无法确定聊天窗口类型")
        return "unknown"
        return "chat"
        control = ui_Coder.WalkControl(self.UiaAPI, maxDepth=15)[0]
        depth = ui_Coder.WalkControl(self.UiaAPI, maxDepth=15)[1]
        name = control.Name
        return "group"
        return "official_account"
        logger.info("微信窗口不存在")
        return "unknown"
        return self._driver.get_chat_window_type(who)
    def get_friend_info_from_chat(self, who):
        """
                从好友聊天窗口获取好友信息（微信号、备注名等）
                Args:
                    who: str, 好友的名称
                Returns:
                    Dict: 好友信息
                        - "success": bool, 是否成功获取
                        - "wechat_id": str, 微信号
                        - "remark_name": str, 备注名
                        - "nickname": str, 昵称
                        - "message": str, 错误信息（如果失败）
                """

        time.sleep(random.uniform(0.2, 0.4))
        chat_type = self.get_chat_window_type(who)
        chat_info_btn = self.UiaAPI.ButtonControl(Name="聊天信息")
        time.sleep(random.uniform(1.0, 2.0))
        members_list = self.UiaAPI.ListControl(Name="聊天成员")
        items = members_list.GetChildren()
        first_item = None
        time.sleep(random.uniform(1.5, 2.5))
        info_pane = self.UiaAPI.PaneControl(Name="微信")
        friend_info = {"success": True, "nickname": who, "wechat_id": "", "remark_name": "", "tags": "", "chat_type": chat_type}
        logger.info("成功获取好友信息: ", f'{friend_info}')
        time.sleep(random.uniform(0.8, 1.5))
        return friend_info
        ui_Coder.SendKeys("{ESC}")
        time.sleep(random.uniform(0.5, 0.8))
        control = NULL[0]
        depth = NULL[1]
        edit_name = control.Name
        friend_info["remark_name"] = edit_name.strip()
        logger.info("找到备注名: ", f'{edit_name}')
        text = control.Name
        next_control = control.GetNextSiblingControl()
        tags = next_control.Name.strip()
        friend_info["tags"] = tags
        logger.info("找到标签: ", f'{tags}')
        next_control = control.GetNextSiblingControl()
        wechat_id = next_control.Name.strip()
        friend_info["wechat_id"] = wechat_id
        logger.info("找到微信号: ", f'{wechat_id}')
        return {"success": False, "message": "未找到个人信息面板"}
        return {"success": False, "message": "点击好友头像失败"}
        return {"success": False, "message": "未找到有效的好友成员项"}
        item = NULL
        first_item = item
        return {"success": False, "message": "聊天成员列表为空"}
        return {"success": False, "message": "未找到聊天成员列表"}
        return {"success": False, "message": "点击聊天信息按钮失败"}
        return {"success": False, "message": "未找到聊天信息按钮"}
        return {"success": "当前窗口不是好友聊天，类型: ", "message": f'{chat_type}', "chat_type": chat_type}
        return self._driver.get_friend_info_from_chat(who)
    def ChatWith(self, who, RollTimes):
        """
                打开某个聊天框
                who : 要打开的聊天框好友名，str
                """

        original_who = who
        edit_msg = self.UiaAPI.EditControl(Name=who)
        current_name = None
        suffix = " 按住 Ctrl + Win  使用语音输入文字"
        target_name_with_suffix = f'{suffix}'
        return 1
        logger.debug("窗口不一致，需要切换")
        self.SwitchToThisWindow()
        def find_in_visible_area(who):
            """在当前可见区域查找会话"""

            visible_sessions = self.SessionList.GetChildren()
            session_list_rect = self.SessionList.BoundingRectangle
            logger.info("find_in_visible_area：没找到会话 ", f'{who}')
            return False
            session = NULL
            session_rect = session.BoundingRectangle
            visible_top = max(session_rect.top, session_list_rect.top)
            visible_bottom = min(session_rect.bottom, session_list_rect.bottom)
            visible_height = max(0, visible_bottom - visible_top)
            total_height = session_rect.bottom - session_rect.top
            visible_ratio = visible_height / total_height
            button = session.ButtonControl()
            text_control = None
            original_name = session.Name
            real_name = re.sub("(\\d+条新消息|已置顶)$", "", original_name).strip()
            logger.info("find_in_visible_area：找到会话 ", f'{who}')
            max_switch_retries = 3
            switch_attempt = range(max_switch_retries)
            time.sleep(random.uniform(0.4, 0.8))
            current_session = self.UiaAPI.TextControl(Name=who)
            "会话切换失败："(f'{who}', "，已达到最大重试次数")
            return False
            time.sleep(random.uniform(0.8, 1.2))
            ui_Coder.WalkControl(session, maxDepth=4)
            return True
            time.sleep(2.0)
            raise "点击会话"(f'{who}', "失败")
            real_name = text_control.Name
            control = Exception[0]
            depth = Exception[1]
            text_control = control
            real_name = button.Name
            logger.debug("跳过被遮挡的会话控件，可见比例: ", f'{visible_ratio:".2f"}')
        first_item = self.SessionList.GetFirstChildControl()
        "在会话列表中未找到 "(f'{who}', "，尝试搜索")
        self.Search(who)
        time.sleep(1)
        logger.info("未能找到会话: ", f'{who}')
        return 0
        return 1
        first_item_rect = first_item.BoundingRectangle
        list_rect = self.SessionList.BoundingRectangle
        logger.info("列表不在顶部，开始动态滚动到顶部")
        max_scroll_attempts = 10
        scroll_count = 0
        time.sleep(random.uniform(0.3, 0.5))
        return 1
        "达到最大滚动次数("(f'{max_scroll_attempts}', ")，停止滚动")
        self.SessionList.WheelUp(wheelTimes=5, waitTime=random.uniform(0.1, 0.2))
        time.sleep(random.uniform(0.2, 0.4))
        first_item = self.SessionList.GetFirstChildControl()
        first_item_rect = first_item.BoundingRectangle
        list_rect = self.SessionList.BoundingRectangle
        position_diff = abs(first_item_rect.top - list_rect.top)
        "次，位置差异: "(f'{position_diff}', "像素")
        scroll_count = scroll_count + 1
        "已滚动到顶部，共滚动"(f'{scroll_count + 1}', "次")
        logger.warning("无法获取第一个子控件，停止滚动")
        return 1
        edit_msg = self._driver._get_edit_control(who)
        who = -3
        return self._driver.ChatWith(who, RollTimes=RollTimes)
        msg = "WeChat 实例未初始化, 请先初始化微信实例"
        logger.error(msg)
        raise RuntimeError(msg)
    def SendVoice(self, mp3_path, who):
        """
                将 mp3 文件作为语音消息发送给 who。委托给驱动 send_voice 实现。

                Phase A：驱动侧目前为 stub 直接返回 False；调用方应在失败后静默回退
                到 SendMsg 文字路径。
                """

        return False
        return bool(self._driver.send_voice(who=who, mp3_path=mp3_path))
        self._ensure_driver()
    def SendMsg(self, msg, who, clear, quote_msg_id):
        max_retries = 2
        retry_count = 0
        try_send_with_keyboard = (lambda : True)
        try_send_with_button = (lambda : UIRetry.try_click_element(send_button, max_attempts=3, wait_time=random.uniform(0.3, 0.5)))
        def fallback_send_by_typing(text):
            logger.info("尝试直接输入兜底...")
            self.EditMsg.SetFocus()
            time.sleep(random.uniform(0.2, 0.4))
            vpat = None
            vpat = self.EditMsg.GetValuePattern()
            filled = False
            time.sleep(random.uniform(0.2, 0.4))
            return True
            time.sleep(random.uniform(0.3, 0.5))
            raise Exception("兜底发送消息失败")
            s = str(text)
            s = s.replace("{", "{{}").replace("}", "{}}")
            self.EditMsg.SendKeys(s, waitTime=random.uniform(0.2, 0.4))
            vpat.SetValue(str(text))
            filled = True
        "/"(f'{max_retries}', ")")
        time.sleep(random.uniform(0.3, 0.5))
        self.SwitchToThisWindow()
        self.EditMsg = self.UiaAPI.EditControl(Name=who)
        last_msg = None
        msg_items = self.MsgList.GetChildren()
        import pyperclip
        max_copy_retries = 3
        copy_success = False
        max_paste_retries = 2
        time.sleep(random.uniform(0.3, 0.8))
        new_msg_items = self.MsgList.GetChildren()
        raise Exception("无法验证消息是否发送成功")
        new_last_msg = None
        drv_name = self._driver.get_driver_name()
        new_last_msg = WxUtils.SplitMessage(new_msg_items[-1])
        raise Exception("消息可能未成功发送（最后一条消息未更新）")
        return True
        new_last_msg = WxUtils.SplitMessage41x(new_msg_items[-1])
        return False
        paste_attempt = range(max_paste_retries)
        self.EditMsg.SetFocus()
        time.sleep(random.uniform(0.3, 0.6))
        current_text = self.EditMsg.GetValuePattern().Value
        self.EditMsg.SendKeys("{Ctrl}v", waitTime=random.uniform(0.3, 0.5))
        time.sleep(random.uniform(0.3, 0.5))
        new_text = self.EditMsg.GetValuePattern().Value
        new_text = self.EditMsg.GetValuePattern().Value
        time.sleep(random.uniform(0.2, 0.4))
        range(max_copy_retries)
        time.sleep(random.uniform(0.3, 0.5))
        raise Exception("发送消息失败")
        raise Exception("粘贴操作未生效")
        time.sleep(random.uniform(0.3, 0.5))
        paste_menu = self.UiaAPI.MenuItemControl(Name="粘贴")
        time.sleep(random.uniform(0.3, 0.5))
        raise Exception("点击粘贴按钮失败")
        raise Exception("右击【聊天编辑框】按钮失败")
        logger.warning("剪贴板复制失败，尝试直接写入")
        raise Exception("复制失败且直接输入失败")
        copy_attempt = f'{retry_count + 1}'
        pyperclip.copy("")
        time.sleep(random.uniform(0.1, 0.3))
        pyperclip.copy(str(msg))
        clipboard_content = pyperclip.paste()
        raise Exception("剪贴板内容与预期不符")
        copy_success = True
        raise Exception("复制到剪贴板失败")
        pyperclip.copy(msg)
        self.EditMsg.SetFocus()
        time.sleep(random.uniform(0.1, 0.3))
        self.EditMsg.SendKeys("{Ctrl}a", waitTime=0.2)
        self.EditMsg.SendKeys("{Delete}", waitTime=0.2)
        drv_name = self._driver.get_driver_name()
        last_msg = WxUtils.SplitMessage(msg_items[-1])
        last_msg = WxUtils.SplitMessage41x(msg_items[-1])
        print("未找到消息输入框，尝试设置输入框焦点..")
        self.EditMsg.SetFocus()
        raise Exception("未找到消息编辑框")
        self.EditMsg = self._driver._get_edit_control(who)
        logger.warning("引用消息失败: ", f'{quote_msg_id}')
        logger.info("成功引用消息: ", f'{quote_msg_id}')
        clear = False
        who = -3
        error_msg = "SendMsg 调用失败: 未初始化，请先初始化微信实例"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    def SendFiles(self):
        """向当前聊天窗口发送文件
                not_exists: 如果未找到指定文件，继续或终止程序
                *filepath: 要复制文件的绝对路径"""

        time.sleep(random.uniform(0.5, 1.5))
        key = ""
        time.sleep(random.uniform(0.3, 1.0))
        wc.OpenClipboard()
        wc.EmptyClipboard()
        time.sleep(random.uniform(0.1, 0.3))
        wc.SetClipboardData(13, "")
        wc.SetClipboardData(16, b'\x04\x08\x00\x00')
        wc.SetClipboardData(1, b'')
        wc.SetClipboardData(7, b'')
        wc.CloseClipboard()
        self.SendClipboard()
        return 1
        i = COPYDICT
        copydata = COPYDICT[i].replace(b'<EditElement type="0" pasteType="0"><![CDATA[ ]]></EditElement>', key.encode()).replace(b'type="0"', b'type="3"')
        wc.SetClipboardData(int(i), copydata)
        time.sleep(random.uniform(0.02, 0.08))
        time.sleep(random.uniform(0.02, 0.1))
        time.sleep(random.uniform(0.03, 0.12))
        time.sleep(random.uniform(0.05, 0.15))
        time.sleep(random.uniform(0.2, 0.5))
        self.EditMsg.SendKeys(" ", waitTime=random.uniform(0.1, 0.3))
        time.sleep(random.uniform(0.1, 0.3))
        self.EditMsg.SendKeys("{Ctrl}a", waitTime=random.uniform(0.1, 0.3))
        time.sleep(random.uniform(0.2, 0.4))
        self.EditMsg.SendKeys("{Ctrl}c", waitTime=random.uniform(0.1, 0.3))
        time.sleep(random.uniform(0.3, 0.6))
        self.EditMsg.SendKeys("{Delete}", waitTime=random.uniform(0.1, 0.3))
        COPYDICT = WxUtils.CopyDict()
        return 0
        file = filepath
        file = os.path.realpath(file)
        key = key + "<EditElement type=\"3\" filepath=\"%s\" shortcut=\"\" />" % file
        raise ValueError("param not_exists only \"ignore\" or \"raise\" supported")
        raise FileExistsError("File Not Exists: %s" % file)
        logger.info("File not exists:", file)
        self.MsgList.WheelDown(wheelTimes=random.randint(1, 2))
        time.sleep(random.uniform(0.3, 0.8))
        self.MsgList.WheelUp(wheelTimes=random.randint(1, 2))
        time.sleep(random.uniform(0.2, 0.6))
    def SendClipboard(self, who):
        """向当前聊天页面发送剪贴板复制的内容"""

        self.SendMsg("{Ctrl}v", who)
    def get_all_messages(self, parse_file, LEN, session_name):
        """获取当前窗口中加载的所有聊天记录"""

        AllMsg = []
        time.sleep(random.uniform(0.2, 0.4))
        MsgItems = self.MsgList.GetChildren()
        has_voice_msg = False
        return AllMsg
        i = enumerate(MsgItems)[0]
        MsgItem = enumerate(MsgItems)[1]
        msg_data = WxUtils.SplitMessage(MsgItem, parse_file)
        AllMsg.append(msg_data)
        logger.info("检测到语音消息，等待语音转文本完成...")
        time.sleep(2)
        MsgItem = MsgItems
        has_voice_msg = True
        MsgItems = None
        return self._driver.get_all_messages(parse_file=parse_file, LEN=LEN, session_name=session_name)
    def get_current_session_messages(self, max_messages):
        """获取当前会话的消息（解耦版本，只负责获取原始消息数据）"""

        logger.info("开始获取当前会话消息，最大数量: ", f'{max_messages}')
        has_more_messages = self._check_has_more_messages_button()
        all_messages = self.get_all_messages(parse_file=True, LEN=max_messages)
        " 条原始消息，"(f'{"无"}', "更多历史消息")
        return {"messages": all_messages, "has_more_messages": has_more_messages}
        logger.info("未获取到消息")
        return {"messages": [], "has_more_messages": has_more_messages}
    def _check_has_more_messages_button(self):
        """检查是否存在'查看更多消息'按钮（只检查第一个位置）"""

        msg_items = self.MsgList.GetChildren()
        first_item = msg_items[0]
        control_type = getattr(first_item, "ControlType", "Unknown")
        control_type_name = getattr(first_item, "ControlTypeName", "Unknown")
        name = getattr(first_item, "Name", "")
        legacy_name = getattr(first_item, "LegacyIAccessibleName", "")
        runtime_id = "Unknown"
        f'{legacy_name}'("', RuntimeId: ", f'{runtime_id}')
        logger.info("第一个位置不是'查看更多消息'按钮，已加载全部消息")
        return False
        button_text = getattr(first_item, "Name", "")
        "检测到按钮控件，文本内容: '"(f'{button_text}', "'")
        logger.info("检测到'查看更多消息'按钮，存在更多历史消息")
        return True
        i = []
        i = "".join(i, first_item.GetRuntimeId())
        return False
    def _scroll_to_load_more_messages(self):
        """滚动到'查看更多消息'按钮并触发加载"""

        msg_items = self.MsgList.GetChildren()
        first_item = msg_items[0]
        more_button = None
        control_type = getattr(first_item, "ControlType", "Unknown")
        control_type_name = getattr(first_item, "ControlTypeName", "Unknown")
        name = getattr(first_item, "Name", "")
        legacy_name = getattr(first_item, "LegacyIAccessibleName", "")
        runtime_id = "Unknown"
        f'{legacy_name}'("', RuntimeId: ", f'{runtime_id}')
        i = []
        original_runtime_id = "".join(i, more_button.GetRuntimeId())
        logger.info("找到'查看更多消息'按钮，RuntimeId: ", f'{original_runtime_id}')
        msg_list_rect = self.MsgList.BoundingRectangle
        button_rect = more_button.BoundingRectangle
        scroll_count = 0
        max_scroll_count = 10
        logger.warning("无法将'查看更多消息'按钮滚动到可见位置")
        return False
        logger.info("'查看更多消息'按钮已可见，等待微信自动加载")
        time.sleep(2.0)
        i = []
        current_runtime_id = "".join(i, more_button.GetRuntimeId())
        return True
        " -> 新:"(f'{current_runtime_id}', ")")
        return True
        i = f'{original_runtime_id}'
        f'{button_rect.top}'(", msg_list_rect.top: ", f'{msg_list_rect.top}')
        self.MsgList.WheelUp(wheelTimes=5, waitTime=0.1)
        time.sleep(0.5)
        current_button_rect = more_button.BoundingRectangle
        button_rect = more_button.BoundingRectangle
        scroll_count = scroll_count + 1
        logger.info("按钮top值为0，历史记录已加载完成，停止滚动")
        return True
        i = "次)，top: "
        logger.info("第一个位置不是'查看更多消息'按钮，无更多历史消息")
        return False
        button_text = getattr(first_item, "Name", "")
        "滚动检测 - 检测到按钮控件，文本内容: '"(f'{button_text}', "'")
        more_button = first_item
        i = []
        i = "".join(i, first_item.GetRuntimeId())
        return False
    def _check_time_limit_reached(self, messages, target_time_minutes):
        """检查是否已达到目标时间限制"""

        earliest_message = messages[-1]
        return False
        earliest_time_str = earliest_message[1]
        earliest_time = TimeParser.parse_time(earliest_time_str)
        return False
        earliest_time_minutes = int(earliest_time.timestamp() // 60) * 60
        logger.info("已达到目标时间限制，最早消息时间: ", f'{earliest_time_str}')
        return True
        return False
    def load_more_history_messages(self, target_time_minutes, max_attempts):
        """智能加载更多历史消息（基于'查看更多消息'按钮定位）"""

        logger.info("开始加载历史消息，目标时间: ", f'{target_time_minutes}')
        initial_messages = self.get_all_messages(parse_file=True, LEN=200)
        initial_count = 0
        logger.info("初始消息数量: ", f'{initial_count}')
        load_attempts = 0
        final_messages = self.get_all_messages(parse_file=True, LEN=200)
        final_count = 0
        logger.info("历史消息加载完成，最终消息数量: ", f'{final_count}')
        return []
        return final_messages
        load_attempts = load_attempts + 1
        "第"(f'{load_attempts}', "次尝试加载历史消息")
        success = self._scroll_to_load_more_messages()
        time.sleep(3.0)
        current_messages = self.get_all_messages(parse_file=True, LEN=200)
        current_count = 0
        f'{initial_count}'(" -> ", f'{current_count}')
        initial_count = current_count
        logger.info("已达到目标时间限制，停止加载")
        logger.info("未检测到新消息加载，停止尝试")
        logger.info("无法找到或滚动到'查看更多消息'按钮，停止加载")
    def _scroll_to_message_top(self):
        """滚动到消息列表顶部"""

        logger.info("滚动到消息列表顶部")
        max_attempts = 5
        logger.info("滚动到顶部完成")
        return True
        attempt = range(max_attempts)
        self.MsgList.WheelUp(wheelTimes=1000, waitTime=0.1)
        time.sleep(1.0)
        current_messages = self.get_all_messages(parse_file=True, LEN=50)
        "已到达消息列表顶部 (尝试"(f'{attempt + 1}', "次)")
        return True
    def get_session_last_message_time(self, session_name):
        """获取会话最后消息时间"""

        messages = self.get_all_messages(parse_file=False, LEN=5, session_name=session_name)
        msg = reversed(messages)
        content = msg[1]
        sender = msg[0]
        datetime.now().isoformat()
        return "???"
        logger.error("无法切换到会话: ", f'{session_name}')
    def determine_session_type(self, session_name):
        """确定会话类型（好友、群聊、公众号等）"""

        chat_type = self.get_chat_window_type(session_name)
        type_mapping = {"official_account": "official", "group": "group", "chat": "friend", "unknown": "unknown"}
        return type_mapping.get(chat_type, "unknown")
        return "unknown"
    def filter_friend_sessions(self, sessions):
        """过滤出好友会话（排除群聊和公众号）"""

        friend_sessions = []
        "过滤完成，共找到 "(f'{len(friend_sessions)}', " 个好友会话")
        return friend_sessions
        session = logger.info
        session_name = session.get("name", "")
        session_type = self.determine_session_type(session_name)
        session["session_type"] = session_type
        " (类型: "(f'{session_type}', ")")
        friend_sessions.append(session)
        logger.info("添加好友会话: ", f'{session_name}')
    def get_sessions_for_collection(self, max_sessions, time_limit_days):
        """为聊天记录采集获取会话列表（包含完整的滚动分页逻辑）"""

        "，时间限制: "(f'{time_limit_days}', "天")
        cutoff_timestamp = 0
        time_limit_minutes = 0
        collection_official_keywords = ("订阅号", "服务号", "微信支付", "微信游戏", "已停用的微信用户", "微信团队", "微信广告助手", "微信小店助手", "微信支付助手", "服务通知", "腾讯充值", "折叠置顶聊天", "文件传输助手")
        collection_manager = ChatCollectionManager()
        saved_official_accounts = collection_manager.load_official_accounts()
        self._scroll_to_session_list_top()
        all_sessions = []
        page_size = 20
        scroll_attempts = 0
        max_scroll_attempts = 20
        no_new_sessions_count = 0
        max_no_new_sessions = 3
        "采集完成，共获取到 "(f'{len(all_sessions)}', " 个符合条件的会话")
        return all_sessions
        visible_sessions = self.SessionList.GetChildren()
        current_sessions = page_size
        page_sessions = self.get_latest_sessions(limit=len(current_sessions), reset=False, time_limit_minutes=time_limit_minutes, official_keywords=collection_official_keywords, visible_sessions=current_sessions, cutoff_timestamp=cutoff_timestamp)
        original_count = len(all_sessions)
        no_new_sessions_count = 0
        " 个新会话，总计 "(f'{len(all_sessions)}', " 个")
        "向下滚动获取更多会话 (第"(f'{scroll_attempts + 1}', "次)")
        self.SessionList.WheelDown(wheelTimes=4, waitTime=0.3)
        time.sleep(random.uniform(0.5, 1.0))
        scroll_attempts = scroll_attempts + 1
        no_new_sessions_count = no_new_sessions_count + 1
        "本次滚动未获取到新会话 (连续"(f'{no_new_sessions_count}', "次)")
        logger.info("会话列表读取完成，下一步采集每个会话的聊天记录...")
        session = logger.info
        session_name = session.get("name", "")
        enhanced_session = {"name": session_name, "last_message": session.get("lastMessage", ""), "last_time": session.get("lastTime", "")}
        all_sessions.append(enhanced_session)
        logger.info("当前页面没有会话")
        logger.info("未获取到可见会话列表")
        collection_official_keywords.extend(saved_official_accounts)
        "已加载 "(f'{len(saved_official_accounts)}', " 个已保存的官方账号")
        from datetime import datetime, timedelta
        start_of_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_time = start_of_today - timedelta(days=time_limit_days - 1)
        cutoff_timestamp = cutoff_time.timestamp()
        " (时间戳: "(f'{cutoff_timestamp}', ")")
        time_limit_minutes = -1
    def _scroll_to_session_list_top(self):
        """滚动会话列表到顶部"""

        logger.info("开始滚动会话列表到顶部")
        max_attempts = 10
        logger.warning("未能滚动到会话列表顶部")
        return False
        attempt = range(max_attempts)
        self.SessionList.WheelUp(wheelTimes=3, waitTime=0.2)
        time.sleep(0.5)
        "已到达会话列表顶部 (尝试"(f'{attempt + 1}', "次)")
        return True
        logger.info("已在会话列表顶部，无需滚动")
        return True
    def _is_at_session_list_top(self):
        """检查是否已到达会话列表顶部"""

        visible_sessions = self.SessionList.GetChildren()
        first_session = visible_sessions[0]
        first_session_rect = first_session.BoundingRectangle
        session_list_rect = self.SessionList.BoundingRectangle
        top_diff = abs(first_session_rect.top - session_list_rect.top)
        tolerance = 5
        is_at_top = top_diff <= tolerance
        f'{session_list_rect.top}'(", 差值=", f'{top_diff}')
        return is_at_top
        f'{session_list_rect.top}'(", 差值=", f'{top_diff}')
        return is_at_top
        return True
    def SavePic(self, savepath, filename):
        WxUtils.SavePic()
    def SendFiles(self, who, filepath, not_exists):
        """
                    向当前聊天窗口发送文件 (商业级高可用版本)
                    not_exists: 如果未找到指定文件，继续或终止程序
                    filepath: 要复制文件的绝对路径
                    """

        self.EditMsg = self.UiaAPI.EditControl(Name=who)
        abs_filepath = str(Path(filepath).resolve())
        logger.info("准备发送文件: ", f'{abs_filepath}')
        def inject_file_to_clipboard(file_path):
            pass  # TODO: decompile function body
        max_retries = 3
        clipboard_ready = False
        self.EditMsg.SetFocus()
        time.sleep(0.1)
        self.EditMsg.SendKeys("{Ctrl}v", waitTime=1)
        time.sleep(0.2)
        self.EditMsg.SendKeys("{Enter}", waitTime=0.1)
        time.sleep(0.1)
        return 1
        raise Exception("重试多次后，剪贴板底层注入依然失败")
        attempt = range(max_retries)
        time.sleep(0.5)
        clipboard_ready = True
        time.sleep(0.3)
        raise BaseException("指定的文件不存在，请检查: ", f'{abs_filepath}')
        raise "未找到与 "(f'{who}', " 的聊天输入框")
        self.EditMsg = self._driver._get_edit_control(who)
        raise "无法打开与 "(f'{who}', " 的聊天窗口")
        filepath = WxUtils._download_network_file(filepath)
    def validate_file_paths(self, paths):
        """强化路径验证"""

        invalid = []
        valid_paths = []
        return valid_paths
        raise FileNotFoundError("无效路径: ", f'{invalid}')
        p = NULL
        abs_path = os.path.abspath(str(p))
        valid_paths.append(abs_path)
        invalid.append(abs_path)
        paths = [paths]
    def _close_favorite_window(self, fav_window):
        """安全关闭「发送收藏」选择窗口（ESC）。任何异常都吞掉，仅用于兜底清理。"""

        win = fav_window
        win = ui_Coder.WindowControl(ClassName="mmui::SendFavoriteWindow")
        win.SetFocus()
        win.SendKeys("{Esc}", waitTime=0.1)
        win = ui_Coder.WindowControl(ClassName="SendFavoriteWindow")
    def SendFavorite(self, who, keyword):
        """
                向指定会话发送一条微信「收藏」记录（按关键词模糊搜索，多条命中默认取第一条）。
                典型用途：发送提前收藏好的位置/定位卡片。仅适配微信 4.1.x（Qt / mmui 控件）。

                流程（控件信息来源：inspect 提取的发送收藏流程）：
                  1. 打开与 who 的聊天窗口
                  2. 点击输入框工具栏「发送收藏」按钮 → 弹出 mmui::SendFavoriteWindow
                  3. 在「搜索」框输入 keyword，等待结果刷新
                  4. 结果列表首项为提示项需跳过，取第二项；不足两项=没搜到，安全退出
                  5. 选中该项后，「发送」可用则点击发送

                Returns: {'success': bool, 'message': str}
                """

        fav_window = None
        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.2, 0.4))
        time.sleep(0.5)
        fav_button = self.UiaAPI.ButtonControl(Name="发送收藏")
        time.sleep(random.uniform(0.5, 1.0))
        fav_window = ui_Coder.WindowControl(ClassName="mmui::SendFavoriteWindow")
        search_box = fav_window.EditControl(Name="搜索")
        search_box.SetFocus()
        search_box.SendKeys("{Ctrl}a", waitTime=0.1)
        search_box.SendKeys("{Delete}", waitTime=0.1)
        search_box.SendKeys(str(keyword), interval=0.05)
        time.sleep(random.uniform(1.0, 1.6))
        result_list = fav_window.ListControl(AutomationId="fav_detail_list")
        items = result_list.GetChildren()
        self._close_favorite_window(fav_window)
        return {"success": f'{keyword}', "message": "\"的收藏"}
        target_item = items[1]
        time.sleep(random.uniform(0.4, 0.8))
        send_btn = fav_window.TextControl(Name="发送")
        time.sleep(random.uniform(0.5, 1.0))
        f'{who}'(", keyword=", f'{keyword}')
        return {"success": True, "message": "收藏发送成功"}
        self._close_favorite_window(fav_window)
        return {"success": False, "message": "点击发送按钮失败"}
        self._close_favorite_window(fav_window)
        return {"success": False, "message": "发送按钮不可用（未正确选中收藏项）"}
        self._close_favorite_window(fav_window)
        return {"success": False, "message": "未找到发送按钮"}
        send_btn = fav_window.ButtonControl(Name="发送")
        self._close_favorite_window(fav_window)
        return {"success": False, "message": "选择收藏项失败"}
        self._close_favorite_window(fav_window)
        return {"success": False, "message": "未找到收藏结果列表"}
        result_list = fav_window.ListControl()
        self._close_favorite_window(fav_window)
        return {"success": False, "message": "未找到收藏搜索框"}
        return {"success": False, "message": "未弹出收藏选择窗口"}
        fav_window = ui_Coder.WindowControl(ClassName="SendFavoriteWindow")
        return {"success": False, "message": "点击\"发送收藏\"按钮失败"}
        return {"success": False, "message": "未找到\"发送收藏\"按钮（请确认微信版本为4.1.x且输入框工具栏可见）"}
        return {"success": "未找到会话: ", "message": f'{who}'}
    def sync_group_members(self, group_name):
        """同步指定群聊的成员列表"""

        self.ChatWith(group_name)
        time.sleep(0.5)
        chat_window = self.GetWeChatWindow()
        info_button = chat_window.ButtonControl(Name="聊天信息")
        more_button = chat_window.ButtonControl(Name="查看更多")
        members_list = chat_window.ListControl(Name="聊天成员")
        rect = members_list.BoundingRectangle
        members = []
        processed_names = set()
        items = members_list.GetChildren()
        new_member_found = False
        ui_Coder.SendKeys("{ESC}")
        return members
        ui_Coder.WheelDown(waitTime=0.5)
        item = items
        name = item.Name
        info_pane = chat_window.PaneControl(Name="微信")
        member_info = {"nickname": name, "gender": "", "wx_id": "", "region": "", "is_friend": False}
        logger.info("开始获取信息面板的子控件...")
        add_friend_button = info_pane.ButtonControl(Name="添加到通讯录")
        member_info["is_friend"] = not add_friend_button.Exists(0.1)
        members.append(member_info)
        processed_names.add(name)
        new_member_found = True
        ui_Coder.SendKeys("{ESC}")
        time.sleep(0.2)
        control = ui_Coder.WalkControl(info_pane)[0]
        depth = ui_Coder.WalkControl(info_pane)[1]
        f'{control.ControlTypeName}'(", 深度: ", f'{depth}')
        text = control.Name
        logger.info("找到文本控件: ", f'{text}')
        next_control = control.GetNextSiblingControl()
        logger.info("昵称后的图片控件:")
        logger.info("- Name: ", f'{next_control.Name}')
        logger.info("- AutomationId: ", f'{next_control.AutomationId}')
        logger.info("- ClassName: ", f'{next_control.ClassName}')
        automation_id = str(next_control.AutomationId).lower()
        member_info["gender"] = "男"
        logger.info("设置性别: 男")
        member_info["gender"] = "女"
        logger.info("设置性别: 女")
        next_control = control.GetNextSiblingControl()
        member_info["region"] = next_control.Name
        logger.info("设置地区: ", f'{member_info["region"]}')
        next_control = control.GetNextSiblingControl()
        member_info["wx_id"] = next_control.Name
        logger.info("设置微信号: ", f'{member_info["wx_id"]}')
        raise "未找到成员 "(f'{name}', " 的信息面板")
        raise Exception("sync_group_members点击item失败")
        raise Exception("未找到群成员列表")
        raise Exception("sync_group_members点击【查看更多】失败")
        raise Exception("点击群成员头像失败")
        raise Exception("未找到群聊信息按钮")
        raise Exception("获取微信窗口失败")
    def GetWeChatWindow(self):
        """获取微信主窗口"""

        self.SwitchToThisWindow()
        time.sleep(0.5)
        return self.UiaAPI
    def invite_friends_to_group(self, friend_nicknames, group_name):
        """
                邀请好友进群
                Args:
                    friend_nicknames: 待入群的好友列表
                    group_name: 群聊名称
                Returns:
                    dict: {'success': bool, 'message': str, 'invited_count': int}
                """

        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.2, 0.4))
        time.sleep(0.5)
        chat_window = self.GetWeChatWindow()
        info_button = chat_window.ButtonControl(Name="聊天信息")
        time.sleep(0.5)
        detail_window = chat_window.PaneControl(ClassName="SessionChatRoomDetailWnd")
        members_list = detail_window.ListControl(Name="聊天成员")
        list_items = members_list.GetChildren()
        add_list_item = list_items[-1]
        return {"success": False, "message": "未找到添加列表项", "invited_count": 0}
        add_button = add_list_item.ButtonControl()
        time.sleep(0.5)
        add_member_window = chat_window.WindowControl(ClassName="AddMemberWnd")
        search_box = add_member_window.EditControl(Name="搜索")
        invited_count = 0
        finish_button = add_member_window.ButtonControl(Name="完成")
        start_time = time.time()
        invitation_success = False
        time.sleep(1)
        time.sleep(0.3)
        return {"success": f'{invited_count}', "message": " 位好友进群", "invited_count": invited_count}
        logger.warning("邀请流程异常：添加成员窗口未关闭且无确认弹窗")
        ui_Coder.SendKeys("{ESC}")
        time.sleep(0.3)
        raise Exception("邀请好友进群失败：添加成员窗口未正常关闭")
        confirm_window = ui_Coder.WindowControl(ClassName="ConfirmDialog", Name="微信")
        time.sleep(1)
        confirm_button = confirm_window.ButtonControl(Name="确定")
        logger.warning("未找到二次确认弹窗的确定按钮")
        time.sleep(1)
        logger.info("确认后添加成员窗口已关闭，邀请成功")
        invitation_success = True
        logger.info("二次确认弹窗->点击确认按钮")
        logger.warning("点击确认弹窗的确定按钮失败")
        logger.info("邀请成功！")
        invitation_success = True
        raise Exception("点击完成按钮失败")
        raise Exception("完成按钮不可点击")
        raise Exception("未找到完成按钮")
        nickname = "成功邀请 "
        search_box.SetFocus()
        search_box.SendKeys("{Ctrl}a")
        search_box.SendKeys("{Delete}")
        time.sleep(random.uniform(0.3, 0.8))
        search_box.SendKeys(nickname, interval=0.2)
        time.sleep(random.uniform(0.5, 1.3))
        result_list = add_member_window.ListControl()
        result_items = result_list.GetChildren()
        first_result = result_items[0]
        invited_count = invited_count + 1
        logger.info("已选择好友: ", f'{nickname}')
        time.sleep(random.uniform(0.5, 1))
        "点击好友 "(f'{nickname}', " 的搜索结果失败")
        "未找到好友 "(f'{nickname}', " 的搜索结果")
        "未找到好友 "(f'{nickname}', " 的搜索结果列表")
        raise Exception("未找到搜索框")
        return {"success": False, "message": "未找到添加成员窗口", "invited_count": 0}
        return {"success": False, "message": "点击添加按钮失败", "invited_count": 0}
        return {"success": False, "message": "未找到添加按钮", "invited_count": 0}
        return {"success": False, "message": "聊天成员列表为空", "invited_count": 0}
        return {"success": False, "message": "聊天成员列表为空", "invited_count": 0}
        return {"success": False, "message": "未找到群聊详情面板", "invited_count": 0}
        return {"success": False, "message": "点击群聊信息按钮失败", "invited_count": 0}
        return {"success": False, "message": "未找到群聊信息按钮", "invited_count": 0}
        return {"success": False, "message": "获取微信窗口失败", "invited_count": 0}
        return {"success": "未找到群聊: ", "message": f'{group_name}', "invited_count": 0}
        return self._driver.invite_friends_to_group(friend_nicknames=friend_nicknames, group_name=group_name)
    def _generate_ai_comment(self, wx_id, content, settings, publisher):
        """
                根据朋友圈内容生成AI评论
                """

        agent_id = settings.get("agentId")
        print("agent_id: ", f'{agent_id}')
        config_manager = ConfigManager()
        agent_info = config_manager.get_agent_by_id(agent_id)
        platform = agent_info.get("platform", "coze").lower()
        account_wxid = ""
        logger.info("不支持的平台类型: ", f'{platform}')
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
    def is_shift_pressed(self):
        """检查 Shift 键是否被按下"""

        return win32api.GetAsyncKeyState(win32con.VK_SHIFT) < 0
    def _close_moment_window(self):
        """关闭朋友圈窗口并返回会话列表"""

        moment_window = ui_Coder.WindowControl(searchDepth=1, Name="朋友圈", ClassName="SnsWnd")
        chat_list_btn = self.UiaAPI.ButtonControl(Name="聊天")
        logger.info("已关闭朋友圈窗口并返回会话界面")
        time.sleep(0.5)
        raise Exception("_close_moment_window点击聊天按钮")
        ui_Coder.SendKeys("{ESC}")
        time.sleep(1)
    def auto_publish_moment(self, text, media_dir):
        return {"success": False, "error": "微信3.9不支持发朋友圈，请安装微信4.1"}
        return self._driver.auto_publish_moment(text=text, media_dir=media_dir)
    def auto_moment_comment(self, settings, callback, collect_wx_id, cancel_checker):
        time.sleep(1)
        self.SwitchToThisWindow()
        user_comment_counts = {}
        comment_count = 0
        processed_moments = set()
        blacklist = settings.get("blacklist", [])
        per_friend_limit = settings.get("perFriendLimit", 2)
        interaction_mode = settings.get("interactionMode", "like_and_comment")
        reachLastPosition = settings.get("reachLastPosition") == "stop"
        should_like = interaction_mode in ("like_only", "like_and_comment")
        should_comment = interaction_mode in ("comment_only", "like_and_comment")
        moment_btn = self.UiaAPI.ButtonControl(Name="朋友圈")
        time.sleep(2)
        moment_window = ui_Coder.WindowControl(searchDepth=1, Name="朋友圈", ClassName="SnsWnd")
        moment_window.SetFocus()
        moment_list = moment_window.ListControl(Name="朋友圈")
        def is_shift_pressed():
            return win32api.GetAsyncKeyState(win32con.VK_SHIFT) < 0
            return True
        moment_window_hwnd = win32gui.FindWindow("SnsWnd", "朋友圈")
        moment_list.WheelDown(wheelTimes=4)
        items = moment_list.GetChildren()
        print("当前可见区域的朋友圈条数：", f'{len(items)}')
        moment_list.WheelDown(wheelTimes=3)
        time.sleep(1)
        item = items
        content = self._get_moment_content(item)[0]
        publisher = self._get_moment_content(item)[1]
        publish_time = self._get_moment_content(item)[2]
        allowed_friends = settings.get("allowedFriends")
        account_id = ""
        moment_id = f'{20}'
        processed_moments.add(moment_id)
        moment_list_rect = moment_list.BoundingRectangle
        comment_btn = item.ButtonControl(Name="评论")
        logger.info("评论按钮不可见，尝试滚动显示")
        moment_list.WheelDown(wheelTimes=4)
        time.sleep(0.5)
        retry = range(3)
        comment_btn = item.ButtonControl(Name="评论")
        moment_list.WheelDown(wheelTimes=3)
        time.sleep(0.3)
        logger.info("find success:找到该条朋友圈评论按钮")
        publish_timestamp = self._parse_publish_time(publish_time)
        logger.info("准备评论好友的朋友圈: ", f'{moment_id}')
        comment = ""
        skip_comment_action = False
        interaction_data = {"type": [], "publisher": publisher, "content": content, "publish_time": publish_time, "comment_content": comment, "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
        user_comment_counts[publisher] = user_comment_counts[publisher] + 1
        WxUtils._save_moment_interaction(interaction_data)
        comment_count = comment_count + 1
        time.sleep(random.randint(3, 8))
        self._close_moment_window()
        callback({"type": "info", "message": "已达到评论限制次数,任务结束"})
        callback("comment", {"type": "已评论: ", "message": f'{comment}'})
        user_comment_counts[publisher] = 1
        interaction_data["type"].append("comment")
        interaction_data["type"].append("like")
        logger.info("自动评论已开启，尝试评论...")
        wx_id = None
        yield None
        yield None
        logger.info("检测到Shift键按下，终止任务")
        self._close_moment_window()
        logger.info("自动点赞已开启，尝试点赞...")
        comment_area = item.ButtonControl(Name="评论")
        time.sleep(1)
        toast_window = moment_window.PaneControl(ClassName="SnsLikeToastWnd")
        like_btn = toast_window.ButtonControl(Name="赞")
        logger.info("未找到点赞按钮或已经点赞过")
        logger.info("找到点赞按钮，执行点赞")
        time.sleep(random.uniform(0.8, 1.2))
        raise Exception("点击【点赞】按钮失败")
        logger.info("检测到Shift键按下，终止任务")
        self._close_moment_window()
        self._collect_moment_publisher_wx_id(item, publisher, moment_window)
        logger.info("未找到点赞评论弹窗")
        logger.info("检测到Shift键按下，终止任务")
        self._close_moment_window()
        raise Exception("点击【评论】按钮失败")
        logger.info("未找到评论区域按钮，跳过点赞")
        logger.info("检测到Shift键按下，终止任务")
        self._close_moment_window()
        self._generate_ai_comment(wx_id, content, settings, publisher)
        logger.info("评论模式下朋友圈内容过短，跳过评论")
        logger.info("发现 2天前 的朋友圈，停止任务")
        self._close_moment_window()
        logger.info("发现已互动过的朋友圈,根据设置，继续执行")
        logger.info("发现已互动过的朋友圈,根据设置，终止任务")
        self._close_moment_window()
        callback({"type": "info", "message": "发现已互动过的朋友圈，终止任务"})
        logger.info("跳过自己发送的朋友圈")
        logger.info("检测到Shift键按下，终止任务")
        self._close_moment_window()
        logger.info("已处理过的朋友圈: ", f'{moment_id}')
        " 已达到评论次数限制 "(f'{per_friend_limit}', "，跳过处理")
        "发布者 "(f'{publisher}', " 在黑名单中，跳过处理")
        "发布者 "(f'{publisher}', " 不在选中的标签范围内，跳过处理")
        print("跳过广告....")
        logger.info("检测到停止信号，终止任务")
        self._close_moment_window()
        callback({"type": "info", "message": "用户按下Shift键或收到前端停止信号，任务终止"})
        logger.info("未找到朋友圈项目")
        foreground_hwnd = win32gui.GetForegroundWindow()
        logger.info("朋友圈窗口被遮挡，尝试前置窗口...")
        win32gui.SetForegroundWindow(moment_window_hwnd)
        moment_window.SetFocus()
        time.sleep(0.5)
        raise Exception("未找到朋友圈列表")
        raise Exception("未找到朋友圈窗口")
        raise Exception("点击【朋友圈】按钮")
        raise Exception("未找到朋友圈按钮")
        yield None
    def _collect_moment_publisher_wx_id(self, moment_item, publisher_name, moment_window):
        """采集朋友圈发布者的微信号

                Args:
                    moment_item: 朋友圈项目控件
                    publisher_name: 发布者姓名
                    moment_window: 朋友圈窗口控件

                Returns:
                    str: 微信号，获取失败返回空字符串
                """

        info_pane = None
        "开始采集朋友圈发布者 "(f'{publisher_name}', " 的微信号")
        avatar_button = moment_item.ButtonControl(foundIndex=1)
        time.sleep(random.uniform(0.8, 1.2))
        info_pane = moment_window.PaneControl(Name="微信")
        wx_id = ""
        time.sleep(0.5)
        return wx_id
        moment_window.SetFocus()
        ui_Coder.SendKeys("{ESC}")
        control = ui_Coder.WalkControl(info_pane)[0]
        depth = ui_Coder.WalkControl(info_pane)[1]
        text = control.Name
        next_control = control.GetNextSiblingControl()
        wx_id = next_control.Name
        logger.info("找到微信号: ", f'{wx_id}')
        "未找到个人信息面板，跳过获取 "(f'{publisher_name}', " 的微信号")
        return ""
        "未找到当前窗口，跳过获取 "(f'{publisher_name}', " 的微信号")
        return ""
        "点击发布者 "(f'{publisher_name}', " 的头像失败")
        return ""
        "未找到发布者 "(f'{publisher_name}', " 的头像按钮")
        return ""
    def _is_control_fully_visible(self, control, container_rect):
        """检查控件是否在容器中完全可见"""

        control_rect = control.BoundingRectangle
        return control_rect.bottom <= container_rect.bottom
    def back_to_chat_list(self):
        """返回会话列表"""

        chat_list_btn = self.UiaAPI.ButtonControl(Name="聊天")
        print("切换到会话列表...")
        time.sleep(0.5)
        raise Exception("back_to_chat_list点击【聊天】按钮失败")
    def _get_last_comment_position(self):
        """获取上次评论位置"""

        f = open("last_comment_position.json", "r")
        json.load(f)(None, None, None)
        return "???"
    def _save_comment_position(self, publisher, publish_time):
        """保存当前评论位置"""

        position = {"publisher": publisher, "time": publish_time}
        f = open("last_comment_position.json", "w")
        json.dump(position, f)
        None(None, None)
    def _is_reached_last_position(self, current_publisher, current_time, last_position):
        """检查是否到达上次评论位置"""

        return current_publisher == last_position["publisher"]
        return False
    def _get_moment_content(self, moment):
        """获取朋友圈内容"""

        moment_text = moment.Name
        parts = moment_text.split(":", 1)
        publisher = parts[0].strip()
        remaining_text = parts[1].strip()
        lines = remaining_text.split("\n")
        line = []
        time_patterns = ("^\\d+分钟前$", "^\\d+小时前$", "^\\d+天前$", "^刚刚$", "^昨天$", "^昨天\\s*\\d{1,2}:\\d{1,2}$", "^前天\\s*\\d{1,2}:\\d{1,2}$", "^\\d{1,2}月\\d{1,2}日\\s*\\d{1,2}:\\d{1,2}$", "^\\d{4}年\\d{1,2}月\\d{1,2}日\\s*\\d{1,2}:\\d{1,2}$")
        system_patterns = ("^包含\\d+张图片$", "^视频号$", "^视频号直播,直播中$", "^\\s*视频\\s*$", "^分享图片$", "^分享视频$", "^分享链接$", "^视频号\\s*·\\s*.*$", ".*\\s*·\\s*视频号$", "^.*市\\s*·\\s*.*$", "^.*省\\s*·\\s*.*$", "^.*区\\s*·\\s*.*$")
        content_lines = []
        publish_time = ""
        found_time = False
        content = "\n".join(content_lines).strip()
        print("##########################################")
        print("- 发布者: ", f'{publisher}')
        print("- 内容: ", f'{content}')
        print("- 时间: ", f'{publish_time}')
        return (content, publisher, publish_time)
        line = NULL
        content_lines.insert(0, line)
        publish_time = line
        found_time = True
        logger.info("朋友圈文本格式不正确：内容为空")
        return (publisher, "", "")
        line = NULL
        logger.info("朋友圈文本格式不正确：未找到冒号分隔符")
        return ("", "", "")
        logger.info("未找到朋友圈文本内容")
        return ("", "", "")
    def _parse_publish_time(self, time_str):
        """解析发布时间"""

        from datetime import datetime, timedelta
        current_time = datetime.now()
        current_year = current_time.year
        time_str = f'{time_str}'
        date_format = "%Y年%m月%d日 %H:%M"
        publish_time = datetime.strptime(time_str, date_format)
        return publish_time.timestamp()
        publish_time = publish_time.replace(year=current_year - 1)
        date_format = "%Y年%m月%d日 %H:%M"
        return (current_time - timedelta(days=1)).timestamp()
        days = int(time_str.replace("天前", ""))
        return current_time.timestamp() - days * 86400
        hours = int(time_str.replace("小时前", ""))
        return current_time.timestamp() - hours * 3600
        minutes = int(time_str.replace("分钟前", ""))
        return current_time.timestamp() - minutes * 60
        return current_time.timestamp()
        return current_time.timestamp()
    def process_friend_requests(self, max_process, tag):
        """
                一次性处理好友申请
                max_process: 本次最多处理的好友数量
                tag: 要设置的标签
                """

        logger.info("开始处理好友申请任务...")
        time.sleep(2)
        processed_count = 0
        scroll_count = 0
        MAX_SCROLL_TIMES = 4
        processed_users = []
        self.SwitchToThisWindow()
        time.sleep(random.uniform(0.3, 0.7))
        time.sleep(0.5)
        new_friend_item = self.UiaAPI.ListItemControl(Name="新的朋友")
        time.sleep(1)
        new_friends_list = self.UiaAPI.ListControl(Name="新的朋友")
        force_break = False
        logger.info("处理完成，准备返回会话列表...")
        chat_list_btn = self.UiaAPI.ButtonControl(Name="聊天")
        logger.info("已返回会话列表")
        return {"success": f'{processed_count}', "message": " 个好友申请", "processed_count": processed_count, "processed_users": processed_users}
        time.sleep(random.uniform(0.3, 0.8))
        raise Exception("【通过好友申请】点击聊天按钮失败")
        "将列表滚动回顶部（滚动 "(f'{scroll_count}', " 次）...")
        _ = range(scroll_count)
        new_friends_list.WheelUp(wheelTimes=3)
        time.sleep(random.uniform(0.3, 0.8))
        children = new_friends_list.GetChildren()
        found_pending = False
        last_item = new_friends_list.GetChildren()[-1]
        pre_last_item_bottom = last_item.BoundingRectangle.bottom
        new_friends_list.WheelDown(wheelTimes=3)
        time.sleep(random.uniform(0.3, 0.8))
        last_item = new_friends_list.GetChildren()[-1]
        post_last_item_bottom = last_item.BoundingRectangle.bottom
        scroll_distance = abs(post_last_item_bottom - pre_last_item_bottom)
        scroll_count = scroll_count + 1
        logger.info("检测到列表已到达底部，停止滚动")
        float("inf")
        friend = float("inf")
        friend_rect = friend.BoundingRectangle
        list_rect = new_friends_list.BoundingRectangle
        offset = 10
        accept_btn = friend.ButtonControl(Name="接受")
        found_pending = True
        nickname = friend.Name
        logger.info("找到待处理好友：", f'{nickname}')
        time.sleep(0.5)
        verify_window = None
        verify_window = self.UiaAPI.WindowControl(Name="通过朋友验证", ClassName="WeUIDialog")
        logger.warning("未找到通过朋友认证弹窗，跳过处理")
        logger.info("成功打开通过朋友认证弹窗")
        confirm_btn = verify_window.ButtonControl(Name="确定")
        logger.info("未找到确定按钮，跳过处理")
        logger.info("【确定】按钮不可点击")
        checkboxes = WxUtils.find_controls_by_type(verify_window, "CheckBoxControl", max_depth=10)
        friend_circle_checkbox = None
        logger.warning("未找到朋友圈复选框...,跳过处理该好友申请")
        logger.info("找到朋友圈复选框，正在点击")
        time.sleep(random.uniform(0.2, 0.5))
        time.sleep(random.uniform(0.2, 0.5))
        time.sleep(2)
        wait_start = time.time()
        processed_count = processed_count + 1
        processed_users.append(nickname)
        "，当前已处理 "(f'{processed_count}', " 个好友申请")
        logger.warning("无法获取账号信息，跳过保存好友到数据库")
        tag_str = ""
        wxid = self._generate_stable_wxid(nickname)
        friend_info = {"nickname": nickname, "wechat_id": wxid, "remark_name": "", "tags": tag_str}
        result = self.db_manager.save_or_update_friend_info(self.account_info["account_id"], friend_info, is_new=True)
        "新好友 "(f'{nickname}', " 添加到数据库失败！")
        "新好友 "(f'{nickname}', " 添加到数据库成功！")
        tag_str = tag
        logger.info("处理好友请求超时，可能是网络问题")
        timeout_dialog = self.UiaAPI.PaneControl(ClassName="WeUIDialog")
        accept_btn = friend.ButtonControl(Name="接受")
        time.sleep(0.5)
        know_btn = timeout_dialog.ButtonControl(Name="我知道了")
        logger.info("好友请求已过期，关闭提示弹窗")
        force_break = True
        raise Exception("点击通过好友->我知道了按钮失败")
        raise Exception("点击确认按钮失败")
        logger.warning("点击朋友圈复选框失败，但继续尝试点击确定按钮")
        checkbox = NULL
        friend_circle_checkbox = checkbox
        logger.info("【确定】按钮可点击")
        f'{nickname}'(" 设置标签: ", f'{tag}')
        logger.info("设置标签失败，但继续处理")
        return {"success": f'{processed_count}', "message": " 个好友申请", "processed_count": processed_count}
        depth = range(1, 5)
        verify_window = self.UiaAPI.WindowControl(searchDepth=depth, ClassName="WeUIDialog")
        "在搜索深度 "(f'{depth}', " 找到通过朋友认证弹窗")
        raise Exception("点击接受按钮失败")
        float("inf")
        return {"success": False, "message": "未找到新朋友列表", "processed_count": 0}
        raise Exception("点击新的朋友按钮失败")
        logger.info("未找到新的朋友入口，尝试向上滚动列表...")
        contact_list = self.UiaAPI.ListControl(Name="联系人")
        return {"success": False, "message": "滚动列表后仍未找到新的朋友入口", "processed_count": 0}
        i = range(3)
        contact_list.WheelUp(wheelTimes=3)
        time.sleep(random.uniform(0.3, 0.7))
        "在第"(f'{i + 1}', "次滚动后找到新的朋友入口")
        return {"success": False, "message": "未找到通讯录列表", "processed_count": 0}
        raise Exception("点击通讯录按钮失败")
        result = self._driver.process_friend_requests(max_process=max_process, tag=tag)
        return result
        return result
        tag_str = tag
        nickname = result["processed_users"]
        wxid = self._generate_stable_wxid(nickname)
        friend_info = {"nickname": nickname, "wechat_id": wxid, "remark_name": "", "tags": tag_str}
        self.db_manager.save_or_update_friend_info(self.account_info["account_id"], friend_info, is_new=True)
    def _set_friend_tag(self, nickname, tag, verify_window):
        """
                在通过好友申请时设置标签
                """

        tag_edit = None
        label_text = verify_window.TextControl(Name="标签")
        printf("标签文本未找到...")
        time.sleep(random.uniform(0.2, 0.4))
        time.sleep(1)
        tag_edit.SetFocus()
        time.sleep(0.5)
        tag_edit.SendKeys("{Ctrl}a")
        time.sleep(random.uniform(0.3, 0.7))
        tag_edit.SendKeys("{Delete}")
        time.sleep(random.uniform(0.3, 0.7))
        original_text = tag + "\n"
        WxUtils.SetClipboard(original_text)
        time.sleep(random.uniform(0.8, 1.5))
        clipboard_text = WxUtils.GetClipboard()
        tag_edit.SendKeys("{Ctrl}v")
        time.sleep(random.uniform(0.3, 0.7))
        current_value = tag_edit.GetValuePattern().Value
        ui_Coder.SendKeys("{Enter}")
        time.sleep(1)
        current_value = tag_edit.GetValuePattern().Value
        f'{nickname}'(" 设置标签: ", f'{tag}')
        return True
        logger.info("标签内容未成功输入，添加好友失败...")
        return False
        logger.info("剪贴板内容验证失败，重试...")
        WxUtils.SetClipboard(original_text)
        time.sleep(random.uniform(0.8, 1.5))
        raise Exception("【设置好友标签】点击标签编辑框失败")
        logger.info("标签输入框不可用")
        return False
        logger.info("未找到标签输入框")
        return False
        all_edits = verify_window.GetChildren(maxDepth=10)
        edit = all_edits
        tag_edit = edit
        logger.info("通过遍历查找到标签输入框")
        label_parent = label_text.GetParentControl()
        siblings = label_parent.GetChildren()
        i = enumerate(siblings)[0]
        sibling = enumerate(siblings)[1]
        next_pane = siblings[i + 1]
        child_pane = next_pane.PaneControl()
        tag_edit = child_pane.EditControl()
        logger.info("通过标签文本定位找到输入框")
        logger.info("未传入验证弹窗控件")
        return False
    def add_new_friend(self, wxid, remark, tags, verify_message):
        """
                自动添加新好友

                Args:
                    wxid: 待添加用户的微信号/手机号
                    remark: 好友备注
                    tags: 好友标签

                Returns:
                    dict: {'success': bool, 'message': str, 'nickname': str}
                """

        time.sleep(random.uniform(2, 3))
        win32gui.SetForegroundWindow(self.window_handle)
        time.sleep(random.uniform(0.2, 0.4))
        time.sleep(random.uniform(0.5, 1.0))
        add_friend_btn = self.UiaAPI.ButtonControl(Name="添加朋友")
        time.sleep(random.uniform(0.5, 1.0))
        search_edit = self.UiaAPI.EditControl(Name="微信号/手机号")
        time.sleep(0.5)
        WxUtils.SetClipboard(wxid)
        search_edit.SendKeys("{Ctrl}v")
        time.sleep(random.uniform(1.0, 1.5))
        search_items = self.UiaAPI.ListControl().GetChildren()
        user_not_found = False
        search_result = self.UiaAPI.ListItemControl("搜索：", Name=f'{wxid}')
        time.sleep(random.uniform(0.5, 1.0))
        user_profile = None
        logger.info("未找到个人信息弹窗窗口...")
        self._click_cancel_in_contacts()
        return {"success": False, "message": "未找到用户信息窗口", "status": "unknown"}
        avatar_btn = user_profile.ButtonControl()
        nickname = ""
        add_button = user_profile.ButtonControl(Name="添加到通讯录")
        time.sleep(random.uniform(0.5, 1.0))
        apply_window = ui_Coder.WindowControl(searchDepth=2, Name="添加朋友请求", ClassName="WeUIDialog")
        time.sleep(random.uniform(0.5, 1.0))
        send_button = apply_window.ButtonControl(Name="确定")
        logger.info("找到发送按钮, 点击发送...")
        logger.info("【确定】按钮不可点击")
        checkboxes = WxUtils.find_controls_by_type(apply_window, "CheckBoxControl", max_depth=10)
        friend_circle_checkbox = None
        print("复选框数量: ", f'{len(checkboxes)}')
        logger.warning("未找到朋友圈复选框...,跳过处理该好友申请")
        self._click_cancel_in_contacts()
        return {"success": False, "message": "未找到朋友圈设置复选框"}
        logger.info("找到朋友圈复选框，正在点击")
        time.sleep(random.uniform(0.2, 0.5))
        time.sleep(random.uniform(2.0, 3))
        self._click_cancel_in_contacts()
        return {"success": True, "message": "添加好友成功", "nickname": nickname}
        raise Exception("【添加好友】点击发送好友申请按钮失败")
        logger.warning("点击朋友圈复选框失败，但继续尝试点击确定按钮")
        checkbox = checkboxes
        friend_circle_checkbox = checkbox
        logger.info("【确定】按钮可点击")
        logger.info("未找到确定按钮")
        ui_Coder.SendKeys("{ESC}")
        time.sleep(random.uniform(0.5, 1.0))
        self._click_cancel_in_contacts()
        return {"success": False, "message": "未找到发送按钮"}
        logger.info("设置标签失败，但继续处理")
        logger.info("设置备注名失败，但继续处理")
        logger.info("设置验证消息失败，但继续处理")
        logger.info("未找到申请添加好友弹窗")
        self._click_cancel_in_contacts()
        return {"success": False, "message": "未找到添加好友申请窗口"}
        logger.info("未找到申请添加朋友弹窗，可能是之前的好友重新添加成功")
        self._click_cancel_in_contacts()
        return {"success": True, "message": "添加好友成功（之前的好友）", "nickname": nickname}
        raise Exception("【添加好友】点击添加到通讯录按钮失败")
        time.sleep(random.uniform(0.3, 0.8))
        ui_Coder.SendKeys("{ESC}")
        time.sleep(random.uniform(0.5, 1.0))
        self._click_cancel_in_contacts()
        return {"success": False, "message": "该用户已经是好友", "nickname": nickname, "status": "already"}
        nickname = avatar_btn.Name
        i = range(2)
        user_profile = ui_Coder.PaneControl(ClassName="ContactProfileWnd")
        "未找到个人信息弹窗窗口，尝试第 "(f'{i + 1}', " 次...")
        time.sleep(1)
        raise Exception("【添加好友】点击搜索结果item失败")
        "未找到搜索："(f'{wxid}', "列表项")
        self._click_cancel_in_contacts()
        return {"success": False, "message": "未找到搜索结果", "status": "unknown"}
        logger.info("用户不存在: ", f'{wxid}')
        self._click_cancel_in_contacts()
        return {"success": False, "message": "用户不存在", "status": "unknown"}
        item = NULL
        user_not_found = True
        logger.info("未找到任何搜索结果: ", f'{wxid}')
        self._click_cancel_in_contacts()
        return {"success": False, "message": "未找到搜索结果", "status": "unknown"}
        raise Exception("【添加好友】点击搜索框失败")
        search_edit = self.UiaAPI.EditControl(Name="WeChat ID/手机号")
        logger.info("未找到搜索输入框（已尝试'微信号/手机号'和'WeChat ID/手机号'）")
        self._click_cancel_in_contacts()
        return {"success": False, "message": "未找到搜索输入框"}
        raise Exception("【添加好友】点击添加按钮失败")
        self._click_cancel_in_contacts()
        add_friend_btn = self.UiaAPI.ButtonControl(Name="添加朋友")
        logger.info("未找到添加朋友按钮")
        return {"success": False, "message": "未找到添加朋友按钮"}
        raise Exception("【添加好友】点击通讯录按钮失败")
        self.window_handle = self._wait_for_wechat_window()
        result = self._driver.add_new_friend(wxid=wxid, remark=remark, tags=tags, verify_message=verify_message)
        return result
    def _click_cancel_in_contacts(self):
        """点击通讯录顶部的取消按钮"""

        cancel_btn = self.UiaAPI.ButtonControl(Name="取消")
        return False
        time.sleep(random.uniform(0.5, 1.0))
        return True
        raise Exception("【添加好友】点击取消按钮失败")
    def _set_friend_remark(self, nickname, remark, verify_window):
        """设置好友备注名"""

        return self._set_input_text(verify_window, remark, "备注名")
    def _set_verify_message(self, message, verify_window):
        """设置验证消息"""

        return self._set_input_text(verify_window, message, "发送添加朋友申请")
    def _set_input_text(self, window, text, control_name):
        pass  # TODO: decompile function body
    __classcell__ = __class__
    return __class__
