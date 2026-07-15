# Decompiled from: unified_scheduler.pyc
# Python 3.12 bytecode (mode: cfg)

"""
统一调度器 - 基于APScheduler 4.0的核心调度组件

这个调度器作为整个task_system_v3的核心，负责：
1. 封装APScheduler 4.0的复杂性
2. 提供与v2系统兼容的接口
3. 管理任务的生命周期
4. 协调权限管理和任务执行
"""

__doc__ = "\n统一调度器 - 基于APScheduler 4.0的核心调度组件\n\n这个调度器作为整个task_system_v3的核心，负责：\n1. 封装APScheduler 4.0的复杂性\n2. 提供与v2系统兼容的接口\n3. 管理任务的生命周期\n4. 协调权限管理和任务执行\n"
import asyncio
import uuid
import json
import pickle
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable, Awaitable
from pathlib import Path
from apscheduler import AsyncScheduler, CoalescePolicy, TaskDefaults, ConflictPolicy
from apscheduler import JobAdded, JobRemoved, JobAcquired, JobReleased, JobCancelled, JobDeadlineMissed, SchedulerStarted, SchedulerStopped, TaskAdded, TaskRemoved
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger
from apscheduler.datastores.sqlalchemy import SQLAlchemyDataStore
from apscheduler.eventbrokers.local import LocalEventBroker
from WeRobotCore.task_system_v3.types import TaskType, TaskStatus, SchedulerType, ExecutionMode, TriggerType, ScheduleConfig, TaskExecutionContext, PermissionLevel, PermissionRequest, SchedulerState, SchedulerStatus
from WeRobotCore.utils.logger import task_logger, get_logger
def execute_scheduled_task(task_id, task_type_str, params):
    """全局任务执行函数，用于APScheduler调度（异步版本）
        加固：捕获 BaseException，避免异常泄漏至 APScheduler 导致作业被标记为 aborted。
        """

    from WeRobotCore.task_system_v3.unified_manager_pattern import get_scheduler
    import logging
    import asyncio
    logger = logging.getLogger("execute_scheduled_task")
    f'{task_id}'(", 类型: ", f'{task_type_str}')
    scheduler_instance = get_scheduler()
    logger.info("[DEBUG] 开始执行任务: ", f'{task_id}')
    yield None
    logger.warning("[DEBUG] 无法获取调度器实例")
