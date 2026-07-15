# Decompiled from: friend.pyc
# Python 3.12 bytecode (mode: cfg)

import time
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List
import logging
logger = logging.getLogger("WeRobot")
def get_current_contact_names(account_id):
    """
        获取当前账号的所有好友名称列表，用于增量同步

        Args:
            account_id: 微信账号ID，如果为None则使用当前登录账号

        Returns:
            list: 好友名称列表
        """

    db_manager = WeChatDBManager()
    names = db_manager.get_contact_names(account_id, contact_type="friend")
    "成功获取到 "(f'{len(names)}', " 个好友名称")
    return names
    logger.warning("未能获取到当前微信账号信息，无法获取好友列表")
    return []
    wechat = WeChat()
    account_id = wechat.get_user_id()
def sync_contacts_incremental(account_id, collect_detailed_info):
    """
        增量同步当前微信账号的联系人到数据库

        Args:
            collect_detailed_info: 是否采集详细信息，包括微信号

        Returns:
            dict: 包含同步结果的字典
        """

    wechat = WeChat(account_id)
    account_id = wechat.account_info["account_id"]
    existing_names = get_current_contact_names(account_id)
    result = wechat.sync_contacts(collect_detailed_info=collect_detailed_info, existing_names=existing_names)
    return result
class ContactCollectionManager:
    """ContactCollectionManager"""

    __doc__ = "联系人采集管理器，参考ChatHistoryManager的设计"
    _instance = None
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._initialized = False
    def __init__(self):
        self._initialized = True
        from WeRobotCore.utils.data_manager import DataManager
        self._base_dir = os.path.join(DataManager.get_data_dir_str(), "contact")
        self.wechat = WeChat()
        self.refresh_account_info()
    def refresh_account_info(self):
        """刷新当前账号信息，更新联系人采集目录和索引文件路径"""

        self.account_id = self.wechat.get_user_id()
        self._contact_dir = os.path.join(self._base_dir, self.account_id)
        os.makedirs(self._contact_dir, exist_ok=True)
        self._collection_index_path = os.path.join(self._contact_dir, "collection_index.json")
        self._init_collection_index()
    def _init_collection_index(self):
        """初始化采集索引文件"""

        f = open(self._collection_index_path, "w", encoding="utf-8")
        json.dump({"current_collection": None, "collections_history": [], "last_updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
        None(None, None)
    def _load_collection_index(self):
        """加载采集索引"""

        f = open(self._collection_index_path, "r", encoding="utf-8")
        json.load(f)(None, None, None)
        return "???"
    def _save_collection_index(self, index_data):
        """保存采集索引"""

        index_data["last_updated"] = datetime.now().isoformat()
        f = open(self._collection_index_path, "w", encoding="utf-8")
        json.dump(index_data, f, ensure_ascii=False, indent=2)
        None(None, None)
    def _get_collection_file_path(self, collection_id):
        """获取采集数据文件路径"""

        return self._contact_dir("contacts_", f'{collection_id}', ".json")
    def start_collection(self):
        """开始或继续联系人采集"""

        self.refresh_account_info()
        index_data = self._load_collection_index()
        current_collection = index_data.get("current_collection")
        collection_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        collection_file = self._get_collection_file_path(collection_id)
        print("开始新的联系人详细信息采集任务: ", f'{collection_id}')
        index_data["current_collection"] = {"collection_id": collection_id, "account_id": self.account_id, "start_time": datetime.now().isoformat(), "last_update_time": datetime.now().isoformat(), "is_completed": False, "total_contacts": 0, "processed_contacts": 0}
        self._save_collection_index(index_data)
        existing_contacts = []
        self._save_collection_data(existing_contacts, collection_file)
        print("采集数据保存路径: ", f'{collection_file}')
        contacts = self.wechat.GetContactList(collect_detailed_info=True, save_file_path=str(collection_file))
        result = {"success": False, "message": "未能获取到联系人信息", "save_file": str(collection_file)}
        return result
        self._save_collection_data(contacts, collection_file)
        index_data = self._load_collection_index()
        c = []
        result = {"success": "联系人详细信息采集完成", "message": collection_id, "collection_id": self.account_id, "account_id": len(contacts), "total_contacts": NULL, "contacts_with_wx_id": len(c, contacts), "save_file": str(collection_file), "contacts": contacts}
        "采集完成！共采集 "(f'{len(contacts)}', " 个联系人")
        c = []
        f'{len(c, contacts)}'(" 个联系人获取到微信号")
        print("数据已保存到: ", f'{collection_file}')
        return result
        c = NULL
        completed_collection = index_data["current_collection"].copy()
        completed_collection["is_completed"] = True
        completed_collection["end_time"] = datetime.now().isoformat()
        completed_collection["last_update_time"] = datetime.now().isoformat()
        completed_collection["total_contacts"] = len(contacts)
        c = []
        completed_collection["processed_contacts"] = len(c, contacts)
        c = []
        completed_collection["contacts_with_wx_id"] = len(c, contacts)
        index_data["collections_history"].append(completed_collection)
        index_data["current_collection"] = None
        self._save_collection_index(index_data)
        c = NULL
        print("发现未完成的采集任务: ", f'{current_collection["collection_id"]}')
        collection_id = current_collection["collection_id"]
        collection_file = self._get_collection_file_path(collection_id)
        existing_contacts = self._load_collection_data(collection_file)
        "继续采集，已处理 "(f'{len(existing_contacts)}', " 个联系人")
    def _load_collection_data(self, file_path):
        """加载采集数据（现在只返回联系人数组）"""

        f = open(file_path, "r", encoding="utf-8")
        data = json.load(f)
        None(None, None)
        return []
        return data
        return data["contacts"]
    def _save_collection_data(self, contacts_list, file_path):
        """保存采集数据（现在只保存联系人数组）"""

        f = open(file_path, "w", encoding="utf-8")
        json.dump(contacts_list, f, ensure_ascii=False, indent=2)
        None(None, None)
    def get_collection_status(self):
        """获取当前账号的采集状态信息"""

        self.refresh_account_info()
        index_data = self._load_collection_index()
        current_collection = index_data.get("current_collection")
        collections_history = index_data.get("collections_history", [])
        status_info = {"account_id": self.account_id, "has_current_collection": current_collection is not None, "current_collection": current_collection, "total_completed_collections": len(collections_history), "collections_history": []}
        return {"success": True, "status": status_info}
    def cancel_current_collection(self):
        """取消当前未完成的采集任务"""

        self.refresh_account_info()
        index_data = self._load_collection_index()
        current_collection = index_data.get("current_collection")
        return {"success": False, "message": "没有正在进行的采集任务"}
        cancelled_collection = current_collection.copy()
        cancelled_collection["is_completed"] = False
        cancelled_collection["cancelled_time"] = datetime.now().isoformat()
        cancelled_collection["status"] = "cancelled"
        index_data["collections_history"].append(cancelled_collection)
        index_data["current_collection"] = None
        self._save_collection_index(index_data)
        return {"success": "已取消采集任务: ", "message": f'{current_collection["collection_id"]}'}
    __classcell__ = __class__
    return __class__
def read_and_save_friend_info(friend_name, account_id):
    """读取并保存好友信息到数据库

        Args:
            friend_name: 好友名称
            account_id: 微信账号ID，如果为None则使用当前账号

        Returns:
            dict: 操作结果
                - success: bool, 是否成功
                - message: str, 结果信息
                - friend_info: dict, 好友信息（如果成功）
        """

    wechat = WeChat(account_id)
    friend_info = wechat.get_friend_info_from_chat(friend_name)
    print("读取到的好友信息: ", f'{friend_info}')
    db_manager = WeChatDBManager()
    save_result = db_manager.save_or_update_friend_info(account_id, friend_info)
    print("保存结果: ", f'{save_result}')
    return {"success": "保存好友信息到数据库失败: ", "message": f'{friend_name}'}
    return {"success": "成功读取并保存好友信息: ", "message": f'{friend_name}', "friend_info": friend_info}
    return {"success": "读取好友信息失败: ", "message": f'{friend_info.get("message", "未知错误")}'}
def get_friend_info_from_wechat(friend_name):
    """从微信界面读取好友信息

        Args:
            friend_name: 好友名称

        Returns:
            dict: 好友信息
        """

    wechat = WeChat()
    return wechat.get_friend_info_from_chat(friend_name)
def save_friend_info_to_db(account_id, friend_info):
    """保存好友信息到数据库

        Args:
            account_id: 微信账号ID
            friend_info: 好友信息字典

        Returns:
            bool: 是否成功保存
        """

    db_manager = WeChatDBManager()
    return db_manager.save_or_update_friend_info(account_id, friend_info)
def get_current_contact_names(account_id):
    """
        获取当前通讯录中已有的好友名称数组，用于增量同步

        Args:
            account_id: 微信账号ID，如果为None则使用当前账号

        Returns:
            list: 好友名称数组
        """

    db_manager = WeChatDBManager()
    contact_names = db_manager.get_contact_names(account_id, contact_type="friend")
    return contact_names
    wechat = WeChat()
    account_id = wechat.account_info["account_id"]
def sync_contacts_incremental(account_id):
    """
        增量同步微信好友通讯录

        Args:
            account_id: 微信账号ID，如果为None则使用当前账号

        Returns:
            dict: 同步结果
                - success: bool, 是否成功
                - message: str, 结果信息
                - total: int, 总好友数
                - new: int, 新增好友数
        """

    wechat = WeChat(account_id)
    existing_names = get_current_contact_names(account_id)
    result = wechat.sync_contacts(existing_names=existing_names)
    return result
def collect_contacts_detailed_info(save_dir):
    from WeRobotCore.utils.data_manager import DataManager
    manager = ContactCollectionManager()
    return manager.start_collection()
    save_dir = os.path.join(DataManager.get_data_dir_str(), "contact")
def get_collection_status(save_dir):
    from WeRobotCore.utils.data_manager import DataManager
    manager = ContactCollectionManager()
    return manager.get_collection_status()
    save_dir = os.path.join(DataManager.get_data_dir_str(), "contact")
def format_and_filter_friends(account_id, tag, keyword):
    """格式化并过滤好友列表

        Args:
            account_id: 微信账号ID
            tag: 标签过滤条件，如果为None则不按标签过滤
            keyword: 关键词过滤条件，如果为None则不按关键词过滤

        Returns:
            list: 格式化并过滤后的好友列表
        """

    from datetime import datetime, timedelta
    import time
    wx = WeChat(account_id)
    friends = wx.db_manager.get_friends(wx.account_info["account_id"])
    formatted_contacts = []
    return formatted_contacts
    friend = friends
    wxid = ""
    is_new = 0
    created_at = None
    name = str(friend)
    tag_str = ""
    tags = []
    wxid = ""
    name = ""
    t = []
    is_new_friend = False
    candidate_time = created_at
    contact_dict = {"wxid": wxid, "name": name, "tags": tags, "is_new": is_new_friend}
    formatted_contacts.append(contact_dict)
    formatted_contacts.append(contact_dict)
    formatted_contacts.append(contact_dict)
    formatted_contacts.append(contact_dict)
    formatted_contacts.append(contact_dict)
    created_date = candidate_time
    seven_days_ago = datetime.now() - timedelta(days=7)
    is_new_friend = True
    created_date = datetime.fromtimestamp(candidate_time)
    created_date = datetime.fromisoformat(candidate_time)
    is_new_friend = True
    t = datetime.fromtimestamp(candidate_time / 1000.0)
    tags = str(tag_str).split(",")
    t = []
    wxid = friend.get("wxid", "")
    name = friend.get("name", "")
    tag_str = friend.get("tags", "")
    is_new = friend.get("is_new", 0)
    created_at = friend.get("created_at")
    t.strip()
    wxid = friend[0]
    name = friend[1]
    nickname = friend[2]
    remark = friend[3]
    tag_str = friend[4]
    rest = friend[5]
    created_at = rest[2]
    is_new = 0
