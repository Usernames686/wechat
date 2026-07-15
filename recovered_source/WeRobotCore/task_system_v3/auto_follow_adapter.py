# Decompiled from: auto_follow_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

"""
自动跟单任务适配器
合并V2和V3版本的核心业务逻辑，采用标准的adapter模式
"""

__doc__ = "\n自动跟单任务适配器\n合并V2和V3版本的核心业务逻辑，采用标准的adapter模式\n"
import asyncio
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
from WeRobotCore.task_system_v3.types import TaskType, TaskStatus, TaskPriority, ScheduleConfig, TaskExecutionContext, TriggerType, ExecutionMode
from WeRobotCore.task_system_v2.base import BaseTask
from WeRobotCore.utils.logger import task_logger, get_logger
class AutoFollowAdapter:
    """AutoFollowAdapter"""

    __doc__ = "自动跟单任务适配器 - 标准版本"
    def __init__(self, unified_scheduler, permission_manager):
        self.scheduler = unified_scheduler
        self.permission_manager = permission_manager
        self.logger = get_logger("auto_follow_adapter")
        self.task_logger = task_logger
        self._task_instances = {}
        self._task_instance_timestamps = {}
        self._is_running = False
        self._startup_time = None
        self._auto_follow_config = {"timeout_seconds": 7200, "misfire_grace_time_hours": 1, "coalesce": True, "auto_resume_enabled": True, "auto_resume_task_type": "auto_follow"}
        self.scheduler.register_task_executor(TaskType.AUTO_FOLLOW, self._execute_auto_follow_task)
        self.scheduler.register_auto_resume_task_type(self.get_auto_resume_task_type())
    def get_task_config(self):
        """获取auto_follow任务的配置信息"""

        return self._auto_follow_config.copy()
    def get_timeout_seconds(self):
        """获取任务超时时间（秒）"""

        return self._auto_follow_config["timeout_seconds"]
    def get_misfire_config(self):
        """获取Misfire策略配置"""

        return {"misfire_grace_time_hours": self._auto_follow_config["misfire_grace_time_hours"], "coalesce": self._auto_follow_config["coalesce"]}
    def is_auto_resume_enabled(self):
        """检查是否启用自动恢复"""

        return self._auto_follow_config["auto_resume_enabled"]
    def get_auto_resume_task_type(self):
        """获取自动恢复的任务类型标识"""

        return self._auto_follow_config["auto_resume_task_type"]
    def apply_task_config_to_schedule(self, schedule_config):
        """将auto_follow特定的配置应用到调度配置中

                Args:
                    schedule_config: 原始调度配置

                Returns:
                    ScheduleConfig: 应用了auto_follow配置的调度配置
                """

        optimized_config = ScheduleConfig(trigger_type=schedule_config.trigger_type, trigger_args=schedule_config.trigger_args.copy(), execution_mode=schedule_config.execution_mode, misfire_grace_time=schedule_config.misfire_grace_time, coalesce=schedule_config.coalesce)
        optimized_config.misfire_grace_time = int(self._auto_follow_config["misfire_grace_time_hours"] * 3600)
        optimized_config.coalesce = self._auto_follow_config["coalesce"]
        return optimized_config
    def start(self):
        """启动适配器"""

        self._is_running = True
        self._startup_time = datetime.now()
        return True
        self.logger.warning("自动跟单适配器已在运行")
        return True
    def stop(self):
        """停止适配器"""

        self._task_instances.clear()
        self._task_instance_timestamps.clear()
        self._is_running = False
        self._startup_time = None
        self.logger.info("自动跟单适配器停止成功")
        return True
        self.logger.warning("自动跟单适配器未在运行")
        return True
    def generate_task_id(self, friend_wxid):
        """生成任务ID"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f'{timestamp}'
    def _build_task_metadata(self, task_data):
        """构建任务元数据"""

        task_id = self.generate_task_id(task_data["friend_wxid"])
        start_date = datetime.now().date()
        follow_days = int(task_data.get("follow_days", 7))
        end_date = start_date + timedelta(days=follow_days - 1)
        follow_frequency = task_data.get("follow_frequency", 1)
        interval_days = 1
        step = interval_days + 1
        max_executions = (follow_days + step - 1) // step
        follow_frequency = interval_days
        current_time = datetime.now().isoformat()
        return {"task_info": {"task_id": task_id, "task_type": "auto_follow", "created_at": current_time, "updated_at": current_time}, "friend_info": {"wxid": task_data["friend_wxid"], "name": task_data.get("friend_name", ""), "account_id": task_data["account_id"], "chat_type": task_data.get("chat_type", "single")}, "execution_strategy": {"follow_scenario": task_data.get("follow_scenario", "新好友"), "follow_days": follow_days, "follow_frequency": follow_frequency, "time_range_start": task_data.get("time_range_start", "09:00"), "time_range_end": task_data.get("time_range_end", "12:00"), "start_date": start_date.isoformat(), "end_date": end_date.isoformat(), "max_executions": max_executions, "first_run_next_day": bool(task_data.get("first_run_next_day", False))}, "execution_stats": {"execution_count": 0, "last_execution_time": "", "next_execution_day": 1, "total_success": 0, "total_failed": 0}, "task_config": {"agent_id": task_data.get("agent_id", ""), "ai_service_type": task_data.get("ai_service_type", "coze")}, "task_status": "active", "execution_history": []}
        interval_days = 0
        interval_days = 1
        interval_days = int(follow_frequency)
        interval_days = 2
        interval_days = 1
        interval_days = follow_frequency
    def _calculate_next_execution_time(self, strategy, current_executions, last_execution_date, is_post_execution):
        """
                计算下次执行时间

                参数：
                - strategy: 执行策略
                - current_executions: 当前执行次数
                - last_execution_date: 上次执行日期（格式：YYYY-MM-DD），None表示从未执行过
                - is_post_execution: 是否为任务执行完成后的重新调度

                核心逻辑：
                1. 如果是任务执行完成后的重新调度，直接安排到下一个执行日期
                2. 否则，首先判断今天是否应该执行任务（基于上次执行日期和频率规则）
                3. 如果今天应该执行：
                   - 当前时间在执行时间段内：立即执行
                   - 当前时间早于执行时间段：安排到今天的开始时间
                   - 当前时间晚于执行时间段：安排到下一个应该执行的日期
                4. 如果今天不应该执行：安排到下一个应该执行的日期
                """

        current_time = datetime.now()
        current_date = current_time.date()
        time_range_start = strategy.get("time_range_start", "09:00")
        time_range_end = strategy.get("time_range_end", "12:00")
        start_hour = map(int, time_range_start.split(":"))[0]
        start_minute = map(int, time_range_start.split(":"))[1]
        end_hour = map(int, time_range_end.split(":"))[0]
        end_minute = map(int, time_range_end.split(":"))[1]
        today_start_time = datetime.combine(current_date, datetime.min.time().replace(hour=start_hour, minute=start_minute))
        today_end_time = datetime.combine(current_date, datetime.min.time().replace(hour=end_hour, minute=end_minute))
        follow_frequency = strategy.get("follow_frequency", "daily")
        should_execute_today = self._should_execute_today(current_date, last_execution_date, follow_frequency, current_executions)
        next_date = self._get_next_execution_date(current_date, follow_frequency, current_executions)
        next_execution_time = datetime.combine(next_date, datetime.min.time().replace(hour=start_hour, minute=start_minute))
        return next_execution_time
        next_date = current_date + timedelta(days=1)
        next_execution_time = datetime.combine(next_date, datetime.min.time().replace(hour=start_hour, minute=start_minute))
        return next_execution_time
        next_date = self._get_next_execution_date(current_date, follow_frequency, current_executions)
        next_execution_time = today_start_time
        return next_execution_time
        next_execution_time = current_time + timedelta(minutes=1)
        return next_execution_time
        next_date = current_date + timedelta(days=1)
        return datetime.combine(next_date, datetime.min.time().replace(hour=start_hour, minute=start_minute))
        next_date = self._get_next_execution_date(current_date, follow_frequency, current_executions)
        next_execution_time = datetime.combine(next_date, datetime.min.time().replace(hour=start_hour, minute=start_minute))
        return next_execution_time
    def _should_execute_today(self, current_date, last_execution_date, follow_frequency, current_executions):
        """
                判断今天是否应该执行任务
                """

        last_date = datetime.strptime(last_execution_date, "%Y-%m-%d").date()
        interval_days = 1
        days_since_last = (current_date - last_date).days
        return days_since_last >= interval_days + 1
        interval_days = 0
        days_since_last = (current_date - last_date).days
        return days_since_last >= 2
        return True
        interval_days = int(follow_frequency)
        interval_days = 2
        interval_days = 1
        interval_days = follow_frequency
        return False
        return True
    def _get_next_execution_date(self, current_date, follow_frequency, current_executions):
        """
                获取下一个应该执行的日期
                """

        interval_days = 1
        return current_date + timedelta(days=interval_days + 1)
        interval_days = 0
        return current_date + timedelta(days=2)
        return current_date + timedelta(days=1)
        interval_days = int(follow_frequency)
        interval_days = 2
        interval_days = 1
        interval_days = follow_frequency
    def add_task(self, account_id, params, schedule_time):
        """添加自动跟单任务"""

        metadata = self._build_task_metadata(params)
        task_id = metadata["task_info"]["task_id"]
        schedule_config = ScheduleConfig(trigger_type=TriggerType.DATE, trigger_args={"run_time": schedule_time}, execution_mode=ExecutionMode.SCHEDULED, max_instances=1, coalesce=True, misfire_grace_time=30)
        optimized_config = self.apply_task_config_to_schedule(schedule_config)
        yield None
        raise ValueError("无法计算任务执行时间")
        execution_strategy = metadata["execution_strategy"]
        last_execution_date = metadata.get("execution_stats", {}).get("last_execution_date")
        schedule_time = self._calculate_next_execution_time(execution_strategy, 0, last_execution_date)
        print("计算出的首次执行时间: ", f'{schedule_time}')
    def _execute_auto_follow_task(self, context, params):
        """执行自动跟单任务的核心逻辑"""

        schedule_id = context.schedule_id
        metadata = context.metadata
        task_status = metadata.get("task_status", "active")
        execution_stats = metadata.get("execution_stats", {})
        execution_strategy = metadata.get("execution_strategy", {})
        current_executions = execution_stats.get("execution_count", 0)
        max_executions = execution_strategy.get("max_executions", 0)
        execution_strategy = metadata.get("execution_strategy", {})
        current_time = datetime.now()
        time_range_start = execution_strategy.get("time_range_start", "09:00")
        time_range_end = execution_strategy.get("time_range_end", "12:00")
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
        " 已达到最大执行次数 "(f'{max_executions}', "，标记为完成")
        yield None
        " 状态为 "(f'{task_status}', "，跳过执行")
        return {"success": True, "message": "任务已暂停或完成"}
    def _perform_auto_follow_task(self, metadata):
        """执行具体的跟单任务"""

        from WeRobotCore.task_system_v2.tasks.auto_follow_task import AutoFollowTask
        task_params = {"friend_wxid": metadata["friend_info"]["wxid"], "friend_name": metadata["friend_info"]["name"], "account_id": metadata["friend_info"]["account_id"], "chat_type": metadata["friend_info"].get("chat_type", "single"), "follow_scenario": metadata["execution_strategy"]["follow_scenario"], "agent_id": metadata["task_config"]["agent_id"], "ai_service_type": metadata["task_config"]["ai_service_type"]}
        task_id = metadata["task_info"]["task_id"]
        task_params["metadata"] = metadata
        auto_follow_task = AutoFollowTask(task_id, task_params)
        start_time = time.time()
        yield None
    def _update_task_status(self, schedule_id, status):
        """更新任务状态"""

        yield None
    def _record_execution(self, schedule_id, result):
        """记录执行历史"""

        f'{schedule_id}'(", ", f'{result}')
        yield None
    def _reschedule_task(self, schedule_id, metadata):
        """重新安排任务执行时间"""

        yield None
    def create_auto_follow_task(self, task_request):
        """创建自动跟单任务"""

        required_fields = ("account_id", "friend_wxid", "friend_name", "agent_id")
        yield None
        field = _
        return {"success": "缺少必需参数: ", "error": f'{field}'}
    def create_batch_auto_follow_tasks(self, batch_request):
        """批量创建自动跟单任务"""

        friends_list = batch_request.get("friend_list", [])
        results = []
        success_count = 0
        failed_count = 0
        common_params = {"account_id": batch_request["account_id"], "agent_id": batch_request["agent_id"], "follow_scenario": batch_request.get("follow_scenario", "新好友"), "follow_days": batch_request.get("follow_days", 7), "follow_frequency": batch_request.get("follow_frequency", "daily"), "time_range_start": batch_request.get("time_range_start", "09:00"), "time_range_end": batch_request.get("time_range_end", "12:00"), "first_run_next_day": batch_request.get("first_run_next_day", False)}
        return {"success": True, "total_friends": len(friends_list), "success_count": success_count, "failed_count": failed_count, "results": results}
        friend = friends_list
        task_request = {"friend_wxid": friend["wxid"], "friend_name": friend["nickname"], "chat_type": friend.get("chat_type", "single")}
        yield None
        return {"success": False, "error": "好友列表不能为空"}
    def cancel_auto_follow_task(self, task_id):
        """取消自动跟单任务"""

        t0 = time.time()
        yield None
    def pause_auto_follow_task(self, task_id):
        """暂停自动跟单任务"""

        yield None
    def resume_auto_follow_task(self, task_id):
        """恢复自动跟单任务"""

        yield None
    def get_auto_follow_tasks_by_account(self, account_id, status):
        """获取账号下的所有跟单任务"""

        yield None
    def get_tasks_by_account(self, account_id, status):
        """获取账号下的所有任务（改动：不需要判断账号，获取所有账号的任务）"""

        yield None
    def get_tasks_by_friend(self, friend_wxid, account_id):
        """获取好友的所有任务"""

        yield None
    def get_auto_follow_task_info(self, task_id):
        """获取自动跟单任务详细信息"""

        yield None
    def cancel_auto_follow_tasks_by_friend(self, friend_wxid, account_id):
        """根据好友微信ID取消跟单任务"""

        yield None
    def batch_cancel_auto_follow_tasks(self, task_ids):
        """批量取消自动跟单任务
                Args:
                    task_ids: 需要取消的任务ID列表
                Returns:
                    Dict: 包含取消成功与失败的统计信息
                """

        cancelled = []
        failed = []
        return {"success": True, "total": len(task_ids), "cancelled": cancelled, "failed": failed}
        tid = task_ids
        yield None
    def batch_update_auto_follow_agent(self, task_ids, new_agent_id):
        """批量修改自动跟单任务的跟进智能体ID
                Args:
                    task_ids: 自动跟单任务ID列表
                    new_agent_id: 新的智能体ID
                Returns:
                    Dict: 更新结果统计
                """

        updated = []
        failed = []
        return {"success": True, "total": len(task_ids), "updated": updated, "failed": failed}
        tid = task_ids
        yield None
    def find_auto_follow_tasks(self, agent_id, date_str):
        """根据智能体ID和任务开始日期(创建时间)组合筛选自动跟单任务（两个参数均可选）"""

        from datetime import datetime
        target_date = None
        yield None
        target_date = datetime.fromisoformat(date_str).date()
    def find_auto_follow_tasks_by_start_date(self, date_str):
        """兼容旧接口：仅按开始日期筛选自动跟单任务"""

        yield None
    def get_auto_follow_logs(self, task_id, account_id, friend_wxid, limit):
        """获取自动跟单执行日志（通过 logger 读取兼容新老版本）"""

        from WeRobotCore.utils.logger import task_logger
        all_logs = task_logger.get_auto_follow_logs()
        formatted_logs = []
        formatted_logs.sort(key=lambda x: x["execution_time"], reverse=True)
        formatted_logs = limit
        return {"success": True, "data": formatted_logs, "total_count": len(formatted_logs)}
        log_entry = None
        execution_time = log_entry.get("execution_time")
        formatted_log = {"id": "id"(f'{log_entry.get("task_id", "")}', "_", f'{execution_time}'), "task_id": log_entry.get("task_id", ""), "friend_wxid": log_entry.get("friend_wxid", ""), "friend_name": log_entry.get("friend_name", ""), "account_id": log_entry.get("account_id", ""), "execution_time": execution_time, "status": log_entry.get("status", "failed"), "message_content": log_entry.get("message_content"), "error_message": log_entry.get("error", ""), "agent_id": log_entry.get("agent_id", ""), "follow_scenario": log_entry.get("follow_scenario", "")}
        formatted_logs.append(formatted_log)