class UnifiedScheduler:
    """UnifiedScheduler"""

    __doc__ = "统一调度器 - APScheduler 4.0的封装"
    def __init__(self):
        self.logger = get_logger("unified_scheduler")
        self.task_logger = task_logger
        self._state = SchedulerState.STOPPED
        self._scheduler = None
        self._permission_manager = None
        self._startup_guard_active = False
        self._active_tasks = {}
        self._task_executors = {}
        self._task_statistics = {"completed": 0, "failed": 0, "cancelled": 0}
        self._schedule_metadata = {}
        self._event_callbacks = {"task_started": [], "task_completed": [], "task_failed": [], "task_cancelled": [], "task_finalized": []}
        self._finalization_pending = {}
        self._apscheduler_available = AsyncScheduler is not None
        self._fallback_mode = not self._apscheduler_available
        self.logger.warning("APScheduler 4.0不可用，使用简单的内存调度器")
        self._fallback_tasks = {}
        self._fallback_timer_task = None
        self.logger.debug("APScheduler 4.0已导入，启用异步调度模式")
    def _generate_standard_task_id(self, task_type, execution_mode, custom_suffix):
        """生成标准化的任务ID

                Args:
                    task_type: 任务类型
                    execution_mode: 执行模式
                    custom_suffix: 自定义后缀（可选）

                Returns:
                    str: 标准化的任务ID
                """

        task_type_str = task_type.value.lower()
        return f'{8}'
        return f'{8}'
        return "_recurring"
        return f'{custom_suffix}'
    def _normalize_task_type_string(self, task_type):
        """将TaskType枚举标准化为小写字符串

                Args:
                    task_type: 任务类型枚举

                Returns:
                    str: 标准化的任务类型字符串
                """

        return task_type.value.lower()
    def initialize(self, db_path, permission_manager, auto_resume_tasks):
        """初始化调度器"""

        self._state = SchedulerState.STARTING
        self._permission_manager = permission_manager
        self._auto_resume_tasks = auto_resume_tasks
        self._auto_resume_task_types = set()
        yield None
        return False
    def _initialize_apscheduler(self, db_path, use_memory_db):
        """初始化APScheduler"""

        from sqlalchemy import create_engine, event
        from sqlalchemy.pool import StaticPool, QueuePool
        self._db_path = str(db_path)
        engine = create_engine("sqlite:///", f'{db_path}', poolclass=QueuePool, pool_size=10, max_overflow=20, pool_timeout=30, pool_pre_ping=True, pool_recycle=3600, connect_args={"check_same_thread": False, "timeout": 30, "isolation_level": None}, echo=False)
        data_store = SQLAlchemyDataStore(engine)
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.execute("PRAGMA busy_timeout=30000")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA cache_size=10000")
            cursor.execute("PRAGMA temp_store=MEMORY")
            cursor.close()
        event_broker = LocalEventBroker()
        self._scheduler = AsyncScheduler(data_store=data_store, event_broker=event_broker, identity="unified_scheduler", max_concurrent_jobs=50, logger=self.logger)
        yield None
        from WeRobotCore.utils.data_manager import DataManager
        db_path = os.path.join(DataManager.get_data_dir_str(), "scheduler_v3.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._db_path = str(db_path)
        engine = create_engine("sqlite:///", f'{db_path}', poolclass=QueuePool, pool_size=10, max_overflow=20, pool_timeout=30, pool_pre_ping=True, pool_recycle=3600, connect_args={"check_same_thread": False, "timeout": 30, "isolation_level": None}, echo=False)
        data_store = SQLAlchemyDataStore(engine)
        self._db_path = None
        engine = create_engine("sqlite:///:memory:", poolclass=StaticPool, connect_args={"check_same_thread": False, "timeout": 30, "isolation_level": None}, echo=False)
        data_store = SQLAlchemyDataStore(engine)
        self.logger.info("使用内存数据库")
    def _ensure_serializable(self, params):
        """确保参数可序列化"""

        json.dumps(params, default=str)
        return params
    def register_task_executor(self, task_type, executor):
        """注册任务执行器"""

        self._task_executors[task_type] = executor
    def register_auto_resume_task_type(self, task_type):
        """注册自动恢复任务类型

                Args:
                    task_type: 任务类型字符串，如 "auto_follow"
                """

        self._auto_resume_task_types.add(task_type)
        self.logger.info("注册持久化任务: ", f'{task_type}')
        self._auto_resume_task_types = set()
    def _ensure_scheduler_running(self):
        """确保调度器处于可运行状态，必要时尝试重启"""

        self.logger.warning("调度器状态异常，尝试重启...")
        yield None
    def process_existing_tasks(self):
        """处理已存在的持久化任务

                这个方法应该在所有adapter注册完成后调用，以确保自动恢复任务类型已经正确注册
                """

        yield None
        self.logger.warning("调度器未运行，无法处理已存在的任务")
    def _get_default_priority(self, task_type):
        """获取任务类型的默认优先级

                数值越大优先级越高
                """

        return 2
        return 1
        return 5
        return 10
    def add_immediate_task(self, task_type, params, task_id):
        """添加立即执行的任务"""

        yield None
    def replace_recurring_task(self, task_type, params, schedule_config, task_id):
        """替换现有的循环任务

                Args:
                    task_type: 任务类型
                    params: 新的任务参数
                    schedule_config: 新的调度配置
                    task_id: 任务ID（可选）

                Returns:
                    str: 新任务ID
                """

        yield None
    def add_task(self, task_id, func, run_time):
        """添加任务的通用方法，兼容旧接口"""

        params = {"func": func}
        yield None
        yield None
    def _check_existing_recurring_task(self, task_type):
        """检查是否已存在相同类型的循环任务

                Args:
                    task_type: 任务类型

                Returns:
                    Optional[str]: 如果存在返回任务ID，否则返回None
                """

        yield None
    def add_scheduled_task(self, task_type, params, schedule_config, task_id, allow_duplicate):
        """添加定时任务

                Args:
                    task_type: 任务类型
                    params: 任务参数
                    schedule_config: 调度配置
                    task_id: 任务ID（可选）
                    allow_duplicate: 是否允许重复的循环任务（默认False）

                Returns:
                    str: 任务ID
                """

        yield None
    def pause_task(self, task_id):
        """暂停任务

                Args:
                    task_id: 任务ID

                Returns:
                    bool: 是否成功
                """

        yield None
    def resume_task(self, task_id):
        """恢复任务

                Args:
                    task_id: 任务ID

                Returns:
                    bool: 是否成功
                """

        yield None
    def _optimize_schedule_config(self, task_type, schedule_config):
        """根据任务类型优化调度配置参数

                Args:
                    task_type: 任务类型
                    schedule_config: 原始调度配置

                Returns:
                    ScheduleConfig: 优化后的调度配置
                """

        optimized_config = ScheduleConfig(trigger_type=schedule_config.trigger_type, trigger_args=schedule_config.trigger_args.copy(), execution_mode=schedule_config.execution_mode, misfire_grace_time=schedule_config.misfire_grace_time, coalesce=schedule_config.coalesce)
        f'{optimized_config.misfire_grace_time}'(", coalesce=", f'{optimized_config.coalesce}')
        return optimized_config
        optimized_config.coalesce = True
        optimized_config.misfire_grace_time = timedelta(minutes=30)
        optimized_config.coalesce = True
        optimized_config.misfire_grace_time = timedelta(minutes=45)
        optimized_config.coalesce = True
        optimized_config.misfire_grace_time = timedelta(minutes=45)
        optimized_config.coalesce = False
        optimized_config.misfire_grace_time = timedelta(minutes=45)
        optimized_config.coalesce = True
        optimized_config.misfire_grace_time = timedelta(hours=1)
        optimized_config.coalesce = True
        optimized_config.misfire_grace_time = timedelta(hours=2)
    def _add_fallback_task(self, task_id, task_type, params, immediate):
        """添加回退模式任务"""

        next_run_time = datetime.now() + timedelta(seconds=1)
        self._fallback_tasks[task_id] = {"task_type": task_type.value, "params": params, "next_run_time": next_run_time, "is_recurring": False}
        return task_id
    def _add_fallback_scheduled_task(self, task_id, task_type, params, schedule_config):
        """添加回退模式的定时任务"""

        next_run_time = datetime.now() + timedelta(minutes=1)
        self._fallback_tasks[task_id] = {"task_type": task_type.value, "params": params, "next_run_time": next_run_time, "is_recurring": schedule_config.execution_mode == ExecutionMode.RECURRING, "interval_seconds": schedule_config.trigger_args.get("seconds", 60)}
        return task_id
        interval = schedule_config.trigger_args.get("seconds", 60)
        next_run_time = datetime.now() + timedelta(seconds=interval)
        next_run_time = schedule_config.trigger_args.get("run_time", datetime.now())
    def _create_trigger(self, config):
        """根据配置创建APScheduler触发器"""

        raise ValueError("不支持的触发器类型: ", f'{config.trigger_type}')
        from datetime import timezone
        cron_list = config.trigger_args.get("cron_list")
        immediate = config.trigger_args.get("immediate", True)
        interval_seconds = config.trigger_args.get("interval_seconds")
        interval_minutes = config.trigger_args.get("interval_minutes")
        start_time = config.trigger_args.get("start_time")
        triggers = []
        triggers.append(IntervalTrigger(seconds=interval_seconds, start_time=start_time))
        return OrTrigger(triggers)
        triggers.append(DateTrigger(run_time=start_time))
        start_time = start_time.replace(tzinfo=timezone.utc)
        start_time = datetime.now(timezone.utc)
        interval_seconds = interval_minutes * 60
        interval_seconds = 60
        triggers = []
        return OrTrigger(triggers)
        item = cron_list
        args = {}
        hour = item.get("hour")
        minute = item.get("minute")
        day_of_week = item.get("day_of_week")
        triggers.append(CronTrigger(*(), **{**{}, **args}))
        args["day_of_week"] = day_of_week
        args["minute"] = minute
        args["hour"] = hour
        return CronTrigger(*(), **{**{}, **config.trigger_args})
        return IntervalTrigger(*(), **{**{}, **config.trigger_args})
        return DateTrigger(*(), **{**{}, **config.trigger_args})
    def _execute_task(self, task_id, task_type_str, params):
        """执行任务的统一入口"""

        f'{task_id}'(", 类型: ", f'{task_type_str}')
        task_type = TaskType[task_type_str]
        schedule_id = params.get("schedule_id", task_id)
        metadata = None
        latest_meta = self._schedule_metadata.get(schedule_id)
        metadata = params.get("metadata", {})
        context = TaskExecutionContext(task_id=task_id, task_type=task_type, scheduler_type=SchedulerType.UNIFIED, execution_time=datetime.now(), schedule_id=schedule_id, metadata=metadata, params=params)
        self._active_tasks[task_id] = context
        permission_granted = False
        executor = self._task_executors.get(task_type)
        yield None
        raise "未找到任务类型 "(f'{task_type}', " 的执行器")
        timeout_map = {TaskType.ADD_FRIEND: 7200, TaskType.FRIEND_REQUEST: 3600, TaskType.MOMENT_COMMENT: 3600, TaskType.MASS_SENDING: 3600, TaskType.AUTO_REPLY: 3600, TaskType.AUTO_FOLLOW: 7200}
        timeout_seconds = timeout_map.get(task_type, 3600)
        permission_request = PermissionRequest(scheduler_name="unified_scheduler", task_id=task_id, task_type=task_type, permission_level=PermissionLevel.EXCLUSIVE, priority=params.get("priority", 2), timeout_seconds=timeout_seconds, estimated_duration=params.get("estimated_duration", timeout_seconds // 2), pause_chat_monitor=task_type in (TaskType.MOMENT_COMMENT, TaskType.ADD_FRIEND, TaskType.FRIEND_REQUEST))
        yield None
        metadata = latest_meta
        yield None
        task_type_name = task_type_str.split(".", 1)[1]
        task_type = TaskType[task_type_name]
    def cancel_task(self, task_id):
        """取消任务"""

        import time as _t
        _c0 = _t.time()
        self.logger.info("[DEBUG] 开始取消任务 cancel_task: ", f'{task_id}')
        yield None
        yield None
    def get_task_info(self, task_id):
        """获取任务信息"""

        task_data = self._fallback_tasks[task_id]
        return {"id": task_id, "type": task_data["task_type"], "status": "pending", "next_run_time": task_data["next_run_time"].isoformat()}
        context = self._active_tasks[task_id]
        status = "running"
        return {"id": task_id, "type": context.task_type.value, "status": status, "execution_time": context.execution_time.isoformat(), "params": getattr(context, "params", None)}
        current_holder = self._permission_manager.get_current_holder()
        status = "pending"
    def get_all_tasks(self):
        """获取所有任务信息"""

        all_tasks = []
        current_holder = None
        return all_tasks
        task_id = self._fallback_tasks.items()[0]
        task_data = self._fallback_tasks.items()[1]
        all_tasks.append({"id": task_id, "type": task_data["task_type"], "status": "pending", "next_run_time": task_data["next_run_time"].isoformat(), "params": task_data.get("params", {})})
        yield None
        task_id = _[0]
        context = _[1]
        status = "running"
        all_tasks.append({"id": task_id, "type": context.task_type.value, "status": status, "execution_time": context.execution_time.isoformat(), "params": getattr(context, "params", None)})
        self._scheduler.get_schedules()
        status = "pending"
        current_holder = self._permission_manager.get_current_holder()
    def get_schedules(self):
        """获取所有调度任务（兼容性方法）"""

        return []
        yield None
    def get_schedule(self, schedule_id):
        """获取单个调度任务（兼容性方法）"""

        yield None
    def add_schedule(self, func, trigger, id, args, kwargs, start_date, end_date, metadata):
        """添加调度任务（兼容性方法）"""

        self.logger.warning("Fallback 模式下不支持 add_schedule")
        raise NotImplementedError("Fallback 模式下不支持 add_schedule")
        schedule_kwargs = {"id": id}
        yield None
        schedule_kwargs["metadata"] = metadata
        schedule_kwargs["end_date"] = end_date
        schedule_kwargs["start_date"] = start_date
        schedule_kwargs["kwargs"] = kwargs
        schedule_kwargs["args"] = args
        id = str(uuid.uuid4())
    def modify_schedule(self, schedule_id):
        """修改调度任务"""

        self.logger.warning("Fallback 模式下不支持 modify_schedule")
        raise NotImplementedError("Fallback 模式下不支持 modify_schedule")
        yield None
    def update_task_metadata(self, schedule_id, metadata):
        """更新任务元数据"""

        yield None
    def pause_schedule(self, schedule_id):
        """暂停调度任务"""

        self.logger.warning("Fallback 模式下不支持 pause_schedule")
        raise NotImplementedError("Fallback 模式下不支持 pause_schedule")
        yield None
    def unpause_schedule(self, schedule_id):
        """恢复调度任务"""

        self.logger.warning("Fallback 模式下不支持 unpause_schedule")
        raise NotImplementedError("Fallback 模式下不支持 unpause_schedule")
        yield None
    def remove_schedule(self, schedule_id):
        """删除调度任务"""

        self.logger.warning("Fallback 模式下不支持 remove_schedule")
        raise NotImplementedError("Fallback 模式下不支持 remove_schedule")
        metadata_before = self._schedule_metadata.get(schedule_id)
        yield None
    def get_status(self):
        """获取调度器状态"""

        return SchedulerStatus(name="unified_scheduler", state=self._state, active_tasks=len(self._active_tasks), pending_tasks=0, completed_tasks=self._task_statistics["completed"], failed_tasks=self._task_statistics["failed"])
    def add_event_listener(self, event_type, callback):
        """添加事件监听器"""

        self._event_callbacks[event_type].append(callback)
    def _trigger_event(self, event_type):
        """触发事件"""

        callback = self._event_callbacks.get(event_type, [])
        callback(*args)
        yield None
    def _try_finalize(self, task_id):
        """合并并发布统一终态事件"""

        pending = self._finalization_pending.get(task_id)
        status = pending.get("status")
        removed = pending.get("removed", False)
        yield None
    def _emit_task_finalized(self, task_id, pending):
        """构造并发布 task_finalized 事件载荷"""

        context = pending.get("context")
        metadata = pending.get("metadata")
        task_type = None
        params = {}
        mode = None
        payload = {"task_id": task_id, "task_type": task_type, "status": pending.get("status", "unknown"), "result": pending.get("result"), "error": pending.get("error"), "removed": pending.get("removed", False), "completed_at": None, "mode": mode, "params": params}
        yield None
        datetime.now().isoformat()
        raw_type = metadata.get("task_type")
        params = metadata.get("params")
        from WeRobotCore.task_system_v3.types import TaskType
        task_type = raw_type
        task_type = context.task_type.value
        params = getattr(context, "params", None)
        mode = getattr(context, "execution_mode", None)
        mode = mode.value
        metadata.get("type")
        self._schedule_metadata.get(task_id)
    def _on_job_acquired(self, event):
        """任务获取事件"""

        yield None
    def _on_job_released(self, event):
        """任务释放事件"""

        self.logger.info("任务释放: ", f'{event.job_id}')
    def _on_job_added(self, event):
        """任务添加事件"""

        self.logger.info("任务添加: ", f'{event.job_id}')
    def _on_job_removed(self, event):
        """任务移除事件"""

        self.logger.info("任务移除: ", f'{event.job_id}')
        pending = self._finalization_pending.get(event.job_id, {})
        pending.update({"removed": True})
        self._finalization_pending[event.job_id] = pending
        yield None
    def _on_job_cancelled(self, event):
        """任务取消事件"""

        self.logger.info("任务取消: ", f'{event.job_id}')
        pending = self._finalization_pending.get(event.job_id, {})
        pending.update({"status": "cancelled"})
        self._finalization_pending[event.job_id] = pending
        yield None
    def _on_job_deadline_missed(self, event):
        """任务错过截止时间事件"""

        self.logger.warning("任务错过截止时间: ", f'{event.job_id}')
        yield None
    def shutdown(self):
        """关闭调度器"""

        self._state = SchedulerState.STOPPING
        self._state = SchedulerState.STOPPED
        self.logger.info("统一调度器已关闭")
        self._fallback_timer_task.cancel()
        yield None
        yield None
    def _handle_existing_tasks(self):
        """处理系统启动时已存在的持久化任务"""

        yield None
    def _get_task_type_from_schedule(self, schedule):
        """从调度任务中提取任务类型"""

        return "unknown"
        return "moment_post"
        return TaskType.SYNC_CONTACTS.value
        return "auto_reply"
        return "mass_sending"
        task_info = schedule.metadata.get("task_info", {})
        return task_info["task_type"]
    def _handle_task_timeout_logic(self, schedule, current_time):
        """处理任务超时逻辑

                Args:
                    schedule: 调度任务对象
                    current_time: 当前时间

                Returns:
                    bool: True表示任务应该继续运行，False表示需要更新执行时间
                """

        next_run_time = getattr(schedule, "next_fire_time", None)
        f'{next_run_time}'("，", f'{schedule.id}')
        task_metadata = getattr(schedule, "metadata", {})
        execution_strategy = task_metadata.get("execution_strategy", {})
        return True
        return False
        end_date_str = execution_strategy.get("end_date")
        end_date = datetime.fromisoformat(end_date_str).date()
        current_date = current_time.date()
        yield None
        current_time = current_time.replace(tzinfo=None)
        next_run_time = next_run_time.replace(tzinfo=None)
        "任务 "(f'{schedule.id}', " 没有下次执行时间，允许继续运行")
        return True
    def _update_schedule_next_run_time(self, schedule):
        trigger = getattr(schedule, "trigger", None)
        from apscheduler.triggers.cron import CronTrigger
        from apscheduler.triggers.combining import OrTrigger
        current_time = datetime.now()
        next_run_time = None
        print("更新前：", f'{next_run_time}')
        yield None
        next_run_time = next(trigger)
        print("更新前__next__：", f'{next_run_time}')
        next_run_time = trigger.next_fire_time
        print("更新前next_fire_time：", f'{next_run_time}')
        next_run_time = trigger.get_next_fire_time(None, current_time)
        print("更新前get_next_fire_time：", f'{next_run_time}')
        args = []
        kwargs = getattr(schedule, "kwargs", {})
        metadata = self._schedule_metadata.get(schedule.id)
        paused = getattr(schedule, "paused", False)
        yield None
        getattr(schedule, "metadata", {})
    def _recover_task_metadata(self, schedules):
        """恢复任务元数据到内存中"""

        recovered_count = 0
        schedule = schedules
        self._schedule_metadata[schedule.id] = schedule.metadata
        recovered_count = recovered_count + 1
