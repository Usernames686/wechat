# Decompiled from: moment_comment_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

"""
朋友圈评论任务适配器 - Task System V3

这个适配器负责将 v2 的朋友圈评论任务适配到 v3 调度系统中，
保持原有的业务逻辑和功能完整性。
"""

__doc__ = "\n朋友圈评论任务适配器 - Task System V3\n\n这个适配器负责将 v2 的朋友圈评论任务适配到 v3 调度系统中，\n保持原有的业务逻辑和功能完整性。\n"
import asyncio
import importlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Type, List
from uuid import uuid4
from WeRobotCore.task_system_v3.types import TaskType, TaskPriority, TaskStatus, BaseTask, TimedBaseTask, ScheduleConfig, TriggerType, ExecutionMode, TaskExecutionContext, PermissionRequest, PermissionLevel
from WeRobotCore.task_system_v3.permission_manager import PermissionManager
from typing import TYPE_CHECKING
from WeRobotCore.utils.logger import task_logger, get_logger
class MomentCommentAdapter:
    """MomentCommentAdapter"""

    __doc__ = "朋友圈评论任务适配器\n    \n    负责处理朋友圈评论任务的执行、调度和状态管理，\n    确保与 v2 系统的完全兼容性。\n    "
    def __init__(self, scheduler, permission_manager):
        self.scheduler = scheduler
        self.permission_manager = permission_manager
        self.task_class_cache = {}
        self.logger = get_logger("moment_comment_adapter")
        self.task_logger = task_logger
        self._running = False
        self._paused = False
        self._multi_cycle_enabled = False
        self._selected_accounts = []
        self._cycle_cursor = 0
        self._active_tasks = {}
        self.scheduler.register_task_executor(TaskType.MOMENT_COMMENT, self._execute_moment_comment_task)
        self.scheduler.add_event_listener("task_cancelled", self._handle_task_cancelled)
    def start(self):
        """启动适配器"""

        self._running = True
        self._paused = False
        self.logger.info("朋友圈评论适配器启动成功")
        return True
        self.logger.info("朋友圈评论适配器已在运行")
        return True
    def add_moment_comment_task(self, task_params, schedule_time, schedule_config, task_id):
        """添加朋友圈评论任务

                Args:
                    task_params: 任务参数，包含评论配置
                    schedule_time: 调度时间，None表示立即执行
                    schedule_config: 调度配置，用于循环任务
                    task_id: 任务ID，None则自动生成

                Returns:
                    str: 任务ID
                """

        self._multi_cycle_enabled = bool(task_params.get("multiCycleEnabled", False))
        self._selected_accounts = list(task_params.get("selectedAccounts", []))
        self._cycle_cursor = 0
        execution_params = {"task_id": task_id, "task_params": task_params, "original_task_type": "moment_comment", "task_class_name": "MomentCommentTask"}
        schedule_config = ScheduleConfig(trigger_type=TriggerType.DATE, trigger_args={"run_time": schedule_time}, execution_mode=ExecutionMode.SCHEDULED)
        yield None
        yield None
        yield None
        interval_seconds = schedule_config.trigger_args.get("seconds", 60)
        start_time = schedule_config.trigger_args.get("start_time")
        or_trigger_config = ScheduleConfig(trigger_type=TriggerType.OR_TRIGGER, trigger_args={"immediate": True, "interval_seconds": interval_seconds, "start_time": start_time}, execution_mode=schedule_config.execution_mode, max_instances=schedule_config.max_instances)
        "将INTERVAL触发器转换为OR_TRIGGER以解决APScheduler 4.0立即执行问题，间隔: "(f'{interval_seconds}', "秒")
        yield None
        task_id = str(uuid4())
    def add_immediate_moment_comment_task(self, task_params, task_id):
        """添加立即执行的朋友圈评论任务

                Args:
                    task_params: 任务参数
                    task_id: 任务ID

                Returns:
                    str: 任务ID
                """

        self._multi_cycle_enabled = bool(task_params.get("multiCycleEnabled", False))
        self._selected_accounts = list(task_params.get("selectedAccounts", []))
        self._cycle_cursor = 0
        execution_params = {"task_id": task_id, "task_params": task_params, "original_task_type": "moment_comment", "task_class_name": "MomentCommentTask"}
        yield None
        task_id = str(uuid4())
    def add_immediate_and_recurring_moment_comment_task(self, task_params, interval_seconds, task_id):
        """添加立即执行且循环的朋友圈评论任务（使用OrTrigger解决APScheduler 4.0问题）

                Args:
                    task_params: 任务参数
                    interval_seconds: 循环间隔（秒）
                    task_id: 任务ID

                Returns:
                    str: 任务ID
                """

        execution_params = {"task_id": task_id, "task_params": task_params, "original_task_type": "moment_comment", "task_class_name": "MomentCommentTask"}
        or_trigger_config = ScheduleConfig(trigger_type=TriggerType.OR_TRIGGER, trigger_args={"immediate": True, "interval_seconds": interval_seconds, "start_time": None}, execution_mode=ExecutionMode.RECURRING, max_instances=1)
        "使用OrTrigger创建立即+循环朋友圈评论任务，间隔: "(f'{interval_seconds}', "秒")
        yield None
        task_id = str(uuid4())
    def _handle_task_cancelled(self, context):
        """处理任务取消事件"""

        task_id = context.task_id
        "[DEBUG] 任务 "(f'{task_id}', " 不在 MomentCommentAdapter 的 active_tasks 中")
        instance = self._active_tasks[task_id]
        self.logger.info("[DEBUG] 找到任务实例: ", f'{instance}')
        self.logger.info("通知活跃的朋友圈评论任务终止: ", f'{task_id}')
        instance.cancel()
        yield None
    def _execute_moment_comment_task(self, context, params):
        """执行朋友圈评论任务

                Args:
                    context: 任务执行上下文
                    params: 执行参数

                Returns:
                    Any: 执行结果
                """

        task_id = params.get("task_id", context.task_id)
        task_params = params.get("task_params", {})
        task_class_name = params.get("task_class_name", "MomentCommentTask")
        yield None
    def _get_moment_comment_task_class(self, class_name):
        """获取朋友圈评论任务类"""

        self.logger.debug("开始导入朋友圈评论任务类...")
        import sys
        import importlib.util as importlib
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        task_file_path = os.path.join(current_dir, "..", "..", "task_system_v2", "tasks", "moment_comment_task.py")
        task_file_path = os.path.normpath(task_file_path)
        self.logger.debug("尝试从文件加载任务类: ", f'{task_file_path}')
        self.logger.debug("回退到直接导入方式...")
        from WeRobotCore.task_system_v2.tasks.moment_comment_task import MomentCommentTask
        self.logger.debug("朋友圈评论任务类导入成功（回退方式）")
        return MomentCommentTask
        spec = importlib.util.spec_from_file_location("moment_comment_task", task_file_path)
        moment_comment_module = importlib.util.module_from_spec(spec)
        sys.modules["moment_comment_task"] = moment_comment_module
        spec.loader.exec_module(moment_comment_module)
        MomentCommentTask = getattr(moment_comment_module, class_name)
        self.logger.debug("朋友圈评论任务类导入成功（文件方式）")
        return MomentCommentTask
    def _execute_task_safely(self, task_instance):
        """安全执行任务实例

                Args:
                    task_instance: 任务实例

                Returns:
                    Any: 执行结果
                """

        raise AttributeError("任务实例没有execute方法")
        loop = asyncio.get_event_loop()
        yield None
        yield None
    def _get_task_priority(self, task_params):
        """获取任务优先级

                Args:
                    task_params: 任务参数

                Returns:
                    TaskPriority: 任务优先级
                """

        priority_str = task_params.get("priority", "normal")
        priority_mapping = {"low": TaskPriority.LOW, "normal": TaskPriority.MEDIUM, "medium": TaskPriority.MEDIUM, "high": TaskPriority.HIGH}
        return priority_mapping.get(priority_str.lower(), TaskPriority.MEDIUM)
    def cancel_task(self, task_id):
        """取消朋友圈评论任务

                Args:
                    task_id: 任务ID

                Returns:
                    bool: 取消是否成功
                """

        yield None
    def get_task_status(self, task_id):
        """获取朋友圈评论任务状态

                Args:
                    task_id: 任务ID

                Returns:
                    Optional[Dict]: 任务状态信息
                """

        yield None
    def get_all_tasks(self):
        """获取所有朋友圈评论任务

                Returns:
                    List[Dict]: 任务列表
                """

        yield None
    def replace_recurring_task(self, task_params, schedule_time, schedule_config, task_id):
        """替换现有的循环朋友圈评论任务

                Args:
                    task_params: 任务参数
                    schedule_time: 调度时间
                    schedule_config: 调度配置
                    task_id: 任务ID

                Returns:
                    str: 任务ID
                """

        execution_params = {"task_id": task_id, "task_params": task_params, "original_task_type": "moment_comment", "task_class_name": "MomentCommentTask"}
        yield None
        interval_seconds = task_params.get("interval_seconds", 60)
        schedule_config = ScheduleConfig(trigger_type=TriggerType.OR_TRIGGER, trigger_args={"immediate": True, "interval_seconds": interval_seconds, "start_time": None}, execution_mode=ExecutionMode.RECURRING, max_instances=1)
        task_id = "moment_comment_recurring"
from WeRobotCore.task_system_v3.unified_scheduler import UnifiedScheduler
