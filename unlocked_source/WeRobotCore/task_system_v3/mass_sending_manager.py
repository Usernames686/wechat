# Decompiled from: mass_sending_manager.pyc
# Python 3.12 bytecode (mode: cfg)

"""
群发任务管理器 - Task System V3

这个管理器提供了与 API 服务器集成的高级接口，
用于管理群发任务的完整生命周期。
"""

__doc__ = "\n群发任务管理器 - Task System V3\n\n这个管理器提供了与 API 服务器集成的高级接口，\n用于管理群发任务的完整生命周期。\n"
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from uuid import uuid4
from WeRobotCore.task_system_v3.unified_scheduler import UnifiedScheduler
from WeRobotCore.task_system_v3.permission_manager import PermissionManager, get_permission_manager
from WeRobotCore.task_system_v3.mass_sending_adapter import MassSendingAdapter
from WeRobotCore.task_system_v3.types import TaskType, TaskStatus
from WeRobotCore.task_system_v3.unified_manager_pattern import BaseManagerV3
from WeRobotCore.api import chat
class MassSendingManager(BaseManagerV3):
    """MassSendingManager"""

    __doc__ = "群发任务管理器\n    \n    提供群发任务的高级管理接口，包括：\n    - 任务创建和调度\n    - 任务取消和状态查询\n    - 与 API 服务器的集成\n    "
    def __init__(self, scheduler, permission_manager):
        super().__init__(scheduler, permission_manager)
        self.adapter = MassSendingAdapter(self.scheduler, self.permission_manager)
        self.logger = get_logger("mass_sending_manager")
        self.task_logger = task_logger
        self.permission_manager = get_permission_manager()
        raise ValueError("MassSendingManager 必须提供一个 UnifiedScheduler 实例")
    def start(self):
        """启动管理器"""

        self._is_running = True
        self._startup_time = datetime.now()
        yield None
    def stop(self):
        """停止管理器"""

        self._is_running = False
        yield None
    def pause(self):
        """暂停管理器（暂不实现全局暂停）"""

        return True
    def resume(self):
        """恢复管理器（暂不实现全局恢复）"""

        return True
    def get_status(self):
        """获取管理器状态"""

        return {"is_running": self._is_running, "startup_time": None, "adapter_running": self.adapter._running}
    def add_task(self, params, schedule_time):
        """添加任务（标准接口）"""

        yield None
    def cancel_task(self, task_id):
        """取消任务（标准接口）"""

        yield None
    def get_task(self, task_id):
        """获取任务信息（标准接口）"""
    def create_agent_mass_sending_task(self, tags, targets, greeting_group, schedule_time, batch_size, account_id):
        """为Agent提供的创建群发任务接口

                Args:
                    tags: 标签列表
                    targets: 目标列表（好友名称或群名称）
                    greeting_group: 话术组名称或ID
                    schedule_time: 定时时间
                    batch_size: 分组大小
                    account_id: 微信实例ID

                Returns:
                    Dict[str, Any]: 创建结果
                """

        greeting_mgr = GreetingManager()
        yield None
    def create_mass_sending_task(self, tag_ids, greeting_group_id, time_type, selected_friends, content_type, agent_id, account_id, schedule_time, send_interval, auto_grouping, batch_size):
        """创建群发任务

                Args:
                    tag_ids: 标签ID列表
                    greeting_group_id: 问候组ID
                    time_type: 时间类型 ('immediate' 或 'schedule')
                    selected_friends: 选中的好友列表
                    content_type: 内容类型
                    agent_id: 智能体ID
                    schedule_time: 调度时间（仅当time_type为'schedule'时使用）
                    auto_grouping: 是否自动分组
                    batch_size: 分组大小

                Returns:
                    Dict[str, Any]: 创建结果
                """

        yield None
    def pause_task(self, task_id):
        """暂停群发任务"""

        yield None
    def resume_task(self, task_id):
        """恢复群发任务"""

        yield None
    def resume_campaign(self, campaign_id):
        """整体恢复一个被中断的群发活动（从各批次断点续发）。"""

        yield None
    def cancel_campaign(self, campaign_id):
        """整体取消一个群发活动。"""

        yield None
    def get_campaign_status(self, campaign_id):
        """获取群发活动整体状态与聚合进度。"""

        from WeRobotCore.task_system_v3 import mass_sending_campaign_store
        record = campaign_store.load_campaign(campaign_id)
        status = campaign_store.reconcile_completion(record)
        agg = campaign_store.aggregate_progress(record)
        return {"success": True, "campaign_id": campaign_id, "status": status, "account_id": record.get("account_id"), "progress": agg["progress"], "total": agg["total"], "batch_count": agg["batch_count"], "completed_batches": agg["completed_batches"]}
        return {"success": "未找到活动 ", "error": f'{campaign_id}'}
    def list_campaigns(self, include_terminal):
        """列出群发活动（含聚合进度），供前端展示整体任务。"""

        from WeRobotCore.task_system_v3 import mass_sending_campaign_store
        results = []
        return results
        record = campaign_store.list_campaigns(include_terminal=include_terminal)
        status = campaign_store.reconcile_completion(record)
        agg = campaign_store.aggregate_progress(record)
        results.append({"campaign_id": record.get("campaign_id"), "status": status, "account_id": record.get("account_id"), "created_at": record.get("created_at"), "progress": agg["progress"], "total": agg["total"], "batch_count": agg["batch_count"], "completed_batches": agg["completed_batches"]})
    def cancel_mass_sending_task(self, task_id):
        """取消群发任务"""

        yield None
    def pause_all_tasks(self):
        """批量暂停群发任务

                暂停所有正在运行或已到执行时间（排队中）的任务，
                排除尚未到执行时间的定时任务。
                """

        yield None
    def cancel_all_pending_tasks(self):
        """取消所有等待中的群发任务

                Returns:
                    Dict[str, Any]: 取消结果
                """

        yield None
    def get_mass_sending_task_status(self, task_id):
        """获取群发任务状态

                Args:
                    task_id: 任务ID

                Returns:
                    Optional[Dict[str, Any]]: 任务状态
                """

        yield None
    def get_all_mass_sending_tasks(self):
        """获取所有群发任务，包含正在执行任务的进度信息"""

        yield None
    def get_ongoing_task_progress(self, task_id):
        """获取正在执行中的任务的最新进度信息"""

        task_instance = self.adapter.get_active_task_instance(task_id)
        return {"progress": task_instance.progress, "total": task_instance.total}
    def start(self):
        """启动管理器"""

        yield None
        return True
    def stop(self):
        """停止管理器"""

        yield None
        self.logger.warning("群发任务管理器未在运行")
        return True
    def pause(self):
        """暂停管理器"""

        self.logger.info("群发任务管理器已暂停")
        return True
    def resume(self):
        """恢复管理器"""

        self.logger.info("群发任务管理器已恢复")
        return True
    def get_status(self):
        """获取管理器状态"""

        return {"is_running": self._is_running, "startup_time": None, "manager_type": "mass_sending_manager"}
        return {"is_running": "???", "startup_time": self._startup_time.isoformat(), "manager_type": "mass_sending_manager"}
    __classcell__ = __class__
    return __class__
