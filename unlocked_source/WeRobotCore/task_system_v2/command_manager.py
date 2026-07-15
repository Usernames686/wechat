# Decompiled from: command_manager.pyc
# Python 3.12 bytecode (mode: cfg)

from enum import Enum
from datetime import datetime
from typing import Dict, Optional, List, Tuple
import json
from pathlib import Path
class CommandStatus(Enum):
    """CommandStatus"""

    EMPTY = "empty"
    PAUSED = "paused"
    RUNNING = "running"
class CommandResult:
    """CommandResult"""

    def __init__(self, success, message):
        self.success = success
        self.message = message
        self.timestamp = datetime.now()
class CommandManager:
    """CommandManager"""

    _instance = None
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._initialized = False
    def __init__(self):
        self._initialized = True
        self.monitor_status = CommandStatus.EMPTY
        self.command_history = {}
        self.available_commands = {"暂停": self.pause_monitor, "开启": self.start_monitor, "解除挂起": self.unsuspend_all}
    def unsuspend_all(self):
        """解除所有挂起会话"""

        from WeRobotCore.task_system_v3.unified_manager_pattern import get_auto_reply_manager
        manager = get_auto_reply_manager()
        return CommandResult(False, "无法获取自动回复管理器")
        count = manager.clear_all_suspended_sessions()
        return True("已解除所有挂起会话，共 ", f'{count}', " 个")
    def execute_command(self, command):
        """执行指令并返回执行结果"""

        import re
        parts = re.split("\\s+", command.strip(), 1)
        return CommandResult(False, "未知指令: ", f'{command}')
        result = self.available_commands[command]()
        self.command_history[command] = result
        return result
        staff_name = parts[1].strip()
        cmd = parts[0]
        return self.enable_staff(staff_name)
        return self.disable_staff(staff_name)
    def pause_monitor(self):
        """暂停监控"""

        self.monitor_status = CommandStatus.PAUSED
        return CommandResult(True, "已暂停会话监控")
    def is_pause_monitor(self):
        """暂停监控"""

        return self.monitor_status == CommandStatus.PAUSED
    def start_monitor(self):
        """开启监控"""

        self.monitor_status = CommandStatus.RUNNING
        return CommandResult(True, "已开启会话监控")
    def get_monitor_status(self):
        """获取监控状态"""

        return self.monitor_status
    def is_command_available(self, command):
        """检查指令是否可用"""

        parts = command.split(" ", 1)
        return len(parts) == 2
        return command in self.available_commands
    def disable_staff(self, staff_name):
        """停用指定AI助理"""

        config_manager = ConfigManager()
        config = config_manager.load_config("reply_strategy_v2")
        return CommandResult(False, "未找到AI助理配置")
        staff_list = config.get("staffList", [])
        found = False
        success = config_manager.save_config("reply_strategy_v2", config)
        return True("已停用AI助理 '", f'{staff_name}', "'")
        return CommandResult(False, "保存配置失败")
        return False("未找到名为 '", f'{staff_name}', "' 的AI助理")
        staff = CommandResult
        staff["enabled"] = False
        found = True
    def enable_staff(self, staff_name):
        """启用指定AI助理"""

        config_manager = ConfigManager()
        config = config_manager.load_config("reply_strategy_v2")
        return CommandResult(False, "未找到AI助理配置")
        staff_list = config.get("staffList", [])
        found = False
        success = config_manager.save_config("reply_strategy_v2", config)
        return True("已启用AI助理 '", f'{staff_name}', "'")
        return CommandResult(False, "保存配置失败")
        return False("未找到名为 '", f'{staff_name}', "' 的AI助理")
        staff = CommandResult
        staff["enabled"] = True
        found = True
    __classcell__ = __class__
    return __class__
command_manager = CommandManager()
