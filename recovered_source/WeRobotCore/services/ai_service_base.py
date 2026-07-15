# Decompiled from: ai_service_base.pyc
# Python 3.12 bytecode (mode: cfg)

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import asyncio
from pathlib import Path
import json
from datetime import datetime, timezone
class AIServiceBase(ABC):
    """AIServiceBase"""

    __doc__ = "智能体服务基类，定义所有智能体平台共有的接口"
    def __init__(self, token):
        self.token = token
        self.conversations_file = f'{self.__class__.__name__.lower()}' / "_conversations.json"
        self.conversations_file.parent.mkdir(parents=True, exist_ok=True)
    @abstractmethod
    def close(self):
        """关闭会话"""
    def __aenter__(self):
        """异步上下文管理器入口"""

        return self
    def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口，自动关闭会话"""

        yield None
    def _load_conversations(self):
        """加载会话记录"""

        return {}
        return json.loads(self.conversations_file.read_text())
    def _save_conversations(self, conversations):
        """保存会话记录"""

        self.conversations_file.write_text(json.dumps(conversations, indent=2))
    def _get_conversation_id(self, session_id):
        """获取会话ID"""

        conversations = self._load_conversations()
        session_info = conversations.get(session_id)
        last_time = datetime.fromisoformat(session_info["last_time"])
        now = datetime.now(timezone.utc)
        return session_info["conversation_id"]
    def _update_conversation(self, session_id, conversation_id):
        """更新会话记录"""

        conversations = self._load_conversations()
        conversations[session_id] = {"session_id": session_id, "conversation_id": conversation_id, "last_time": datetime.now(timezone.utc).isoformat()}
        self._save_conversations(conversations)
    start_chat = abstractmethod((lambda self, agent_id, message, session_id, user_name, session_name, account_id, cache_session: ...))
    generate_comment = abstractmethod((lambda self, content, agent_id: ...))
    upload_file = abstractmethod((lambda self, file_path, user_id: ...))
