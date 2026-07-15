# Decompiled from: __init__.pyc
# Python 3.12 bytecode (mode: cfg)

"""
pyweixin 包（微信 4.x 自动化）

为避免在导入包时加载沉重依赖，本模块不再在顶层导入子模块。
如需使用具体模块，请显式导入：
    from .Uielements import SideBar, Lists, Edits
    from .WeChatAuto import Messages  # 需要 pyautogui
    from .WeChatTools import Tools    # 需要 pywinauto/pywin32
"""

__doc__ = "\npyweixin 包（微信 4.x 自动化）\n\n为避免在导入包时加载沉重依赖，本模块不再在顶层导入子模块。\n如需使用具体模块，请显式导入：\n    from .Uielements import SideBar, Lists, Edits\n    from .WeChatAuto import Messages  # 需要 pyautogui\n    from .WeChatTools import Tools    # 需要 pywinauto/pywin32\n"
__all__ = ["Uielements"]
