# Decompiled from: add_friend_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

"""
自动添加好友任务适配器

负责处理自动添加好友任务的执行、调度和状态管理，
保持与V2系统的完全兼容性，同时支持V3的新特性。
"""

__doc__ = "\n自动添加好友任务适配器\n\n负责处理自动添加好友任务的执行、调度和状态管理，\n保持与V2系统的完全兼容性，同时支持V3的新特性。\n"
import asyncio
import random
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from WeRobotCore.utils.config_manager import ConfigManager
from WeRobotCore.utils.task_logger import TaskLogger
from WeRobotCore.utils.daily_counter import DailyCounter
from WeRobotCore.services.validate_mobile_service import ValidateMobileService
from WeRobotCore.utils.customer_api_config import CustomerAPIConfig
from WeRobotCore.utils.risk_control_manager import RiskControlManager, RiskControlType
class AddFriendAdapter:
    """AddFriendAdapter"""

    __doc__ = "自动添加好友任务适配器\n    \n    负责处理自动添加好友任务的执行、调度和状态管理\n    "
    def __init__(self, scheduler, permission_manager):
        """初始化适配器

                Args:
                    scheduler: 统一调度器实例
                    permission_manager: 权限管理器实例
                """

        self.scheduler = scheduler
        self.permission_manager = permission_manager
        self.wechat = WeChat()
        self.task_logger = TaskLogger()
        self.config_manager = ConfigManager()
        self.daily_counter = DailyCounter()
        self.risk_manager = None
        self._running = False
        self._paused = False
        self._executing = False
        self._multi_cycle_enabled = False
        self._selected_accounts = []
        self._last_index = -1
        self.scheduler.register_task_executor(TaskType.ADD_FRIEND, self.execute_task)
    def start(self):
        """启动适配器"""

        self._running = True
        self._paused = False
        print("AddFriendAdapter 启动成功")
        return True
        print("AddFriendAdapter 已运行，忽略重复启动")
        return True
    def stop(self):
        """停止适配器"""

        self._running = False
        self._paused = False
        self._last_index = -1
        self._selected_accounts = []
        WeChat.cleanup_invalid_instances()
        print("AddFriendAdapter 停止成功")
        return True
    def pause(self):
        """暂停适配器"""

        self._paused = True
        print("AddFriendAdapter 暂停成功")
        return True
    def resume(self):
        """恢复适配器"""

        self._paused = False
        print("AddFriendAdapter 恢复成功")
        return True
    def is_running(self):
        """检查适配器是否运行中"""

        return self._running
    def get_status(self):
        """获取适配器状态"""

        return {"running": self._running, "paused": self._paused, "active": self.is_running()}
    def execute_task(self, context, params):
        """执行自动添加好友任务

                Args:
                    context: 任务执行上下文
                    params: 任务参数（可选，如果未提供则使用context.params）

                Returns:
                    执行是否成功
                """

        print("AddFriendAdapter 未运行或已暂停")
        return False
        self._executing = True
        task_params = context.params
        today_count = self.daily_counter.get_today_count(self.wechat.get_user_id())
        max_friends = task_params.get("maxFriendsPerDay", 10)
        " 今日添加好友数量 "(f'{today_count}', " 人")
        self._multi_cycle_enabled = bool(task_params.get("multiCycleEnabled", False))
        from WeRobotCore.core.instance_manager_v2 import InstanceManagerV2
        _active = InstanceManagerV2().get_active_instance()
        self.wechat = WeChat()
        yield None
        print("添加好友：当前活动实例已退出托管，跳过任务")
        yield None
        incoming_accounts = task_params.get("accountIds")
        x = []
        from WeRobotCore.core.instance_manager_v2 import InstanceManagerV2
        _mgr = InstanceManagerV2()
        _exited = _mgr.list_instances()
        inst = set()
        valid_accounts = incoming_accounts
        a = []
        idx_base = self._selected_accounts
        next_index = (self._last_index + 1) % len(idx_base)
        chosen_id = idx_base[next_index]
        f'{self._selected_accounts}'(",当前执行账号：", f'{chosen_id}')
        self._last_index = next_index
        self.wechat = WeChat(account_id=chosen_id)
        self._selected_accounts = valid_accounts
        self._last_index = -1
        print("添加好友：所有选中账号已退出托管，跳过任务")
        yield None
        a = _
        inst = a
        inst.get("account_info").get("account_id")
        x = {}
        str(x)
        "当前微信账号 "(f'{self.wechat.get_user_id()}', " 处于加好友频繁风控中，暂停执行")
        yield None
        yield None
        print("当前时间在休息时间段内，暂停执行")
        yield None
        print("AddFriendAdapter 正在执行，跳过本次触发")
        return False
    def _is_rest_time(self):
        """检查当前时间是否在休息时间段内"""

        rest_config = self.config_manager.load_config("rest_time_settings")
        return False
        settings = rest_config["rest_time_settings"]
        selected_tasks = settings.get("selectedTasks", [])
        start_time = settings.get("startTime", 0)
        end_time = settings.get("endTime", 28)
        now = datetime.now()
        current_interval = now.hour * 4 + now.minute // 15
        return current_interval >= start_time
        return start_time <= current_interval
        return "???" <= end_time
        return False
    def _sync_external_api_friends(self):
        """同步外部API好友名单"""

        api_config = self.config_manager.load_config("external_api_settings")
        customer_id = api_config["identifier"]
        print("使用配置的客户标识符: ", f'{customer_id}')
        customer_config_manager = CustomerAPIConfig()
        customer_config = customer_config_manager.get_customer_config(customer_id)
        "客户标识符 '"(f'{customer_id}', "' 配置无效或已禁用")
        service = ValidateMobileService()
        yield None
    def _broadcast_status(self, task_id, status, error):
        """广播任务状态更新"""
    def add_task(self, params, schedule_time):
        """添加自动添加好友任务

                Args:
                    params: 任务参数
                    schedule_time: 调度时间（可选）

                Returns:
                    str: 任务ID
                """

        required_params = ("maxFriendsPerDay", "maxProcessPerTime", "checkInterval")
        check_interval = params.get("checkInterval", 10)
        schedule_config = ScheduleConfig(trigger_type=TriggerType.OR_TRIGGER, trigger_args={"immediate": True, "interval_minutes": check_interval}, execution_mode=ExecutionMode.RECURRING)
        yield None
        raise ValueError("缺少必要参数：", f'{required_params}')
    def get_adapter_status(self):
        """获取适配器状态

                Returns:
                    适配器状态信息
                """

        return {"adapter_type": "AddFriendAdapter", "running": self._running, "paused": self._paused, "wechat_connected": hasattr(self.wechat, "get_user_id")}
