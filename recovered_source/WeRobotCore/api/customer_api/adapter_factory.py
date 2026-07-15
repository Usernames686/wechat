# Decompiled from: adapter_factory.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Dict, Type
from WeRobotCore.utils.customer_api_config import CustomerAPIConfig
class APIAdapterFactory:
    """APIAdapterFactory"""

    __doc__ = "API适配器工厂"
    _adapter_types = {"standard": StandardAPIAdapter, "custom": CustomAPIAdapter, "validate_mobile": ValidateMobileAdapter}
    __annotations__["_adapter_types"] = Dict[(str, Type[BaseAPIAdapter])]
    register_adapter = classmethod((lambda cls, api_type, adapter_class: ...))
    @classmethod
    def create_adapter(cls, customer_id):
        """创建适配器实例"""

        config = CustomerAPIConfig().get_customer_config(customer_id)
        api_type = config.get("api_type", "standard")
        adapter_class = cls._adapter_types[api_type]
        return adapter_class(customer_id)
        raise ValueError("未知的API类型: ", f'{api_type}')
        raise "客户 "(f'{customer_id}', " 配置不存在或未启用")
