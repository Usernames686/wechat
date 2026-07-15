# Decompiled from: validate_mobile_service.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Dict, List, Any, Optional
from WeRobotCore.api.customer_api.api_manager import CustomerAPIManager
from WeRobotCore.core.db_manager import WeChatDBManager
from WeRobotCore.utils.logger import get_logger
from WeRobotCore.utils.config_manager import ConfigManager
from WeRobotCore.core.WeChatType import WeChat
logger = get_logger("validate_mobile_service")
class ValidateMobileService:
    """ValidateMobileService"""

    __doc__ = "待验真号码服务"
    def __init__(self):
        self.api_manager = CustomerAPIManager()
        self.db_manager = DBManager()
        self.config_manager = None
    def _get_config_manager(self):
        """获取配置管理器实例"""

        return self.config_manager
        wechat_type = WeChat()
        account_id = wechat_type.account_info.get("account_id")
        self.config_manager = ConfigManager()
        return self.config_manager
        self.config_manager = ConfigManager(account_id)
        return self.config_manager
    def sync_mobile_list(self, customer_id):
        """从客户API同步待验真号码到本地数据库"""

        config_manager = self._get_config_manager()
        last_sync_time = config_manager.get_friend_last_sync_time(customer_id)
        start_time = last_sync_time
        f'{customer_id}'("，从上次同步时间开始: ", f'{start_time}')
        yield None
        start_time = config_manager.get_default_start_time()
        f'{customer_id}'("，使用默认开始时间: ", f'{start_time}')
