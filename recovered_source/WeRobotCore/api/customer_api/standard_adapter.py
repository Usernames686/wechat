# Decompiled from: standard_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Dict, Any, List, Optional
class StandardAPIAdapter(BaseAPIAdapter):
    """StandardAPIAdapter"""

    __doc__ = "标准API适配器实现"
    def get_friends_data(self):
        """获取好友数据"""

        endpoint = self.config.get("endpoints", {}).get("get_friends")
        yield None
        raise APIError("未配置获取好友数据的端点")
    def add_friend(self, friend_data):
        """添加好友"""

        endpoint = self.config.get("endpoints", {}).get("add_friend")
        yield None
        raise APIError("未配置添加好友的端点")
