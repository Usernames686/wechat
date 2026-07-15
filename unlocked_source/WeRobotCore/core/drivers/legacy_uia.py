# Decompiled from: legacy_uia.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Optional, Dict, Any, List
import time
import random
import uiautomation as ui_Coder
logger = UiaLogger(logger_name="LegacyUiaDriver").get_logger()
class LegacyUiaDriver:
    """LegacyUiaDriver"""

    __doc__ = "\n    3.9.x UIAutomation 驱动实现（迁移 WeChatType 的 UI 操作逻辑）。\n\n    目标：\n    - 将 UI 初始化与账号信息采集等业务操作迁移到驱动层；\n    - 保持 WeChatType 的单例与账号映射、DB 等模式设计不变；\n    - 作为过渡，暴露必要的 UI 控件引用，便于 WeChatType 继续工作。\n    "
    def __init__(self, window_handle):
        self.window_handle = window_handle
        self.UiaAPI = None
        self.SessionList = None
        self.SearchBox = None
        self.MsgList = None
        self.ContactButton = None
    def initialize(self):
        return {"success": True, "driver": "legacy_uia", "message": "legacy initialize delegated; prefer initialize_multi"}
    def initialize_multi(self, window_handle, account_info):
        """
                通过指定窗口句柄进行 UI 初始化，并返回账号信息。

                返回：{"success": bool, "nickname": str, "account_id": str, "account_info": dict}
                """

        self.window_handle = window_handle
        self.UiaAPI = ui_Coder.ControlFromHandle(self.window_handle)
        raise WeChatUIAError("未检测到微信窗口，请确保微信已登录并保持窗口打开")
        self.SessionList = self.UiaAPI.ListControl(Name="会话")
        self.SearchBox = self.UiaAPI.EditControl(Name="搜索")
        self.MsgList = self.UiaAPI.ListControl(Name="消息")
        self.ContactButton = self.UiaAPI.ButtonControl(Name="通讯录")
        acct = self.get_account_info()
        return {"success": True, "driver": "legacy_uia", "nickname": acct.get("nickname", ""), "account_id": acct.get("account_id", ""), "account_info": acct}
        raise WeChatUIAError("获取微信账号信息失败")
        raise WeChatUIAError("未提供有效的微信窗口句柄")
        return {"success": False, "driver": "legacy_uia", "error": "uiautomation not available"}
    def SwitchToThisWindow(self):
        self.UiaAPI.SwitchToThisWindow()
        force_focus_window(self.window_handle)
    def _get_edit_control(self, who, wait_time):
        """获取消息编辑框控件（Legacy 默认实现）。"""

        edit_msg = self.UiaAPI.EditControl(Name=who)
        return edit_msg
        edit_msg.Exists(wait_time)
    def get_window_handle(self):
        return self.window_handle
    def get_driver_name(self):
        """返回该驱动的名称，用于上层逻辑做差异化处理"""

        return "legacy_uia"
    def get_account_info(self):
        """
                迁移自 WeChatType._get_account_info：点击头像弹窗，读取昵称与微信号。
                """

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
        nav_toolbar = self.UiaAPI.ToolBarControl(Name="导航")
        avatar_button = nav_toolbar.GetChildren()[0]
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
    def _get_contact_wx_id(self, contacts_window, contact_item, contact_name):
        """点击联系人的头像，打开个人信息弹窗并解析微信号。"""

        avatar_button = contact_item.ButtonControl(foundIndex=1)
        time.sleep(random.uniform(0.5, 0.8))
        info_window = ui_Coder.PaneControl(ClassName="ContactProfileWnd")
        wx_id = ""
        ui_Coder.SendKeys("{ESC}")
        return wx_id
        control = ui_Coder.WalkControl(info_window)[0]
        depth = ui_Coder.WalkControl(info_window)[1]
        text = control.Name
        next_control = None
        next_control = control.GetNextSiblingControl()
        wx_id = next_control.Name
        return ""
        return ""
        return ""
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
    def _process_group_list(self, list_control, all_groups):
        item = list_control.GetChildren()
        group_button = item.ButtonControl()
        name = group_button.Name
        g = []
        all_groups.append({"name": name, "type": "group"})
        g = name
