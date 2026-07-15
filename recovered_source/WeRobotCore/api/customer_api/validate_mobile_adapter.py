# Decompiled from: validate_mobile_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Dict, Any, List, Optional
from WeRobotCore.utils.logger import get_logger
import time
logger = get_logger("validate_mobile")
class ValidateMobileAdapter(BaseAPIAdapter):
    """ValidateMobileAdapter"""

    __doc__ = "待验真号码API适配器实现"
    def get_friends_data(self, start_time):
        """获取待验真号码列表

                Args:
                    start_time: 开始时间戳（毫秒级），用于增量查询
                """

        endpoint = self.config.get("endpoints", {}).get("get_friends")
        headers = self._get_auth_headers()
        request_data = {}
        logger.info("首次查询，未提供startTime参数")
        yield None
        request_data["startTime"] = start_time
        logger.info("使用增量查询，startTime: ", f'{start_time}')
        raise APIError("当前客户未配置获取名单列表的端口")
    def add_friend(self, friend_data):
        """添加好友 - 此API不支持此操作"""

        raise APIError("待验真号码API不支持添加好友操作")
