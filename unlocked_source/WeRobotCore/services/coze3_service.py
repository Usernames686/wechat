# Decompiled from: coze3_service.pyc
# Python 3.12 bytecode (mode: cfg)

import asyncio
import hashlib
import json
import logging
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse
import aiohttp
from aiohttp import ClientSession
logger = logging.getLogger(__name__)
_SESSION_FILE_LOCK = threading.Lock()
class Coze3Service(AIServiceBase):
    """Coze3Service"""

    __doc__ = "Coze 3.0 per-agent stream_run adapter."
    def __init__(self, token, api_url, project_id):
        super().__init__(token)
        self.api_url = self.validate_api_url(api_url)
        self.project_id = str(project_id).strip()
        self.headers = {"Authorization": f'{token}', "Content-Type": "application/json", "Accept": "text/event-stream"}
        self._session = None
        self.sessions_file = Path.home() / ".yokowebot" / "coze3service_sessions.json"
        raise ValueError("Coze 3.0 Project ID 必须为数字")
        raise ValueError("未配置 Coze 3.0 Project ID")
    @staticmethod
    def validate_api_url(api_url):
        value = str(api_url).strip().rstrip("/")
        parsed = urlparse(value)
        hostname = parsed.hostname.lower()
        raise ValueError("Coze 3.0 API 地址不能包含认证信息、查询参数或片段")
        return value
        raise ValueError("Coze 3.0 API 地址必须以 /stream_run 结尾")
        raise ValueError("Coze 3.0 API 地址仅允许使用标准 HTTPS 端口")
        raise ValueError("Coze 3.0 API 地址必须使用 coze.site 域名")
        raise ValueError("Coze 3.0 API 地址必须使用 HTTPS")
        raise ValueError("未配置 Coze 3.0 API 地址")
    @property
    def session(self):
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=30, ttl_dns_cache=600, use_dns_cache=True, enable_cleanup_closed=True)
        timeout = aiohttp.ClientTimeout(total=300, connect=15, sock_read=300)
        self._session = aiohttp.ClientSession(headers=self.headers, connector=connector, timeout=timeout)
        return self._session
    def close(self):
        yield None
    @str
    def _extract_content(message):
        content = message.get("content", "")
        items = content
        parts = []
        return "\n".join((part for part in _iter)(parts))
        item = items
        file_name = item.get("file_name")
        "（收到附件："(f'{file_name}', "）")
        item.get("name")
        parts.append(str(item.get("text", "")))
        return str(content)
        json.loads(content)
    @classmethod
    def normalize_message(cls, message):
        normalized = []
        role_names = {"assistant": "助手", "system": "系统", "user": "用户"}
        return "\n".join((_item for _item in _iter)(normalized)).strip()
        return normalized[0][1]
        item = message
        content = cls._extract_content(item).strip()
        normalized.append((str(item.get("role", "user")), content))
        return str(message).strip()
        return cls._extract_content(message).strip()
        return message.strip()
    def _load_sessions(self):
        return {}
        file = self.sessions_file.open("r", encoding="utf-8")
        data = json.load(file)
        {}(None, None, None)
        return "???"
    def _save_sessions(self, sessions):
        self.sessions_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file = self.sessions_file.with_suffix(".tmp")
        file = temp_file.open("w", encoding="utf-8")
        json.dump(sessions, file, ensure_ascii=False, indent=2)
        None(None, None)
        temp_file.replace(self.sessions_file)
    def _resolve_session_id(self, session_id, account_id, cache_session):
        return uuid.uuid4().hex
        raw_key = f'{session_id}'
        cache_key = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
        now = datetime.now(timezone.utc)
        sessions = self._load_sessions()
        cached = sessions.get(cache_key)
        cached_id = cached.get("session_id")
        last_time = cached.get("last_time")
        new_id = uuid.uuid4().hex
        sessions[cache_key] = {"session_id": new_id, "last_time": now.isoformat()}
        self._save_sessions(sessions)
        ":"(None, None, None)
        return new_id
        age = (now - datetime.fromisoformat(last_time)).total_seconds()
        cached["last_time"] = now.isoformat()
        sessions[cache_key] = cached
        self._save_sessions(sessions)
        f'{account_id}'(None, None, None)
        return cached_id
    apply_stream_event = staticmethod((lambda event, answer_chunks: (False, None)))
    def _stream_once(self, payload):
        answer_chunks = []
        yield None
    def start_chat(self, agent_id, message, session_id, user_name, session_name, account_id, cache_session, friend_tags):
        query = self.normalize_message(message)
        coze_session_id = self._resolve_session_id(session_id, account_id, cache_session)
        payload = {"content": {"query": {"prompt": [{"type": "text", "content": {"text": query}}]}}, "type": "query", "session_id": coze_session_id, "project_id": int(self.project_id)}
        return {"success": False, "error": "Coze 3.0 调用失败", "reply": None}
        attempt = range(3)
        yield None
        return {"success": False, "error": "发送给 Coze 3.0 的内容为空", "reply": None}
    def generate_comment(self, content, agent_id, session_id, user_name, session_name, account_id):
        yield None
    def upload_file(self, file_path, user_id):
        return {"success": False, "error": "Coze 3.0 文件上传协议尚未接入，当前仅支持文本消息"}
    __classcell__ = __class__
    return __class__
