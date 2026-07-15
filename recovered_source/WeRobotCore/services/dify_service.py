# Decompiled from: dify_service.pyc
# Python 3.12 bytecode (mode: cfg)

import json
import asyncio
import time
import requests
import os
from aiohttp import ClientSession, TCPConnector
from typing import Optional, Dict, Any, List
from datetime import datetime
class DifyService(AIServiceBase):
    """DifyService"""

    def __init__(self, token, base_url):
        super().__init__(token)
        self.base_url = base_url
        self.headers = {"Authorization": f'{token}', "Content-Type": "application/json"}
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
                使用Dify智能体生成评论
                """

        None(f'{50}', "...")
        request_data = {"query": "blocking", "response_mode": "user_", "user": f'{int(time.time() * 1000)}'}
        yield None
        request_data["inputs"] = {"user_name": user_name, "session_name": session_name, "session_id": session_id, "account_id": account_id}
    def start_chat(self, agent_id, message, session_id, user_name, session_name, account_id, cache_session, friend_tags):
        """启动一个完整的对话流程"""

        conversation_id = self._get_conversation_id(session_id)
        message_content = message
        files_list = []
        request_data = {"query": "blocking", "response_mode": "user_", "user": f'{int(time.time() * 1000)}'}
        print("Dify请求>>>>> ", f'{json.dumps(request_data, ensure_ascii=False, indent=2)}')
        yield None
        request_data["conversation_id"] = conversation_id
        request_data["files"] = files_list
        request_data["inputs"] = {"user_name": user_name, "session_name": session_name, "session_id": session_id, "account_id": account_id, "friend_tags": friend_tags}
        friend_tags = ""
        msg = reversed(message)
        message_content = msg.get("content", "")
        content_obj = json.loads(msg.get("content", ""))
        item = content_obj
        file_type = "document"
        type_mapping = {"image": "image", "audio": "audio", "video": "video", "file": "document"}
        file_type = type_mapping.get(item.get("type"), "document")
        files_list.append({"type": file_type, "transfer_method": "local_file", "upload_file_id": item.get("file_id")})
        message_content = item.get("text", "")
    def upload_file(self, file_path, user_id):
        """上传文件到Dify

                Args:
                    file_path: 文件路径
                    user_id: 用户标识，用于定义终端用户的身份，必须和发送消息接口传入user保持一致

                Returns:
                    Dict包含上传结果
                """

        import mimetypes
        mime_type = mimetypes.guess_type(file_path)[0]
        _ = mimetypes.guess_type(file_path)[1]
        file_ext = os.path.splitext(file_path)[1].lower()
        allowed_extensions = (".txt", ".pdf", ".doc", ".docx", ".csv", ".xls", ".xlsx", ".png", ".jpeg", ".jpg", ".gif", ".webp")
        f = open(file_path, "rb")
        files = {"file": (os.path.basename(file_path), f, mime_type)}
        data = {"user": user_id}
        response = requests.post(f'{self.base_url}', "/files/upload", headers={"Authorization": self.headers["Authorization"]}, files=files, data=data)
        None(None, None)
        data = response.json()
        print("Dify上传文件响应: ", f'{data}')
        error_msg = data.get("message", "未知错误")
        error_code = data.get("code", "unknown")
        " (代码: "(f'{error_code}', ")")
        return {"success": False, "error": error_msg, "code": error_code}
        print("Dify上传文件成功: ", f'{data.get("id")}')
        return {"success": True, "file_id": data.get("id"), "file_name": data.get("name"), "extension": data.get("extension"), "mime_type": data.get("mime_type"), "size": data.get("size")}
        user_id = f'{int(time.time() * 1000)}'
        return {"success": f'{file_ext}', "error": "。Dify目前只接受文档类文件。"}
    __classcell__ = __class__
    return __class__
