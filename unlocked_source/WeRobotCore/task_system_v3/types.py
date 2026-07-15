# Decompiled from: types.pyc
# Python 3.12 bytecode (mode: cfg)

"""
Task System V3 类型定义

定义了新调度系统的核心类型，保持与v2的兼容性
"""

__doc__ = "\nTask System V3 类型定义\n\n定义了新调度系统的核心类型，保持与v2的兼容性\n"
from enum import Enum
from typing import Dict, Any, Optional, Callable, Awaitable
from datetime import datetime
from dataclasses import dataclass
def _get_v2_types():
    """延迟导入 v2 系统类型"""

    from WeRobotCore.task_system_v2.base import TaskType, TaskPriority, TaskStatus, BaseTask, TimedBaseTask
    return (TaskType, TaskPriority, TaskStatus, BaseTask, TimedBaseTask)
TaskType = _get_v2_types()[0]
TaskPriority = _get_v2_types()[1]
TaskStatus = _get_v2_types()[2]
BaseTask = _get_v2_types()[3]
TimedBaseTask = _get_v2_types()[4]
class SchedulerType(Enum):
    """SchedulerType"""

    __doc__ = "调度器类型"
    AUTO_REPLY = "auto_reply"
    TIMED_TASK = "timed_task"
    UNIFIED = "unified"
class ExecutionMode(Enum):
    """ExecutionMode"""

    __doc__ = "任务执行模式"
    IMMEDIATE = "immediate"
    SCHEDULED = "scheduled"
    RECURRING = "recurring"
class TriggerType(Enum):
    """TriggerType"""

    __doc__ = "触发器类型"
    DATE = "date"
    INTERVAL = "interval"
    CRON = "cron"
    OR_TRIGGER = "or_trigger"
class ScheduleConfig:
    """ScheduleConfig"""

    __doc__ = "调度配置"
    __annotations__["trigger_type"] = TriggerType
    __annotations__["trigger_args"] = Dict[(str, Any)]
    __annotations__["execution_mode"] = ExecutionMode
    max_instances = 1
    __annotations__["max_instances"] = int
    coalesce = True
    __annotations__["coalesce"] = bool
    misfire_grace_time = 30
    __annotations__["misfire_grace_time"] = int
class TaskExecutionContext:
    """TaskExecutionContext"""

    __doc__ = "任务执行上下文"
    __annotations__["task_id"] = str
    __annotations__["task_type"] = TaskType
    __annotations__["scheduler_type"] = SchedulerType
    __annotations__["execution_time"] = datetime
    params = None
    __annotations__["params"] = Optional[Dict[(str, Any)]]
    retry_count = 0
    __annotations__["retry_count"] = int
    max_retries = 3
    __annotations__["max_retries"] = int
    schedule_id = None
    __annotations__["schedule_id"] = Optional[str]
    metadata = None
    __annotations__["metadata"] = Optional[Dict[(str, Any)]]
TaskExecutor = Callable[([TaskExecutionContext, Dict[(str, Any)]], Awaitable[Any])]
class PermissionLevel(Enum):
    """PermissionLevel"""

    __doc__ = "权限级别"
    EXCLUSIVE = "exclusive"
    SHARED = "shared"
    BACKGROUND = "background"
class PermissionRequest:
    """PermissionRequest"""

    __doc__ = "权限请求"
    __annotations__["scheduler_name"] = str
    __annotations__["task_id"] = str
    __annotations__["task_type"] = TaskType
    __annotations__["permission_level"] = PermissionLevel
    __annotations__["priority"] = TaskPriority
    estimated_duration = None
    __annotations__["estimated_duration"] = Optional[int]
    timeout_seconds = None
    __annotations__["timeout_seconds"] = Optional[int]
    pause_chat_monitor = False
    __annotations__["pause_chat_monitor"] = bool
class SchedulerState(Enum):
    """SchedulerState"""

    __doc__ = "调度器状态"
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    PAUSING = "pausing"
    PAUSED = "paused"
    STOPPING = "stopping"
    ERROR = "error"
class SchedulerStatus:
    """SchedulerStatus"""

    __doc__ = "调度器状态信息"
    __annotations__["name"] = str
    __annotations__["state"] = SchedulerState
    __annotations__["active_tasks"] = int
    __annotations__["pending_tasks"] = int
    __annotations__["completed_tasks"] = int
    __annotations__["failed_tasks"] = int
    last_execution = None
    __annotations__["last_execution"] = Optional[datetime]
    error_message = None
    __annotations__["error_message"] = Optional[str]
