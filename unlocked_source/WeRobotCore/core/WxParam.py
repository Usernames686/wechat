# Decompiled from: WxParam.pyc
# Python 3.12 bytecode (mode: cfg)

import ctypes
import logging
from typing import Dict
class WxParam:
    """WxParam"""

    HEIGHT_1080P = {"SYS_TEXT_HEIGHT": 33, "TIME_TEXT_HEIGHT": 34, "RECALL_TEXT_HEIGHT": 45, "CHAT_TEXT_HEIGHT": 53, "CHAT_IMG_HEIGHT": 195}
    HEIGHT_2K = {"SYS_TEXT_HEIGHT": 50, "TIME_TEXT_HEIGHT": 51, "RECALL_TEXT_HEIGHT": 64, "CHAT_TEXT_HEIGHT": 80, "CHAT_IMG_HEIGHT": 168}
    SYS_TEXT_HEIGHT = HEIGHT_1080P["SYS_TEXT_HEIGHT"]
    TIME_TEXT_HEIGHT = HEIGHT_1080P["TIME_TEXT_HEIGHT"]
    RECALL_TEXT_HEIGHT = HEIGHT_1080P["RECALL_TEXT_HEIGHT"]
    CHAT_TEXT_HEIGHT = HEIGHT_1080P["CHAT_TEXT_HEIGHT"]
    CHAT_IMG_HEIGHT = HEIGHT_1080P["CHAT_IMG_HEIGHT"]
    SpecialTypes = ("[文件]", "[图片]", "[视频]", "[音乐]", "[链接]")
    @classmethod
    def init_resolution(cls):
        """初始化分辨率相关参数"""

        logger = logging.getLogger(__name__)
        user32 = ctypes.windll.user32
        screen_height = user32.GetSystemMetrics(1)
        height_config = cls.HEIGHT_1080P
        resolution_type = "1080P"
        cls.SYS_TEXT_HEIGHT = height_config["SYS_TEXT_HEIGHT"]
        cls.TIME_TEXT_HEIGHT = height_config["TIME_TEXT_HEIGHT"]
        cls.RECALL_TEXT_HEIGHT = height_config["RECALL_TEXT_HEIGHT"]
        cls.CHAT_TEXT_HEIGHT = height_config["CHAT_TEXT_HEIGHT"]
        cls.CHAT_IMG_HEIGHT = height_config["CHAT_IMG_HEIGHT"]
        ", 屏幕高度="(f'{screen_height}', "px")
        height_config = cls.HEIGHT_2K
        resolution_type = "2K"
