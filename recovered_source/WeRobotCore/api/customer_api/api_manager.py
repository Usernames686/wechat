# Decompiled from: api_manager.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Dict, Any, List, Optional
import asyncio
from WeRobotCore.utils.customer_api_config import CustomerAPIConfig
class CustomerAPIManager:
    """CustomerAPIManager"""

    __doc__ = "客户API管理器"
    _instance = None
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._adapters = {}
    def get_adapter(self, customer_id):
        """获取客户API适配器"""

        adapter = APIAdapterFactory.create_adapter(customer_id)
        self._adapters[customer_id] = adapter
        return adapter
        return self._adapters[customer_id]
    def close_all(self):
        """关闭所有适配器连接"""

        close_tasks = []
        self._adapters.clear()
        yield None
        adapter = _
        close_tasks.append(adapter.close())
    def get_friends_data(self, customer_id, start_time):
        """获取指定客户的好友数据

                Args:
                    customer_id: 客户ID
                    start_time: 开始时间戳（毫秒级），用于增量查询
                """

        yield None
    def add_friend(self, customer_id, friend_data):
        """通过指定客户的API添加好友"""

        yield None
    def get_available_customers(self):
        """获取所有可用的客户列表"""

        return CustomerAPIConfig().get_all_enabled_customers()
    __classcell__ = __class__
    return __class__
