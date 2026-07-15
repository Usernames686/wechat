# Decompiled from: fireflow_service.pyc
# Python 3.12 bytecode (mode: cfg)

import json
import time
import requests
import os
from aiohttp import ClientSession, TCPConnector
from typing import Optional, Dict, Any, List
from datetime import datetime
class FireflowService(AIServiceBase):
    """FireflowService"""

    def __init__(self, token, base_url):
        super().__init__(token)
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f'{token}', "Content-Type": "application/json", "x-channel-id": "agent_generic"}
        self._session = None
    @property
    def session(self):
        connector = TCPConnector(ssl=False)
        self._session = ClientSession(headers=self.headers, connector=connector)
        return self._session
    def close(self):
        """关闭aiohttp会话"""

        yield None
    def generate_comment(self, content, agent_id, session_id, user_name, session_name, account_id):
        """
                使用Fireflow智能体生成评论
                """

        None(f'{50}', "...")
        request_data = {"user_id": f'{int(time.time() * 1000)}', "query": content, "inputs": {}}
        log_query = request_data["query"]
        print("Fireflow请求>>>>> ", f'{json.dumps(log_query, ensure_ascii=False, indent=2)}')
        yield None
        log_query = 50 + "... [已截断]"
        request_data["inputs"] = {"user_name": user_name, "session_name": session_name, "session_id": session_id, "account_id": account_id}
        account_id = str(account_id)
        session_id = str(session_id)
    def _clear_conversation_cache(self, session_id):
        """清空指定会话的缓存"""

        conversations = self._load_conversations()
        del conversations[session_id]
        self._save_conversations(conversations)
        print("已清空会话缓存: ", f'{session_id}')
    def start_chat(self, agent_id, message, session_id, user_name, session_name, account_id, cache_session, friend_tags):
        """启动一个完整的对话流程"""

        max_retries = 3
        retry_count = range(max_retries + 1)
        conversation_id = None
        message_content = message
        history = []
        files = []
        request_data = {"user_id": f'{int(time.time() * 1000)}', "query": message_content.get("content", ""), "inputs": {}}
        log_data = request_data.copy()
        print("Fireflow请求>>>>> ", f'{json.dumps(log_data, ensure_ascii=False, indent=2)}')
        yield None
        log_data["history"] = "[历史上下文记录打包]"
        log_data["query"] = 100 + "... [已截断]"
        request_data["conversation_id"] = conversation_id
        request_data["inputs"] = {"user_name": user_name, "session_name": session_name, "session_id": session_id, "account_id": account_id}
        request_data["history"] = history
        request_data["files"] = files
        last_msg = message[-1]
        message_content = last_msg.get("content", "")
        msg = -1
        role = msg.get("role", "user")
        content = msg.get("content", "")
        history.append({"role": role, "content": content})
        content_obj = json.loads(content)
        item = content_obj
        content = item.get("text", "")
        content_obj = json.loads(last_msg.get("content", ""))
        item = content_obj
        file_url = item.get("url")
        files.append({"type": "file", "url": file_url})
        extracted_text = self._extracted_texts.pop(file_url, "")
        original_filename = getattr(self, "_extracted_filenames", {}).get(file_url, "未知文档")
        message_content = "\n\n====== 附件文档内容 ======\n" + f'{extracted_text}'
        message_content = f'{extracted_text}'
        message_content = item.get("text", "")
        conversation_id = self._get_conversation_id(session_id)
        account_id = str(account_id)
        session_id = str(session_id)
    def upload_file(self, file_path, user_id):
        """
                上传文件到Fireflow / 或在本地解析常见文档
                流程:
                1. 检查是否是可解析文档，如果是则本地解析提取文本并缓存
                2. 否则通过 /v1/oss/upload 换取预签名上传URL上传到OSS
                """

        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        import mimetypes
        content_type = mimetypes.guess_type(file_path)[0]
        _ = mimetypes.guess_type(file_path)[1]
        uid = f'{int(time.time() * 1000)}'
        oss_key = f'{file_name}'
        request_data = {"key": oss_key, "contentType": content_type}
        print("请求上传预签名URL: ", f'{oss_key}')
        yield None
        content_type = "application/octet-stream"
        extracted_text = DocumentExtractor.extract_text(file_path)
        print("本地提取文档失败，退级走普通上传流程: ", f'{file_name}')
        fake_id = f'{int(time.time() * 1000)}'
        self._extracted_texts[fake_id] = extracted_text
        self._extracted_filenames[fake_id] = file_name
        f'{file_name}'(", 长度: ", f'{len(extracted_text)}')
        return {"success": True, "error": None, "file_id": fake_id, "url": fake_id}
        self._extracted_filenames = {}
        self._extracted_texts = {}
        return {"success": "文件不存在: ", "error": f'{file_path}', "file_id": None, "url": None}
    __classcell__ = __class__
    return __class__
