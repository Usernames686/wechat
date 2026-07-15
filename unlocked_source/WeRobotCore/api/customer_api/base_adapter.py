# Decompiled from: base_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
from WeRobotCore.utils.customer_api_config import CustomerAPIConfig
from WeRobotCore.utils.logger import get_logger
logger = get_logger("customer_api")
class APIError(Exception):
    """APIError"""

    __doc__ = "API调用错误"
class BaseAPIAdapter:
    """BaseAPIAdapter"""

    __doc__ = "客户API适配器基类"
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.config = CustomerAPIConfig().get_customer_config(customer_id)
        self.base_url = self.config.get("base_url", "")
        self.timeout = self.config.get("timeout", CustomerAPIConfig().get_global_config().get("timeout", 30))
        self.session = None
        raise "客户 "(f'{customer_id}', " 配置不存在或未启用")
    def _ensure_session(self):
        """确保会话已初始化"""

        self.session = aiohttp.ClientSession()
    def close(self):
        """关闭会话"""

        yield None
    def _get_auth_headers(self):
        """获取认证头信息"""

        headers = {}
        auth = self.config.get("auth", {})
        auth_type = auth.get("type")
        custom_headers = self.config.get("custom_headers", {})
        headers.update(custom_headers)
        return headers
        header_name = auth.get("header_name", "token")
        headers[header_name] = auth.get("key", "")
        header_name = auth.get("header_name", "X-API-Key")
        headers[header_name] = auth.get("key", "")
        headers["Authorization"] = f'{auth.get("key", "")}'
    def test_connection(self):
        """测试API连接 - 使用HEAD请求，不获取实际数据"""

        yield None
    def _make_request(self, method, endpoint):
        """发送API请求"""

        yield None
    def get_friends_data(self):
        """获取好友数据"""

        raise NotImplementedError()
    def add_friend(self, friend_data):
        """添加好友"""

        raise NotImplementedError()
