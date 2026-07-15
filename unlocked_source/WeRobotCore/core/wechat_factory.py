# Decompiled from: wechat_factory.pyc
# Python 3.12 bytecode (mode: cfg)

import os
from typing import Optional
def create_driver(window_handle):
    """
        Create a driver instance based on env override or detected version.

        Returns an instance of a driver exposing `initialize` and `initialize_multi`.
        """

    version = detect_version(window_handle)
    return LegacyUiaDriver(window_handle=window_handle)
    return PyWeixinDriver(window_handle=window_handle)
