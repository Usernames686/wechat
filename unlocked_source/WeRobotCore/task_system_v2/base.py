# Decompiled from: base.pyc
# Python 3.12 bytecode (mode: cfg)

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
class TaskType(Enum):
    """TaskType"""

    AUTO_REPLY = "auto_reply"
    FRIEND_REQUEST = "friend_request"
    MASS_SENDING = "mass_sending"
    TIMED_TASK = "timed_task"
    ADD_FRIEND = "add_friend"
    MOMENT_COMMENT = "moment_comment"
    MOMENT_POST = "moment_post"
    CHAT_COLLECTION = "chat_collection"
    AUTO_FOLLOW = "auto_follow"
    SYNC_CONTACTS = "sync_contacts"
    SOP_FLOW = "sop_flow"
class TaskPriority(Enum):
    """TaskPriority"""

    LOW = 0
    MEDIUM = 1
    HIGH = 2
class TaskStatus(Enum):
    """TaskStatus"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING_CONFIRMATION = "pending_confirmation"
    PAUSED = "paused"
    PENDING_AGENT = "pending_agent"
class BaseTask:
    """BaseTask"""

    def __init__(self, task_id, task_type, params, schedule_time, priority):
        self.id = task_id
        self.type = task_type
        self.params = params
        self.schedule_time = schedule_time
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.error = None
        self.result = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.run_index = 1
        self.correlation_id = "_run1"
    def execute(self):
        """执行任务的抽象方法"""

        raise NotImplementedError
    def to_dict(self):
        """将任务转换为字典格式"""

        return {"id": self.id, "type": self.type.value, "params": self.params, "schedule_time": None, "priority": self.priority.value, "status": self.status.value, "error": None, "result": self.result, "created_at": self.created_at.isoformat(), "started_at": None, "completed_at": None}
        return {"id": "???", "type": "???", "params": "???", "schedule_time": "???", "priority": "???", "status": "???", "error": "???", "result": "???", "created_at": "???", "started_at": "???", "completed_at": self.completed_at.isoformat()}
class TimedBaseTask(BaseTask):
    """TimedBaseTask"""

    __doc__ = "定时任务基类"
    def __init__(self, task_id, task_type, params, schedule_time, schedule_config, is_recurring, priority):
        super().__init__(task_id, task_type, params, priority)
        self.schedule_time = schedule_time
        self.schedule_config = schedule_config
        self.is_recurring = is_recurring
    def to_dict(self):
        data = super().to_dict()
        data.update({"schedule_time": None, "schedule_config": self.schedule_config, "is_recurring": self.is_recurring})
        return data
    __classcell__ = __class__
    return __class__
