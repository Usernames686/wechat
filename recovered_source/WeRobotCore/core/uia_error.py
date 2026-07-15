# Decompiled from: uia_error.pyc
# Python 3.12 bytecode (mode: cfg)

import win32gui
from typing import Optional, Tuple, Any
logger = UiaLogger().get_logger()
class WeChatUIAError(Exception):
    """WeChatUIAError"""

    __doc__ = "微信 UIA 操作异常基类"
    def __init__(self, message, original_error):
        super().__init__(message)
        self.original_error = original_error
    __classcell__ = __class__
    return __class__
class WeChatUIAConnectionError(WeChatUIAError):
    """WeChatUIAConnectionError"""

    __doc__ = "微信 UIA 连接断开异常"
    def __init__(self, message, original_error):
        super().__init__(message, original_error)
    __classcell__ = __class__
    return __class__
class WeChatWindowError(WeChatUIAError):
    """WeChatWindowError"""

    __doc__ = "微信窗口相关异常"
    def __init__(self, message, original_error):
        super().__init__(message, original_error)
    __classcell__ = __class__
    return __class__
def check_wechat_disconnected(wechat_instance):
    """
        检查微信是否断开连接

        Args:
            wechat_instance: WeChat实例

        Returns:
            tuple[bool, str]: (是否断开连接, 断开原因)
        """

    status = wechat_instance.check_connection_status()
    return (False, "")
    return (True, status.get("reason", "未知原因"))
def uia_error(e):
    """
        处理UIA异常，识别特定类型的错误并转换为对应的异常类

        Args:
            e: 原始异常

        Returns:
            Optional[WeChatUIAError]: 如果是已知的UIA异常则返回对应的异常对象，否则返回None
        """

    error_str = str(e)
    return WeChatUIAError("UIA异常: ", message=f'{str(e)}', original_error=e)
    return e
    alert_notifier = AlertNotifier(email_config)
    wx = WeChat()
    status = wx.check_connection_status()
    alert_notifier.check_error(e)
    return WeChatUIAConnectionError(original_error=e)
