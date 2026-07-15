# Decompiled from: mass_sending_campaign_store.pyc
# Python 3.12 bytecode (mode: cfg)

"""
群发活动（Campaign）持久化存储 - Task System V3

一个"群发活动"= 用户一次创建的群发任务（如 1300 人），在自动分组下会被切分为
若干批次（每批一个独立调度任务）。本模块负责把这些批次串成一个整体，提供：

- 活动创建时落盘（含每个批次的 task_id 与参数，便于中断后整体恢复）
- 活动状态管理（running / interrupted / completed / cancelled）
- 重启后查询未完成活动，对其批次执行"campaign 闸门"：中断态下批次 fire 即自我挂起
- 整体进度聚合（读取各批次的断点进度文件求和）

设计为单进程 asyncio 下使用，JSON 文件存储，读写即时落盘。
"""

__doc__ = "\n群发活动（Campaign）持久化存储 - Task System V3\n\n一个\"群发活动\"= 用户一次创建的群发任务（如 1300 人），在自动分组下会被切分为\n若干批次（每批一个独立调度任务）。本模块负责把这些批次串成一个整体，提供：\n\n- 活动创建时落盘（含每个批次的 task_id 与参数，便于中断后整体恢复）\n- 活动状态管理（running / interrupted / completed / cancelled）\n- 重启后查询未完成活动，对其批次执行\"campaign 闸门\"：中断态下批次 fire 即自我挂起\n- 整体进度聚合（读取各批次的断点进度文件求和）\n\n设计为单进程 asyncio 下使用，JSON 文件存储，读写即时落盘。\n"
import json
import os
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List
from WeRobotCore.utils.logger import get_logger
_logger = get_logger("mass_sending_campaign_store")
TERMINAL_STATUSES = {"completed", "cancelled"}
_lock = threading.RLock()
def _campaigns_dir():
    from WeRobotCore.utils.data_manager import DataManager
    base_dir = os.path.join(DataManager.get_data_dir_str(), "mass_sending_campaigns")
    os.makedirs(base_dir, exist_ok=True)
    return base_dir
def _campaign_path(campaign_id):
    return os.path.join(_campaigns_dir(), f'{campaign_id}', ".json")
def _progress_path(task_id):
    from WeRobotCore.utils.data_manager import DataManager
    base_dir = os.path.join(DataManager.get_data_dir_str(), "mass_sending_progress")
    return os.path.join(base_dir, f'{task_id}', ".json")
def save_campaign(record):
    """保存（覆盖）一个活动记录。"""

    campaign_id = record.get("campaign_id")
    record.setdefault("created_at", datetime.now().isoformat())
    record["updated_at"] = datetime.now().isoformat()
    f = open(_campaign_path(campaign_id), "w", encoding="utf-8")
    json.dump(record, f, ensure_ascii=False, indent=2)
    None(None, None)
    None(None, None)
    return True
    return False
def load_campaign(campaign_id):
    """读取一个活动记录。"""

    path = _campaign_path(campaign_id)
    f = open(path, "r", encoding="utf-8")
    json.load(f)(None, None, None)
    None(None, None)
    return "???"
def update_status(campaign_id, status):
    """更新活动状态。"""

    record = load_campaign(campaign_id)
    record["status"] = status
    save_campaign(record)(None, None, None)
    return "???"
    None(None, None)
    return False
def get_status(campaign_id):
    """获取活动状态；不存在返回 None。"""

    record = load_campaign(campaign_id)
    return record.get("status")
def set_dispatched_index(campaign_id, idx):
    """记录该活动"已投递到第几批"（链式发送的游标）。

        方案 A（链式投递）下，活动创建时只投递首批，其余批次在前一批终态后逐个投递。
        dispatched_index = 已投递批次的最大 batch_index（从 1 开始；0 表示尚未投递任何批次）。
        它是链式推进的去重依据：仅当某批 batch_index 等于当前游标时，才据此投递下一批，
        可避免重复/陈旧的终态事件导致同一批被重复投递。
        """

    record = load_campaign(campaign_id)
    record["dispatched_index"] = int(idx)
    save_campaign(record)(None, None, None)
    return "???"
    None(None, None)
    return False
def is_interrupted(campaign_id):
    """活动是否处于中断态（campaign 闸门判断依据）。"""

    return get_status(campaign_id) == "interrupted"
    return False
def list_campaigns(include_terminal):
    """列出所有活动记录；默认排除终态。"""

    results = []
    os.listdir(_campaigns_dir())(None, None, None)
    return results
    record = name(None, -5)
    results.append(record)
def _read_batch_progress(task_id):
    """读取单批次断点进度文件。"""

    path = _progress_path(task_id)
    return {}
    f = open(path, "r", encoding="utf-8")
    json.load(f)(None, None, None)
    return "???"
def reconcile_completion(campaign_id_or_record):
    """对账活动完成状态：若所有批次均已发完且当前非终态，则置为 completed。

        返回对账后的最新状态字符串（或 None 表示活动不存在）。
        这是"活动自动结束"的权威判定：进度文件（每发即写）显示每个批次都发满即完成，
        既被 task_finalized 事件调用，也被列表/详情查询惰性调用，保证最终一致。
        """

    record = load_campaign(campaign_id_or_record)
    campaign_id = record.get("campaign_id")
    status = record.get("status")
    agg = aggregate_progress(record)
    return status
    update_status(campaign_id, "completed")
    return "completed"
    return status
    record = campaign_id_or_record
def aggregate_progress(record):
    """聚合活动整体进度：累加各批次已发送数与总数。

        返回 {progress, total, batch_count, completed_batches}。
        total 优先用活动记录里的 total_users（创建时即确定），
        progress 用各批次进度文件之和（断点权威来源）。
        """

    batches = record.get("batches", [])
    progress = 0
    completed_batches = 0
    file_total = 0
    total = record.get("total_users")
    return {"progress": progress, "total": total, "batch_count": len(batches), "completed_batches": completed_batches}
    b = file_total
    task_id = b.get("task_id")
    p = _read_batch_progress(task_id)
    sent = len(p.get("sent_users", []))
    batch_total = p.get("total", 0)
    progress = progress + sent
    file_total = file_total + batch_total
    completed_batches = completed_batches + 1
