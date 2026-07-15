# Decompiled from: friend_request_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

"""
自动通过好友任务适配器

负责处理自动通过好友任务的执行、调度和状态管理，
保持与V2系统的完全兼容性，同时支持V3的新特性。
"""

__doc__ = "\n自动通过好友任务适配器\n\n负责处理自动通过好友任务的执行、调度和状态管理，\n保持与V2系统的完全兼容性，同时支持V3的新特性。\n"
import asyncio
import random
from datetime import datetime
from typing import Dict, Any, Optional, List
from WeRobotCore.utils.config_manager import ConfigManager
from WeRobotCore.utils.greeting_manager import GreetingManager
from WeRobotCore.utils.task_logger import TaskLogger
class FriendRequestAdapter:
    """FriendRequestAdapter"""

    __doc__ = "自动通过好友任务适配器\n    \n    负责处理自动通过好友任务的执行、调度和状态管理\n    "
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
        self._running = False
        self._paused = False
        self._multi_cycle_enabled = False
        self._selected_accounts = []
        self._last_index = -1
        self.scheduler.register_task_executor(TaskType.FRIEND_REQUEST, self.execute_task)
    def start(self):
        """启动适配器"""

        self._running = True
        self._paused = False
        return True
    def stop(self):
        """停止适配器"""

        self._running = False
        print("FriendRequestAdapter 停止成功")
        return True
    def pause(self):
        """暂停适配器"""

        self._paused = True
        print("FriendRequestAdapter 暂停成功")
        return True
    def resume(self):
        """恢复适配器"""

        self._paused = False
        print("FriendRequestAdapter 恢复成功")
        return True
    def is_running(self):
        """检查适配器是否运行中"""

        return self._running
    def get_status(self):
        """获取适配器状态"""

        return {"running": self._running, "paused": self._paused, "active": self.is_running()}
    def _is_rest_time(self):
        """检查当前时间是否在休息时间段内

                Returns:
                    bool: True表示在休息时间内，False表示可以执行
                """

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
    def execute_task(self, context, params):
        """执行自动通过好友任务

                Args:
                    context: 任务执行上下文
                    params: 任务参数

                Returns:
                    Any: 任务执行结果
                """

        print("开始执行自动通过好友任务，任务ID: ", f'{context.task_id}')
        print("任务参数: ", f'{params}')
        max_process = params.get("maxProcessPerTime", 5)
        tag = params.get("tag")
        greeting_group_id = params.get("greetingGroupId")
        target_group = params.get("targetGroup")
        self._multi_cycle_enabled = bool(params.get("multiCycleEnabled", False))
        from WeRobotCore.core.instance_manager_v2 import InstanceManagerV2
        _active = InstanceManagerV2().get_active_instance()
        self.wechat = WeChat()
        yield None
        print("自动通过好友：当前活动实例已退出托管，跳过任务")
        return {"success": False, "message": "当前活动实例已退出托管", "processed_count": 0}
        incoming_accounts = params.get("accountIds")
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
        print("自动通过好友：所有选中账号已退出托管，跳过任务")
        return {"success": False, "message": "所有账号已退出托管", "processed_count": 0}
        a = "自动通过好友：多账号循环模式已启用，选中账号："
        inst = a
        inst.get("account_info").get("account_id")
        x = {}
        str(x)
        print("当前时间在休息时间段内，暂停执行")
        return {"success": False, "message": "当前时间在休息时间段内，暂停执行", "processed_count": 0}
        raise Exception("FriendRequestAdapter 未运行或已暂停")
    def _send_greeting_messages(self, processed_users, greeting_group_id):
        """发送打招呼消息

                Args:
                    processed_users: 已处理的用户列表
                    greeting_group_id: 话术组ID
                """

        greeting_manager = GreetingManager(self.config_manager)
        print("开始向新添加的好友发送打招呼消息...")
        user = processed_users
        yield None
    def _invite_to_group(self, processed_users, target_group):
        """邀请用户加入群组

                Args:
                    processed_users: 已处理的用户列表
                    target_group: 目标群组
                """

        print("开始处理自动拉群：", f'{processed_users}')
        import threading
        current_loop = asyncio.get_running_loop()
        future = current_loop.create_future()
        def worker():
            res = self.wechat.invite_friends_to_group(processed_users, target_group)
            current_loop.call_soon_threadsafe(future.set_result, res)
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        yield None
    def _broadcast_status(self, task_id, status, params, progress, total, error):
        """广播任务状态更新

                Args:
                    task_id: 任务ID
                    status: 任务状态
                    params: 任务参数
                    progress: 进度
                    total: 总数
                    error: 错误信息
                """

        yield None
    def _save_task_log(self, task_id, status, processed_count, tag, processed_users, greeting_group_id, target_group):
        """保存任务日志

                Args:
                    task_id: 任务ID
                    status: 任务状态
                    processed_count: 处理数量
                    tag: 标签
                    processed_users: 处理的用户列表
                    greeting_group_id: 话术组ID
                    target_group: 目标群组
                """

        account_id = ""
        account_id = self.wechat.account_info["account_id"]
        details = {"processed_users": processed_users, "tag": tag, "greeting_group_id": greeting_group_id, "target_group": target_group}
        self.task_logger.add_friend_request_log(task_id=task_id, status=status.value, processed_count=processed_count, tag=tag, error=None)
        self.task_logger.add_friend_request_action_log(account_id=account_id, task_id=task_id, status=status.value, details=details, error_msg=None)
    def add_task(self, params, schedule_time):
        """添加自动通过好友任务

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
    def replace_recurring_task(self, params, schedule_time):
        """替换现有的循环好友请求任务

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
