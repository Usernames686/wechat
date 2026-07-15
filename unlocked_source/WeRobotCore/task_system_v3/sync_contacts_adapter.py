# Decompiled from: sync_contacts_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

"""
自动同步通讯录任务适配器
采用标准的adapter模式，实现通讯录定期同步功能
"""

__doc__ = "\n自动同步通讯录任务适配器\n采用标准的adapter模式，实现通讯录定期同步功能\n"
import asyncio
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from WeRobotCore.task_system_v3.types import TaskType, TaskStatus, TaskPriority, ScheduleConfig, TaskExecutionContext, TriggerType, ExecutionMode
from WeRobotCore.task_system_v2.base import BaseTask
from WeRobotCore.utils.logger import task_logger, get_logger
class SyncContactsAdapter:
    """SyncContactsAdapter"""

    __doc__ = "自动同步通讯录任务适配器 - 标准版本"
    def __init__(self, unified_scheduler, permission_manager):
        self.scheduler = unified_scheduler
        self.permission_manager = permission_manager
        self.logger = get_logger("sync_contacts_adapter")
        self.task_logger = task_logger
        self._task_instances = {}
        self._task_instance_timestamps = {}
        self._is_running = False
        self._startup_time = None
        self._sync_contacts_config = {"timeout_seconds": 3600, "misfire_grace_time_hours": 2, "coalesce": True, "auto_resume_enabled": True, "auto_resume_task_type": "sync_contacts"}
        self.scheduler.register_task_executor(TaskType.SYNC_CONTACTS, self._execute_sync_contacts_task)
        self.scheduler.register_auto_resume_task_type(self.get_auto_resume_task_type())
    def get_task_config(self):
        """获取sync_contacts任务的配置信息"""

        return self._sync_contacts_config.copy()
    def get_timeout_seconds(self):
        """获取任务超时时间（秒）"""

        return self._sync_contacts_config["timeout_seconds"]
    def get_misfire_config(self):
        """获取Misfire策略配置"""

        return {"misfire_grace_time_hours": self._sync_contacts_config["misfire_grace_time_hours"], "coalesce": self._sync_contacts_config["coalesce"]}
    def is_auto_resume_enabled(self):
        """检查是否启用自动恢复"""

        return self._sync_contacts_config["auto_resume_enabled"]
    def get_auto_resume_task_type(self):
        """获取自动恢复的任务类型标识"""

        return self._sync_contacts_config["auto_resume_task_type"]
    def apply_task_config_to_schedule(self, schedule_config):
        """将sync_contacts特定的配置应用到调度配置中

                Args:
                    schedule_config: 原始调度配置

                Returns:
                    ScheduleConfig: 应用了sync_contacts配置的调度配置
                """

        optimized_config = ScheduleConfig(trigger_type=schedule_config.trigger_type, trigger_args=schedule_config.trigger_args.copy(), execution_mode=schedule_config.execution_mode, misfire_grace_time=schedule_config.misfire_grace_time, coalesce=schedule_config.coalesce)
        optimized_config.misfire_grace_time = int(self._sync_contacts_config["misfire_grace_time_hours"] * 3600)
        optimized_config.coalesce = self._sync_contacts_config["coalesce"]
        return optimized_config
    def start(self):
        """启动适配器"""

        self._is_running = True
        self._startup_time = datetime.now()
        return True
        self.logger.warning("自动同步通讯录适配器已在运行")
        return True
    def stop(self):
        """停止适配器"""

        self._task_instances.clear()
        self._task_instance_timestamps.clear()
        self._is_running = False
        self._startup_time = None
        self.logger.info("自动同步通讯录适配器停止成功")
        return True
        self.logger.warning("自动同步通讯录适配器未在运行")
        return True
    def generate_task_id(self):
        """生成任务ID"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f'{timestamp}'
    def _build_task_metadata(self, task_data):
        """构建任务元数据"""

        task_id = self.generate_task_id()
        start_date = datetime.now().date()
        current_time = datetime.now().isoformat()
        return {"task_info": {"task_id": task_id, "task_type": "sync_contacts", "created_at": current_time, "updated_at": current_time}, "sync_config": {"sync_items": task_data.get("sync_items", ["group"]), "sync_frequency": task_data.get("sync_frequency", 7), "time_range_start": task_data.get("time_range_start", "02:00"), "time_range_end": task_data.get("time_range_end", "04:00"), "start_date": start_date.isoformat()}, "execution_stats": {"execution_count": 0, "last_execution_time": "", "total_success": 0, "total_failed": 0}, "task_status": "active", "execution_history": []}
    def _calculate_next_execution_time(self, sync_config, last_execution_date):
        """
                计算下次执行时间

                参数：
                - sync_config: 同步配置
                - last_execution_date: 上次执行日期（格式：YYYY-MM-DD），None表示从未执行过

                核心逻辑：
                1. 根据同步频率（每隔x天）计算下次执行日期
                2. 在执行日期的指定时间段内选择开始时间点
                """

        current_time = datetime.now()
        current_date = current_time.date()
        time_range_start = sync_config.get("time_range_start", "02:00")
        time_range_end = sync_config.get("time_range_end", "04:00")
        start_hour = map(int, time_range_start.split(":"))[0]
        start_minute = map(int, time_range_start.split(":"))[1]
        end_hour = map(int, time_range_end.split(":"))[0]
        end_minute = map(int, time_range_end.split(":"))[1]
        sync_frequency = sync_config.get("sync_frequency", 7)
        def is_in_time_range(check_time):
            check_hour = check_time.hour
            check_minute = check_time.minute
            check_minutes = check_hour * 60 + check_minute
            start_minutes = start_hour * 60 + start_minute
            end_minutes = end_hour * 60 + end_minute
            return check_minutes >= start_minutes
            return start_minutes <= check_minutes
            return "???" <= end_minutes
        last_date = datetime.strptime(last_execution_date, "%Y-%m-%d").date()
        next_date = last_date + timedelta(days=sync_frequency)
        next_execution_time = datetime.combine(next_date, datetime.min.time().replace(hour=start_hour, minute=start_minute))
        f'{current_time}'(" ，下次执行时间: ", f'{next_execution_time}')
        return next_execution_time
        days_since_last = (current_date - last_date).days
        cycles_passed = days_since_last // sync_frequency
        next_date = last_date + timedelta(days=(cycles_passed + 1) * sync_frequency)
        today_start_time = datetime.combine(current_date, datetime.min.time().replace(hour=start_hour, minute=start_minute))
        next_date = current_date + timedelta(days=1)
        next_execution_time = datetime.combine(next_date, datetime.min.time().replace(hour=start_hour, minute=start_minute))
        next_execution_time = today_start_time
        next_execution_time = current_time + timedelta(minutes=1)
    def create_sync_contacts_task(self, task_request):
        """创建自动同步通讯录任务"""

        sync_items = task_request.get("sync_items", [])
        sync_frequency = task_request.get("sync_frequency", 7)
        return {"success": False, "error": "同步频率必须在2-30天之间"}
        yield None
        return {"success": False, "error": "必须选择至少一个同步项（好友或群聊）"}
    def _execute_sync_contacts_task(self, context, params):
        """执行自动同步通讯录任务的核心逻辑"""

        schedule_id = context.schedule_id
        metadata = context.metadata
        task_status = metadata.get("task_status", "active")
        sync_config = metadata.get("sync_config", {})
        current_time = datetime.now()
        time_range_start = sync_config.get("time_range_start", "02:00")
        time_range_end = sync_config.get("time_range_end", "04:00")
        start_hour = map(int, time_range_start.split(":"))[0]
        start_minute = map(int, time_range_start.split(":"))[1]
        end_hour = map(int, time_range_end.split(":"))[0]
        end_minute = map(int, time_range_end.split(":"))[1]
        current_hour = current_time.hour
        current_minute = current_time.minute
        start_minutes = start_hour * 60 + start_minute
        end_minutes = end_hour * 60 + end_minute
        current_minutes = current_hour * 60 + current_minute
        "任务 "(f'{schedule_id}', " 不在执行时间段内，跳过执行")
        yield None
        yield None
        " 状态为 "(f'{task_status}', "，跳过执行")
        return {"success": True, "message": "任务已暂停或完成"}
    def _perform_sync_contacts_task(self, metadata):
        """执行具体的同步通讯录任务"""

        from WeRobotCore.task_system_v2.tasks.sync_contacts_task import SyncContactsTask
        sync_config = metadata.get("sync_config", {})
        task_params = {"sync_items": sync_config.get("sync_items", ["group"])}
        task_id = metadata["task_info"]["task_id"]
        sync_contacts_task = SyncContactsTask(task_id, task_params)
        start_time = time.time()
        yield None
    def _record_execution(self, schedule_id, result):
        """记录执行结果"""

        current_time = datetime.now()
        execution_record = {"execution_time": current_time.isoformat(), "success": result.get("success", False), "message": result.get("message", ""), "execution_duration": result.get("execution_time", 0)}
        yield None
    def _reschedule_task(self, schedule_id, metadata):
        """重新安排下次执行"""

        sync_config = metadata.get("sync_config", {})
        execution_stats = metadata.get("execution_stats", {})
        last_execution_time = execution_stats.get("last_execution_time", "")
        current_time = datetime.now()
        current_date = current_time.date().isoformat()
        next_execution_time = self._calculate_next_execution_time(sync_config, current_date)
        "无法计算任务 "(f'{schedule_id}', " 的下次执行时间")
        yield None
    def cancel_sync_contacts_task(self, task_id):
        """取消自动同步通讯录任务"""

        yield None
    def get_sync_contacts_task_info(self, task_id):
        """获取自动同步通讯录任务详细信息"""

        yield None
    def get_sync_contacts_tasks(self, status):
        """获取所有自动同步通讯录任务"""

        yield None
    def get_sync_contacts_task_status(self):
        """获取当前自动同步通讯录任务状态（单个任务）"""

        yield None
