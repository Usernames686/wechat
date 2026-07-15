# Decompiled from: moment_post_manager.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Dict, Any, Optional, List
from datetime import datetime
from WeRobotCore.task_system_v3.unified_manager_pattern import BaseManagerV3
from WeRobotCore.task_system_v3.types import ScheduleConfig, TriggerType, ExecutionMode, TaskType
from WeRobotCore.task_system_v3.moment_post_adapter import MomentPostAdapter
class MomentPostManager(BaseManagerV3):
    """MomentPostManager"""

    def __init__(self, scheduler, permission_manager):
        super().__init__(scheduler, permission_manager)
        self.adapter = MomentPostAdapter(self.scheduler, self.permission_manager)
        self._is_running = False
        self._startup_time = None
        from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
        self.permission_manager = get_permission_manager()
        from WeRobotCore.task_system_v3.unified_scheduler import UnifiedScheduler
        self.scheduler = UnifiedScheduler()
    def start(self):
        yield None
        return True
    def stop(self):
        self._is_running = False
        return True
    def pause(self):
        return True
    def resume(self):
        return True
    def get_status(self):
        return {"is_running": self._is_running, "startup_time": None}
        return {"is_running": "???", "startup_time": self._startup_time.isoformat()}
    def create_tasks(self, params):
        yield None
    def post_moment_direct(self, content, material_folder):
        yield None
    def get_tasks(self):
        yield None
    def cancel_task(self, task_id):
        yield None
    __classcell__ = __class__
    return __class__
