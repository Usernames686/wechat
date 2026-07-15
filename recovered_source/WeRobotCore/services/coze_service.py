# Decompiled from: coze_service.pyc
# Python 3.12 bytecode (mode: cfg)

from datetime import datetime, timezone
from pathlib import Path
import json
import requests
import asyncio
import time
from aiohttp import ClientSession
from typing import Optional, Dict, Any, List
_COZE_CONFIG_HINTS = {4100: "token 无效，请在 coze.cn → 个人设置 → API 密钥中重新生成并更新", 4011: "账户 Token 余额不足，请登录 coze.cn 充值或升级套餐", 4006: "智能体 ID 不存在，请检查 botId/agentId 配置是否正确", 4015: "智能体尚未发布到 API，请在 coze.cn 发布该智能体后再试", 4012: "模型无效或已下架，请在 coze.cn 更换智能体使用的模型"}
class CozeService(AIServiceBase):
    """CozeService"""

    def __init__(self, token):
        super().__init__(token)
        self.base_url = "https://api.coze.cn/v3"
        self.headers = {"Authorization": f'{token}', "Content-Type": "application/json"}
        self._session = None
    @property
    def session(self):
        import aiohttp
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30, ttl_dns_cache=600, use_dns_cache=True, enable_cleanup_closed=True, family=0, ssl=False)
        timeout = aiohttp.ClientTimeout(total=45, connect=15, sock_read=30)
        self._session = aiohttp.ClientSession(headers=self.headers, connector=connector, timeout=timeout)
        return self._session
    def close(self):
        """关闭aiohttp会话"""

        yield None
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
    def _clear_conversation_cache(self, session_id):
        """清空指定会话的缓存"""

        conversations = self._load_conversations()
        del conversations[session_id]
        self._save_conversations(conversations)
        print("已清空会话缓存: ", f'{session_id}')
    def generate_comment(self, content, agent_id, session_id, user_name, session_name, account_id):
        """
                使用Coze智能体生成评论
                """

        None(f'{50}', "...")
        message_content = {"role": "user", "content_type": "text", "content": content}
        yield None
    def start_chat(self, agent_id, message, session_id, user_name, session_name, account_id, cache_session, friend_tags):
        """启动一个完整的对话流程"""

        max_retries = 3
        return {"success": False, "error": "对话请求失败，已达到最大重试次数", "reply": None}
        retry_count = range(max_retries + 1)
        yield None
    def _is_retriable_error(self, error_msg):
        """判断错误是否可重试"""

        retriable_keywords = ("getaddrinfo failed", "connection timeout", "connection reset", "dns resolution", "temporary failure", "network unreachable", "connection refused", "timeout")
        return any((keyword for keyword in _iter)(retriable_keywords))
    def _start_chat(self, agent_id, message, session_id, user_name, session_name, account_id, cache_session, friend_tags):
        """初始化对话"""

        max_retries = 3
        base_delay = 1
        max_delay = 5
        attempt = range(max_retries)
        url = "/chat"
        conversation_id = None
        user_id = f'{int(time.time() * 1000)}'
        additional_messages = [message]
        request_data = {"bot_id": agent_id, "user_id": user_id, "stream": False, "auto_save_history": True, "additional_messages": additional_messages}
        f'{max_retries}'(") ", f'{json.dumps(request_data, ensure_ascii=False, indent=2)}')
        yield None
        request_data["parameters"] = {"user": [{"user_name": user_name, "session_name": session_name, "session_id": session_id, "account_id": account_id, "friend_tags": friend_tags}]}
        friend_tags = ""
        conversation_id = self._get_conversation_id(session_id)
        url = f'{conversation_id}'
    def upload_file(self, file_path, ser_id):
        """上传文件到Coze"""

        f = open(file_path, "rb")
        response = requests.post("https://api.coze.cn/v1/files/upload", headers={"Authorization": self.headers["Authorization"]}, files={"file": f})
        None(None, None)
        data = response.json()
        print("Coze上传文件成功: ", f'{data["data"]["id"]}')
        return {"success": True, "file_id": data["data"]["id"], "file_name": data["data"]["file_name"]}
        error_msg = self._get_error_message(data.get("code"), data.get("msg"))
        print("Coze上传文件失败: ", f'{error_msg}')
        return {"success": False, "error": error_msg}
    def _wait_for_completion(self, conversation_id, chat_id):
        """等待对话完成"""

        max_retries = 300
        return {"success": False, "error": "等待回复超时"}
        i = range(max_retries)
        yield None
    def _get_error_message(self, code, msg):
        """获取错误信息"""

        error_messages = {4002: "指定的会话不存在", 4006: "智能体ID不存在", 4010: "问题太长，超过限制", 4011: "账户Token余额不足", 4012: "模型无效（模型可能已下架）", 4015: "智能体没有发布到API", 4016: "当前会话已有chat在运行", 4100: "身份验证无效"}
        return "Coze服务异常(code:"(f'{code}', "): ", f'{msg}')
    def _get_reply(self, conversation_id, chat_id):
        """获取回复内容"""

        yield None
    def get_benefits(self):
        url = "https://api.coze.cn/v1/commerce/benefit/benefits/get"
        yield None
    __classcell__ = __class__
    return __class__
