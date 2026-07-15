# Decompiled from: chat_history.pyc
# Python 3.12 bytecode (mode: cfg)

from email import message
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
from WeRobotCore.core.WeChatType import WeChat
class ChatHistoryManager:
    """ChatHistoryManager"""

    _instances = {}
    _default_instance = None
    def __new__(cls, account_id):
        """支持多账号的单例模式实现"""

        return cls._instances[account_id]
        instance = super().__new__(cls)
        instance._initialized = False
        instance.account_id = account_id
        cls._instances[account_id] = instance
        return cls._default_instance
        cls._default_instance = super().__new__(cls)
        cls._default_instance._initialized = False
        cls._default_instance.account_id = None
    def __init__(self, account_id):
        from WeRobotCore.utils.data_manager import DataManager
        self._initialized = True
        self._lock = asyncio.Lock()
        self._history_dir = os.path.join(DataManager.get_data_dir_str(), "chat_history")
        self._max_messages = 100
        self.wechat = None
        self._initialized = True
        self.wechat = WeChat(self.account_id)
        self._history_dir = os.path.join(DataManager.get_data_dir_str(), "chat_history", self.account_id)
        os.makedirs(self._history_dir, exist_ok=True)
        self._sessions_index_path = os.path.join(self._history_dir, "sessions_index.json")
        self._init_sessions_index()
        self._initialized = True
        self.account_id = account_id
    def _init_sessions_index(self):
        """初始化会话索引文件"""

        f = open(self._sessions_index_path, "w", encoding="utf-8")
        json.dump({"sessions": [], "last_updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
        None(None, None)
    def _get_history_file(self, session_id):
        """获取会话历史记录文件路径"""

        filename = hashlib.md5(session_id.encode()).hexdigest()
        return os.path.join(self._history_dir, f'{filename}', ".json")
    def get_sessions_index(self):
        """获取会话索引列表"""

        return []
        yield None
        print("ChatHistoryManager: 账号ID为空，返回空会话索引")
        return []
    def update_session_index(self, session_name, session_id, last_message, is_group, last_message_fingerprint):
        """更新会话索引"""

        yield None
    def load_history(self, session_id):
        """加载会话历史记录"""

        history_file = self._get_history_file(session_id)
        yield None
        return []
        print("ChatHistoryManager: 账号ID为空，返回空历史记录")
        return []
    def save_messages(self, session_id, session_name, messages, is_group):
        """保存会话消息"""

        yield None
        print("ChatHistoryManager: 账号ID为空，跳过消息保存")
    def delete_session(self, session_id):
        """删除指定会话的本地历史记录：消息文件 + 会话索引条目。

                session_id 即会话名（保存时 session_id=session_name，文件名取其 md5）。
                重名会话因 md5 相同本就是同一份文件，删除即可清掉被"串"在一起的污染记录。
                """

        history_file = self._get_history_file(session_id)
        yield None
        os.remove(history_file)
        print("ChatHistoryManager: 账号ID为空，无法删除会话历史")
        return False
    def get_last_message_fingerprint(self, session_id):
        """获取会话最后一条消息的指纹"""

        yield None
    def build_context_messages(self, session_id, session_name, all_messages, current_fingerprint, sender_name, context_count):
        """构建智能上下文消息列表，避免重复携带已存在于智能体平台的消息"""

        context_messages = []
        yield None
        print("ChatHistoryManager: 账号ID为空，跳过上下文消息")
        return context_messages
    __classcell__ = __class__
    return __class__
