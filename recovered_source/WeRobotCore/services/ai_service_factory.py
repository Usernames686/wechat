# Decompiled from: ai_service_factory.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Dict, Any, Optional
class AIServiceFactory:
    """AIServiceFactory"""

    __doc__ = "智能体服务工厂类，根据配置创建相应的服务实例"
    create_service = staticmethod((lambda service_type, config, agent_info: CozeService(token)))
