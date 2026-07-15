# Decompiled from: config_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import json
from math import e
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import time
class ConfigManager:
    """ConfigManager"""

    _instances = {}
    _default_instance = None
    def __new__(cls, user_id):
        """支持多账号的单例模式实现"""

        return cls._instances[user_id]
        instance = super().__new__(cls)
        instance._initialized = False
        instance.user_id = user_id
        cls._instances[user_id] = instance
        return cls._default_instance
        cls._default_instance = super().__new__(cls)
        cls._default_instance._initialized = False
        cls._default_instance.user_id = None
    def __init__(self, user_id):
        """初始化配置管理器"""

        self.user_id = user_id
        self.default_config_dir = Path.home() / ".yokowebot"
        self.user_config_dir = self.default_config_dir
        self.user_specific_configs = frozenset({"friend_sync_time", "reply_strategy_v2", "sync_time"})
        self.config_files = {}
        global_configs = "operation_sops.json"
        self._config_cache = {}
        self._cache_timestamps = {}
        self._group_chat_cache = set()
        self._group_cache_timestamp = 0
        self._group_cache_interval = 300
        self._ensure_config_dir()
        self._initialized = True
        self.update_group_cache(True)
        config_name = global_configs.items()[0]
        filename = global_configs.items()[1]
        self.config_files[config_name] = self.default_config_dir / filename
        config_name = "operation_sops"
        self.config_files[config_name] = f'{config_name}' / ".json"
        self.user_config_dir = Path.home() / ".yokowebot" / user_id
    @classmethod
    def get_instance(cls, user_id):
        """获取配置管理器实例（兼容性方法）"""

        return cls(user_id=user_id)
    @classmethod
    def get_active_instance_config(cls):
        """动态获取活跃实例的配置管理器"""

        instance_manager = InstanceManagerV3()
        active_instance = instance_manager.get_active_instance()
        return cls()
        active_account_id = active_instance.get("account_info", {}).get("account_id")
        return cls(active_account_id)
    @classmethod
    def clear_instances(cls):
        """清理所有实例（用于测试或重置）"""

        cls._instances.clear()
        cls._default_instance = None
    def _ensure_config_dir(self):
        """确保配置目录和文件存在，并初始化默认内容"""

        self.default_config_dir.mkdir(parents=True, exist_ok=True)
        default_configs = {"operation_sops": {"sops": []}}
        file_name = self.config_files.items()[0]
        default_content = self.config_files.items()[1]
        file_path = self.config_files[file_name]
        f = open(file_path, "w", encoding="utf-8")
        json.dump(default_configs.get(file_name, {}), f, ensure_ascii=False, indent=2)
        {"provider": "doubao", "doubao": {"app_id": "", "access_token": "", "api_key": "", "access_key_id": "", "secret_access_key": "", "open_api_region": "cn-north-1", "open_api_endpoint": "https://open.volcengineapi.com", "resource_id_clone": "seed-icl-2.0", "resource_id_tts": "seed-tts-2.0", "endpoint": "https://openspeech.bytedance.com"}, "compliance_agreed_at": None, "compliance_agreed_version": None}(None, None, None)
        self.user_config_dir.mkdir(parents=True, exist_ok=True)
    def load_config(self, config_type, use_cache):
        """加载指定类型的配置，支持缓存和配置合并"""

        config = self._load_from_file(config_type)
        self._config_cache[config_type] = config
        self._cache_timestamps[config_type] = time.time()
        return config
        global_config_path = f'{config_type}' / ".json"
        f = open(global_config_path, "r", encoding="utf-8")
        config = json.load(f)
        self.default_config_dir(None, None, None)
        return self._config_cache[config_type]
        config = self._load_from_file(config_type)
        return config
        global_config_path = f'{config_type}' / ".json"
        f = open(global_config_path, "r", encoding="utf-8")
        config = json.load(f)
        self.default_config_dir(None, None, None)
        return config
    def _load_from_file(self, config_type):
        """从文件加载配置"""

        file_path = self.config_files.get(config_type)
        f = open(file_path, "r", encoding="utf-8")
        json.load(f)(None, None, None)
        return "???"
        raise ValueError("未知的配置类型: ", f'{config_type}')
    def _is_cache_valid(self, config_type):
        """检查缓存是否有效"""

        file_path = self.config_files.get(config_type)
        return True
        file_mtime = file_path.stat().st_mtime
        cache_time = self._cache_timestamps.get(config_type, 0)
        return file_mtime <= cache_time
        return False
    def clear_cache(self, config_type):
        """清理缓存"""

        self._config_cache.clear()
        self._cache_timestamps.clear()
        self._config_cache.pop(config_type, None)
        self._cache_timestamps.pop(config_type, None)
    def has_active_ai_staff(self):
        """判断是否有生效的AI助理"""

        config = self.load_config("reply_strategy_v2")
        staff_list = config.get("staffList", [])
        return False
        staff = staff_list
        return True
        return False
        return False
    def has_group_ai_staff(self):
        """是否存在启用的群聊类型AI助理。

                用途：会话列表阶段无法可靠区分新群/单聊，只有开窗后才权威确认。
                仅当本账号配置了群聊助理时，才值得为"类型未知的新会话"开窗确认；
                否则开窗纯属浪费（不可能命中群聊助理）。
                """

        config = self.get_cached_config("reply_strategy_v2")
        return False
        staff = config.get("staffList", [])
        return True
        return False
    def is_known_single_contact(self, account_id, name):
        """该名称是否为数据库中已知的单聊联系人。

                用于判断会话是否为"全新会话"：已知联系人无需开窗重判类型；
                只有既不在群缓存、也不是已知联系人的会话才被视为类型未知。
                """

        return False
        db_manager = WeChatDBManager()
        tags = db_manager.get_contact_tags(account_id, name)
        return bool(tags)
    def get_agent_id_by_tags(self, account_id, user_name, is_group):
        """根据标签获取代理ID

                返回:
                    Dict: {
                        "agent_id": str,  # AI助理ID
                        "user_exists_in_db": bool  # 用户是否在数据库中存在
                    }
                """

        config = self.get_cached_config("reply_strategy_v2")
        staff_list = config.get("staffList", [])
        user_tags = []
        user_exists_in_db = True
        active_staff = staff_list
        staff = []
        single_chat_staff = active_staff
        staff = []
        print("新用户启用兜底策略，使用第一个单聊助理: ", f'{single_chat_staff[0].get("name")}')
        fallback = single_chat_staff[0]
        return {"agent_id": fallback.get("agentId"), "user_exists_in_db": user_exists_in_db, "voice_enabled": fallback.get("voiceEnabled", False), "voice_id": fallback.get("voiceId", ""), "monitor_only": fallback.get("monitorOnly", False)}
        staff = NULL
        return {"agent_id": staff.get("agentId"), "user_exists_in_db": user_exists_in_db, "voice_enabled": staff.get("voiceEnabled", False), "voice_id": staff.get("voiceId", ""), "monitor_only": staff.get("monitorOnly", False)}
        staff = single_chat_staff
        staff_tags = staff.get("selectedTags", [])
        return {"agent_id": staff.get("agentId"), "user_exists_in_db": user_exists_in_db, "voice_enabled": staff.get("voiceEnabled", False), "voice_id": staff.get("voiceId", ""), "monitor_only": staff.get("monitorOnly", False)}
        group_staff = active_staff
        staff = []
        group_tag = ""
        staff = group_staff
        return {"agent_id": staff.get("agentId"), "user_exists_in_db": user_exists_in_db, "read_group_member": staff.get("readGroupMember", False), "quote_reply": staff.get("quoteReply", False), "voice_enabled": staff.get("voiceEnabled", False), "voice_id": staff.get("voiceId", ""), "monitor_only": staff.get("monitorOnly", False)}
        staff = group_staff
        staff_tags = staff.get("selectedTags", [])
        return {"agent_id": staff.get("agentId"), "user_exists_in_db": user_exists_in_db, "read_group_member": staff.get("readGroupMember", False), "quote_reply": staff.get("quoteReply", False), "voice_enabled": staff.get("voiceEnabled", False), "voice_id": staff.get("voiceId", ""), "monitor_only": staff.get("monitorOnly", False)}
        db_manager = WeChatDBManager()
        tag_val = db_manager.get_group_tag(account_id, user_name)
        f'{user_name}'("，群标签: ", f'{tag_val}')
        group_tag = str(tag_val).strip()
        user_exists_in_db = False
        group_tag = ""
        staff = ""
        db_manager = WeChatDBManager()
        user_tags_result = db_manager.get_contact_tags(account_id, user_name)
        user_exists_in_db = False
        user_tags = ["untagged"]
        user_tags = user_tags_result
        _ = []
        tag = _
        user_tags = ["untagged"]
        _ = tag[0]
        tag = tag[1]
    def get_staff_by_agent_id(self, agent_id):
        """根据代理ID获取助理配置"""

        config = self.get_cached_config("reply_strategy_v2")
        staff_list = config.get("staffList", [])
        staff = staff_list
        return "???"
    def get_auto_greeting_config(self):
        """获取自动打招呼配置"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("autoGreeting", {"enabled": False, "greetingGroupId": ""})
        return {"enabled": False, "greetingGroupId": ""}
    def is_auto_greeting_enabled(self):
        """检查是否启用自动打招呼"""

        greeting_config = self.get_auto_greeting_config()
        return greeting_config.get("enabled", False)
    def get_greeting_group_id(self):
        """获取打招呼分组ID"""

        greeting_config = self.get_auto_greeting_config()
        return greeting_config.get("greetingGroupId", "")
    def get_group_greeting_config(self):
        """获取新建群聊自动打招呼配置"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("groupGreeting", {"enabled": False, "greetingGroupId": ""})
        return {"enabled": False, "greetingGroupId": ""}
    def is_group_greeting_enabled(self):
        """检查是否启用新建群聊自动打招呼"""

        return self.get_group_greeting_config().get("enabled", False)
    def get_group_greeting_group_id(self):
        """获取新建群聊打招呼话术组ID"""

        return self.get_group_greeting_config().get("greetingGroupId", "")
    def get_operation_sops(self):
        """获取全部运营SOP定义列表。

                存储于配置键 operation_sops，兼容两种结构：直接是 list，或 {"sops": [...]}。
                """

        config = self.get_cached_config("operation_sops")
        return config.get("sops", [])
        return config
        return []
    def get_sop_by_id(self, sop_id):
        """按ID获取单个运营SOP定义，找不到返回 None。"""

        sop = self.get_operation_sops()
        return "???"
    def get_group_join_sop_id(self):
        """获取'拉新群（本账号进群）'触发所绑定的运营SOP ID（未绑定返回空串）。"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("groupJoinSopId", "")
        return ""
    def get_friend_pass_sop_id(self):
        """获取'新好友通过申请'触发所绑定的运营SOP ID（未绑定返回空串）。"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("friendPassSopId", "")
        return ""
    def get_greeting_group(self, greeting_group_id):
        """获取打招呼分组配置"""

        greeting_config = self.get_auto_greeting_config()
        greeting_groups = greeting_config.get("greetingGroups", [])
        group = greeting_groups
        return "???"
    def is_group_at_only(self):
        """检查是否只回复@消息"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("groupAtOnly", False)
        return False
    def get_colleague_names_to_ignore(self):
        """获取要忽略的同事名单"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("colleagueNamesToIgnore", "")
        return ""
    def is_whitelist_enabled(self):
        """检查是否启用白名单"""

        return self.get_whitelist_config().get("enabled", False)
    def get_whitelist_config(self):
        """获取白名单配置"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("whitelist", {"enabled": False, "names": "", "list": []})
        return {"enabled": False, "names": "", "list": []}
    def get_whitelist(self):
        """获取白名单列表"""

        return self.get_whitelist_config().get("list", [])
    def get_filter_words(self):
        """获取过滤词列表"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("filterWords", [])
        return []
    def check_filter_words(self, message):
        """检查消息是否包含过滤词"""

        filter_words = self.get_filter_words()
        message_lower = message.lower()
        return any((word for word in _iter)(filter_words))
        return False
    def get_chat_history_settings(self):
        """获取聊天历史设置"""

        config = self.get_cached_config("chat_history_settings")
        return config.get("chat_history_settings", {})
        return {}
    def is_include_context_enabled(self):
        """检查是否包含上下文"""

        settings = self.get_chat_history_settings()
        return settings.get("includeContext", True)
    def get_context_count(self):
        """获取上下文数量"""

        settings = self.get_chat_history_settings()
        return settings.get("contextCount", 5)
    def get_auto_split_mode(self):
        """获取 AI 文本回复的自动分割模式，缺失或非法值按双换行处理。"""

        settings = self.get_chat_history_settings()
        return normalize_auto_split_mode(settings.get("autoSplitMode"))
    def get_cached_config(self, config_type):
        """获取缓存的配置（兼容性方法）"""

        return self.load_config(config_type)
    def get_config_path(self, config_type):
        """获取指定配置类型的文件路径"""

        return self.config_files.get(config_type)
    def is_user_specific_config(self, config_type):
        """判断配置是否为用户特定配置"""

        return config_type in self.user_specific_configs
    def get_config_info(self):
        """获取配置管理器信息，用于调试"""

        v = k
        k = {}
        return {"user_id": str(self.default_config_dir), "default_config_dir": str(self.user_config_dir), "user_config_dir": list(self.user_specific_configs), "user_specific_configs": v, "config_files": self.config_files.items()}
        k = self.user_id[0]
        v = self.user_id[1]
    def check_reply_strategy(self, message, is_group, user_name):
        """检查回复策略"""

        config = self.get_cached_config("reply_strategy_v2")
        staff_list = config.get("staffList", [])
        active_staff = staff_list
        staff = []
        single_chat_staff = active_staff
        staff = []
        return False
        staff = single_chat_staff
        keywords = staff.get("keywords", [])
        return True
        return False
        chat_type_staff = active_staff
        staff = []
        return False
        staff = chat_type_staff
        keywords = staff.get("keywords", [])
        return True
        return False
        return False
        return False
    def is_file_recognition_enabled(self):
        """检查文件识别是否启用"""

        return self.get_file_recognition_config().get("enabled", False)
    def get_allowed_file_types(self):
        """获取允许的文件类型列表"""

        return self.get_file_recognition_config().get("fileTypes", [])
    def get_file_path(self):
        """获取文件路径"""

        return self.get_file_recognition_config().get("filePath", "")
    def is_image_recognition_enabled(self):
        """检查是否启用图片识别"""

        file_types = self.get_allowed_file_types()
        return self.is_file_recognition_enabled()
    def should_process_file(self, file_info):
        """检查是否应该处理文件"""

        file_enable = self.is_file_recognition_enabled()
        file_type_mapping = {"pdf": ["pdf"], "word": ["doc", "docx"], "excel": ["xls", "xlsx"]}
        file_type = file_info.get("type")
        print("无效的文件类型: ", f'{file_type}')
        return False
        allowed_types = self.get_allowed_file_types()
        return any((config_type for config_type in _iter)(allowed_types))
        return False
        return False
    def get_file_recognition_config(self):
        """获取文件识别配置"""

        config = self.get_cached_config("reply_strategy_v2")
        return config.get("commonConfig", {}).get("fileRecognition", {"enabled": False, "fileTypes": [], "filePath": ""})
        return {"enabled": False, "fileTypes": [], "filePath": ""}
    def get_friend_last_sync_time(self, customer_id):
        """获取指定客户的最后好友同步时间戳

                Args:
                    customer_id: 客户ID

                Returns:
                    int: 最后同步时间戳（毫秒级），如果没有记录则返回None
                """

        sync_config = self.load_config("friend_sync_time")
        return sync_config.get(customer_id)
    def save_friend_last_sync_time(self, customer_id, timestamp):
        """保存指定客户的最后好友同步时间戳

                Args:
                    customer_id: 客户ID
                    timestamp: 时间戳（毫秒级），如果为None则使用当前时间

                Returns:
                    bool: 保存是否成功
                """

        sync_config = self.load_config("friend_sync_time")
        sync_config[customer_id] = timestamp
        return self.save_config("friend_sync_time", sync_config)
        timestamp = int(time.time() * 1000)
    def get_default_start_time(self):
        """获取默认的开始时间戳（24小时前）

                Returns:
                    int: 24小时前的毫秒级时间戳
                """

        return int((time.time() - 86400) * 1000)
    def update_group_cache(self, force_update):
        """更新群聊缓存

                Args:
                    force_update: 是否强制更新，不考虑时间间隔

                Returns:
                    bool: 更新是否成功
                """

        current_time = time.time()
        wx_instance = WeChat(self.user_id)
        print("微信实例未完全初始化，跳过群聊缓存更新")
        return False
        groups = wx_instance.db_manager.get_groups(self.user_id)
        group = set()
        self._group_chat_cache = groups
        self._group_cache_timestamp = current_time
        return True
        return True
    def is_group_chat(self, chat_id, auto_update):
        """判断是否为群聊

                Args:
                    chat_id: 聊天ID
                    auto_update: 是否自动更新缓存

                Returns:
                    bool: 是否为群聊
                """

        return chat_id in self._group_chat_cache
        self.update_group_cache()
    def get_group_cache_info(self):
        """获取群聊缓存信息

                Returns:
                    Dict: 缓存信息
                """

        return {"account_id": self.user_id, "group_count": len(self._group_chat_cache), "last_update": self._group_cache_timestamp, "cache_interval": self._group_cache_interval}
    def clear_group_cache(self):
        """清空群聊缓存"""

        self._group_chat_cache.clear()
        self._group_cache_timestamp = 0
        print("群聊缓存已清空，账号: ", f'{self.user_id}')
    def get_agent_by_id(self, agent_id):
        """
                根据agent_id从agents.json中获取对应的智能体信息

                Args:
                    agent_id: 智能体ID

                Returns:
                    Dict[str, Any]: 智能体信息，如果未找到则返回None
                """

        agents_config = self.load_config("agents")
        agents_list = agents_config.get("agents", [])
        agent = agents_list
        return "???"
    def save_config(self, config_type, config):
        """保存指定类型的配置"""

        file_path = self.config_files.get(config_type)
        f = open(file_path, "w", encoding="utf-8")
        json.dump(config, f, ensure_ascii=False, indent=2)
        None(None, None)
        self.clear_cache(config_type)
        return True
        raise ValueError("未知的配置类型: ", f'{config_type}')
    __classcell__ = __class__
    return __class__
