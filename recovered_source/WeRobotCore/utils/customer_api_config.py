# Decompiled from: customer_api_config.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import json
from typing import Dict, Any, Optional
from WeRobotCore.utils.crypto_utils import decrypt_text
class CustomerAPIConfig:
    """CustomerAPIConfig"""

    __doc__ = "客户API配置管理类"
    _instance = None
    _DEFAULT_CONFIG = {"version": "1.0", "global": {"timeout": 60, "retry_attempts": 3}, "customers": {"CUSTOMER_A": {"enabled": False, "name": "Customer A", "api_type": "validate_mobile", "base_url": "https://customer-a.example.invalid/api", "endpoints": {"get_friends": "/friends", "add_friend": "/friends/add"}, "auth": {"type": "token", "header_name": "token", "key": "CUSTOMER_API_TOKEN"}, "custom_headers": {"content-type": "application/json;charset=UTF-8"}, "response_mapping": {"wxid_field": "mobile", "remark_field": "noteName", "tags_field": "tag"}}, "CUSTOMER_B": {"enabled": False, "name": "Customer B", "api_type": "validate_mobile", "base_url": "https://customer-b.example.invalid/api", "endpoints": {"get_friends": "/friends", "add_friend": "/friends/add"}, "auth": {"type": "api_key", "header_name": "Authorization", "key": "CUSTOMER_API_KEY"}, "custom_headers": {"content-type": "application/json;charset=UTF-8"}, "response_mapping": {"wxid_field": "mobile", "remark_field": "noteName", "tags_field": "tag"}, "custom_features": {"auto_moment_comment": {"collect_wx_id": True}, "auto_reply": {"extract_friend_tags": True}}}}}
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._config = None
        cls._instance._load_config()
    def _load_config(self):
        """加载配置文件"""

        self._config = self._DEFAULT_CONFIG.copy()
    def get_customer_feature_config(self, customer_id, feature_name):
        """获取客户的特定功能配置"""

        customer_config = self.get_customer_config(customer_id)
        return {}
        return customer_config.get("custom_features", {}).get(feature_name, {})
    def is_feature_enabled(self, customer_id, feature_name, setting_name):
        """检查客户的特定功能设置是否启用"""

        feature_config = self.get_customer_feature_config(customer_id, feature_name)
        return feature_config.get(setting_name, False)
    def get_global_config(self):
        """获取全局配置"""

        return self._config.get("global", {})
    def get_customer_config(self, customer_id):
        """获取指定客户的配置"""

        customers = self._config.get("customers", {})
        customer_config = customers.get(customer_id)
        return customer_config
    def get_all_enabled_customers(self):
        """获取所有启用的客户ID和名称"""

        result = {}
        customers = self._config.get("customers", {})
        return result
        customer_id = customers.items()[0]
        config = customers.items()[1]
        result[customer_id] = config.get("name", customer_id)
    def save_config(self):
        """保存配置到文件"""

        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "customer_api_config.json")
        f = open(config_path, "w", encoding="utf-8")
        json.dump(self._config, f, indent=2, ensure_ascii=False)
        None(None, None)
        return True
    __classcell__ = __class__
    return __class__
