# Decompiled from: mass_sending_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

"""
群发任务适配器 - Task System V3

这个适配器负责将 v2 的群发任务适配到 v3 调度系统中，
保持原有的业务逻辑和功能完整性。
"""

__doc__ = "\n群发任务适配器 - Task System V3\n\n这个适配器负责将 v2 的群发任务适配到 v3 调度系统中，\n保持原有的业务逻辑和功能完整性。\n"
import asyncio
import importlib
import importlib.util as importlib
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Type, List
import uuid
from WeRobotCore.task_system_v3.types import TaskType, TaskPriority, TaskStatus, BaseTask, TimedBaseTask, ScheduleConfig, TriggerType, ExecutionMode, TaskExecutionContext, PermissionRequest, PermissionLevel
from WeRobotCore.task_system_v3.permission_manager import PermissionManager
from typing import TYPE_CHECKING
from WeRobotCore.utils.logger import task_logger, get_logger
from WeRobotCore.task_system_v2.websocket_manager import websocket_manager
class MassSendingAdapter:
    """MassSendingAdapter"""

    __doc__ = "群发任务适配器\n    \n    负责处理群发任务的执行、调度和状态管理，\n    确保与 v2 系统的完全兼容性。\n    "
    def __init__(self, scheduler, permission_manager):
        self.scheduler = scheduler
        self.permission_manager = permission_manager
        self.task_class_cache = {}
        self.logger = get_logger("mass_sending_adapter")
        self.task_logger = task_logger
        self._active_task_instances = {}
        self._completed_tasks_history = []
        self._running = False
        self._paused = False
        from WeRobotCore.utils.data_manager import DataManager
        base_dir = os.path.join(DataManager.get_data_dir_str(), "mass_sending_tasks")
        os.makedirs(base_dir, exist_ok=True)
        self._tasks_state_file = os.path.join(base_dir, "tasks_state.json")
        self.scheduler.register_task_executor(TaskType.MASS_SENDING, self._execute_mass_sending_task)
        self.scheduler.add_event_listener("task_finalized", self._on_task_finalized)
        self.scheduler.add_event_listener("task_cancelled", self._on_task_cancelled)
    def start(self):
        """启动适配器"""

        self._running = True
        self._paused = False
        yield None
        return True
    def _reconcile_stalled_campaigns_on_startup(self):
        """仅在启动时执行：把"未完成、但已无任何存活批次"的孤儿活动置为中断。

                ⚠ 只能在启动期调用，不可放到运行期（如前端列表轮询）。原因：链式投递的"投下一批"
                由 task_finalized 事件异步触发（在上一批 job 移除后才发布），批次之间存在真实空窗；
                运行期检测会在该空窗里把健康活动误判为卡死、并被前端显示为"微信掉线"。
                启动期系统处于静止态（无在途链式推进），不存在该空窗，可安全判定。

                覆盖场景：进程重启 / 崩溃后，活动未完成、但调度器里已没有它的任何批次——
                例如历史版本里后续批次因等权限超时被静默丢弃，或链头完成而下一批尚未投递时进程退出。
                这类活动既非 paused 也非 interrupted，前端不会显示"继续"按钮 → 静默卡死。
                置为 interrupted 后，用户即可点"继续"，由 resume_campaign 链式从断点续发。
                """

        from WeRobotCore.task_system_v3 import mass_sending_campaign_store
        non_terminal = campaign_store.list_campaigns(include_terminal=False)
        r = []
        live_ids = set(self._active_task_instances.keys())
        yield None
        r = _
    def stop(self):
        """停止适配器"""

        self._running = False
        self._paused = False
        self.logger.info("群发任务适配器停止成功")
        return True
        self.logger.info("群发任务适配器未在运行")
        return True
    def _save_tasks_state(self):
        """保存任务状态到文件"""

        tasks_data = []
        f = open(self._tasks_state_file, "w", encoding="utf-8")
        json.dump(tasks_data, f, ensure_ascii=False, indent=2)
        self._active_task_instances.items()(None, None, None)
        task_id = "???"[0]
        instance = "???"[1]
        status = getattr(instance, "status", TaskStatus.PENDING)
        tasks_data.append({"id": task_id, "params": instance.params, "schedule_time": None, "status": str(status), "created_at": datetime.now().isoformat(), "progress": getattr(instance, "progress", 0), "sent_users": list(getattr(instance, "sent_users", [])), "total": getattr(instance, "total", 0), "interrupted": getattr(instance, "interrupted", False), "interrupt_reason": getattr(instance, "interrupt_reason", None)})
        status = status.value
    def _restore_paused_tasks(self):
        """恢复处于暂停状态的任务"""

        f = open(self._tasks_state_file, "r", encoding="utf-8")
        tasks_data = json.load(f)
        None(None, None)
        yield None
    def add_mass_sending_task(self, task_params, schedule_time, task_id):
        """添加群发任务

                Args:
                    task_params: 任务参数，包含群发配置
                    schedule_time: 调度时间，None表示立即执行
                    task_id: 任务ID，None则自动生成

                Returns:
                    str: 任务ID
                """

        cleaned_params = {}
        execution_params = {"task_id": task_id, "task_params": cleaned_params, "original_task_type": TaskType.MASS_SENDING.value}
        schedule_config = ScheduleConfig(trigger_type=TriggerType.DATE, trigger_args={"run_time": schedule_time}, execution_mode=ExecutionMode.SCHEDULED)
        yield None
        yield None
        k = _[0]
        v = _[1]
        cleaned_params[k] = v
        self.scheduler.add_immediate_task(task_type=TaskType.MASS_SENDING, params=execution_params, task_id=task_id)
        task_id = f'{8}'
    def pause_mass_sending_task(self, task_id):
        """暂停群发任务"""

        success = False
        instance = self._active_task_instances.get(task_id)
        yield None
        instance.status = TaskStatus.PAUSED
        self._save_tasks_state()
        return success
        instance.pause()
        success = True
        yield None
        yield None
    def resume_mass_sending_task(self, task_id):
        """恢复群发任务"""

        success = False
        instance = self._active_task_instances.get(task_id)
        return success
        instance.status = TaskStatus.RUNNING
        self._save_tasks_state()
        return success
        instance.resume()
        success = True
        yield None
        yield None
        self.logger.info("恢复已持久化的暂停任务，重新提交调度: ", f'{task_id}')
        delattr(instance, "_is_restored_paused")
        params = instance.params
        params["_restored_progress"] = getattr(instance, "progress", 0)
        params["_restored_sent_users"] = list(getattr(instance, "sent_users", []))
        params["_restored_total"] = getattr(instance, "total", 0)
        yield None
    def resume_campaign(self, campaign_id):
        """整体恢复一个群发活动（手动恢复策略，方案 A 链式投递）。

                从断点续发：
                - 先把活动状态置回 running，解除 campaign 闸门；
                - 跳过已发完的批次，仅投递"第一个未完成批次"（注入断点，已发用户不重复发送）；
                - 其余未完成批次由 _advance_campaign_chain 在每批终态后逐个接力，
                  全程权限等待队列深度恒为 0~1，从根上规避了"批次一次性排队等权限超时"的问题。
                """

        from WeRobotCore.task_system_v3 import mass_sending_campaign_store
        record = campaign_store.load_campaign(campaign_id)
        campaign_store.update_status(campaign_id, "running")
        batches = sorted(record.get("batches", []), key=lambda b: b.get("batch_index", 0))
        skipped = 0
        start_cursor = 0
        first_pending = None
        campaign_store.set_dispatched_index(campaign_id, start_cursor)
        yield None
        campaign_store.reconcile_completion(campaign_id)
        yield None
        b = _
        tid = b.get("task_id")
        prog = campaign_store._read_batch_progress(tid)
        sent = set(prog.get("sent_users", []))
        total = int(prog.get("total", 0))
        first_pending = b
        self.broadcast_task_list_update()
        skipped = skipped + 1
        start_cursor = int(b.get("batch_index", 0))
        return {"success": "未找到活动 ", "error": f'{campaign_id}'}
    def cancel_campaign(self, campaign_id):
        """整体取消一个群发活动：取消其所有批次并把活动置为已取消。"""

        from WeRobotCore.task_system_v3 import mass_sending_campaign_store
        record = campaign_store.load_campaign(campaign_id)
        status = campaign_store.reconcile_completion(record)
        cancelled = 0
        campaign_store.update_status(campaign_id, "cancelled")
        yield None
        b = _
        tid = b.get("task_id")
        yield None
        status_text = {"completed": "已完成", "cancelled": "已取消"}.get(status, status)
        return {"success": f'{status_text}', "error": "，无法取消", "status": status}
        return {"success": "未找到活动 ", "error": f'{campaign_id}'}
    def _dispatch_campaign_batch(self, batch_entry, schedule_time):
        """投递活动中的单个批次（方案 A 链式投递的最小执行单元）。

                - 若该批次依进度文件判定已发完，返回 False（表示应跳过、由调用方继续找下一批）；
                - 否则注入断点（已发用户跳过、不重复发送）并提交调度，返回 True。

                与 resume_campaign 共用本方法，保证"创建首批 / 链式下一批 / 整体恢复"三处投递口径一致。
                """

        from WeRobotCore.task_system_v3 import mass_sending_campaign_store
        tid = batch_entry.get("task_id")
        params = dict(batch_entry.get("params", {}))
        prog = campaign_store._read_batch_progress(tid)
        sent = set(prog.get("sent_users", []))
        total = int(prog.get("total", 0))
        yield None
        return False
        return False
    def _advance_campaign_chain(self, campaign_id, finished_index):
        """某批终态后，投递活动中的下一批（方案 A 链式投递的推进器）。

                通过 dispatched_index 游标去重：仅当本次终态对应的批次就是当前链头
                （finished_index >= 游标）时才推进，避免重复/陈旧的终态事件造成重复投递。
                中断 / 取消 / 已完成的活动一律不再推进。
                """

        from WeRobotCore.task_system_v3 import mass_sending_campaign_store
        record = campaign_store.load_campaign(campaign_id)
        dispatched_index = int(record.get("dispatched_index", 0))
        batches = sorted(record.get("batches", []), key=lambda b: b.get("batch_index", 0))
        campaign_store.reconcile_completion(campaign_id)
        entry = batches
        idx = int(entry.get("batch_index", 0))
        yield None
    def _execute_mass_sending_task(self, context, params):
        """执行群发任务

                Args:
                    context: 任务执行上下文
                    params: 执行参数

                Returns:
                    Any: 执行结果
                """

        task_id = params.get("task_id", context.task_id)
        task_params = params.get("task_params", {})
        def yield_permission_callback():
            """释放权限回调"""

            "任务 "(f'{task_id}', " 暂停，释放执行权限")
            yield None
        def acquire_permission_callback():
            """重新获取权限回调"""

            "任务 "(f'{task_id}', " 恢复，重新申请执行权限")
            priority = TaskPriority.MEDIUM
            request = PermissionRequest(task_id=task_id, task_type=TaskType.MASS_SENDING, permission_level=PermissionLevel.EXCLUSIVE, priority=priority, scheduler_name="unified_scheduler", pause_chat_monitor=True, timeout_seconds=3600)
            yield None
            priority = context.priority
        yield None
    def _get_mass_sending_task_class(self):
        """动态获取群发任务类

                Returns:
                    Type[TimedBaseTask]: 群发任务类
                """

        return self.task_class_cache["MassSendingTask"]
        task_class = None
        module = importlib.import_module("WeRobotCore.task_system_v2.tasks.mass_sending_task")
        task_class = getattr(module, "MassSendingTask")
        self.task_class_cache["MassSendingTask"] = task_class
        raise ImportError("无法导入群发任务类")
    def _get_task_priority(self, task_params):
        """获取任务优先级

                Args:
                    task_params: 任务参数

                Returns:
                    int: 优先级数值
                """

        priority = task_params.get("priority", TaskPriority.MEDIUM)
        return TaskPriority.MEDIUM.value
        return priority.value
    def _log_task_error(self, task_id, task_params, error):
        """记录任务错误

                Args:
                    task_id: 任务ID
                    task_params: 任务参数
                    error: 错误信息
                """

        task_logger.add_mass_sending_log(task_id=task_id, status=TaskStatus.FAILED.value, params=task_params, error=error)
    def _add_to_history(self, task_id, status, params, result, error):
        """添加任务到历史记录"""

        completed_info = {"id": task_id, "type": TaskType.MASS_SENDING.value, "status": status, "execution_time": datetime.now().isoformat(), "params": params, "result": result, "error": error}
        t = []
        self._completed_tasks_history = self._completed_tasks_history
        self._completed_tasks_history.append(completed_info)
        self._completed_tasks_history.pop(0)
        self._completed_tasks_history = []
    def cancel_mass_sending_task(self, task_id):
        """取消群发任务

                Args:
                    task_id: 任务ID

                Returns:
                    bool: 是否成功取消
                """

        yield None
    def get_mass_sending_task_status(self, task_id):
        """获取群发任务状态

                Args:
                    task_id: 任务ID

                Returns:
                    Optional[Dict[str, Any]]: 任务状态信息
                """

        return self.scheduler.get_task_status(task_id)
    def get_all_mass_sending_tasks(self):
        """获取所有群发任务

                Returns:
                    List[Dict[str, Any]]: 任务列表
                """

        yield None
        self._completed_tasks_history = []
    def _broadcast_task_completion(self, task_id, task_params, result):
        """广播任务完成状态通知"""

        yield None
        self.logger.warning("WebSocket管理器未可用，无法广播任务状态")
    def broadcast_task_list_update(self):
        """广播任务列表更新通知"""

        yield None
    def get_active_task_instance(self, task_id):
        """获取活跃的任务实例"""

        return self._active_task_instances.get(task_id)
    def _on_task_finalized(self, payload):
        """处理统一终态事件并广播群发任务列表，降低状态抖动"""

        task_type = payload.get("task_type")
        task_id = payload.get("task_id")
        status = payload.get("status")
        result = payload.get("result")
        error = payload.get("error")
        params = payload.get("params")
        self._add_to_history(task_id=task_id, status=status, params=params, result=result, error=error)
        inner = {}
        campaign_id = inner.get("campaignId")
        batch_index = int(inner.get("batchIndex", 0))
        yield None
        yield None
        inner = {}
        campaign_id = inner.get("campaignId")
        from WeRobotCore.task_system_v3 import mass_sending_campaign_store
        new_status = campaign_store.reconcile_completion(campaign_id)
        "活动 "(f'{campaign_id}', " 全部批次完成，整体置为完成")
        params.get("task_params", params)
        self._completed_tasks_history = []
    def _on_task_cancelled(self, context):
        """处理任务取消事件

                Args:
                    context: 任务执行上下文或包含task_id的字典
                """

        task_id = None
        self._save_tasks_state()
        instance = self._active_task_instances[task_id]
        self.logger.info("收到任务取消事件，停止运行中的任务实例: ", f'{task_id}')
        instance.cancel()
        yield None
        task_id = context.get("task_id")
        task_id = context.task_id
from WeRobotCore.task_system_v3.unified_scheduler import UnifiedScheduler
