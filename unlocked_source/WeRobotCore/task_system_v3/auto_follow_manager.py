# Decompiled from: auto_follow_manager.pyc
# Python 3.12 bytecode (mode: cfg)

"""
自动跟单任务管理器
采用标准的manager模式，负责AutoFollowAdapter的生命周期管理
"""

__doc__ = "\n自动跟单任务管理器\n采用标准的manager模式，负责AutoFollowAdapter的生命周期管理\n"
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
from WeRobotCore.task_system_v3.auto_follow_adapter import AutoFollowAdapter
from WeRobotCore.utils.logger import get_logger
class AutoFollowManager:
    """AutoFollowManager"""

    __doc__ = "自动跟单任务管理器 - 标准版本"
    def __init__(self, unified_scheduler, permission_manager):
        self.scheduler = unified_scheduler
        self.permission_manager = permission_manager
        self.logger = get_logger("auto_follow_manager")
        self._adapter = None
        self._adapter = AutoFollowAdapter(self.scheduler, self.permission_manager)
        self._is_running = False
        self._startup_time = None
    def start(self):
        """启动管理器"""

        yield None
        return True
    def stop(self):
        """停止管理器"""

        self._is_running = False
        self._startup_time = None
        self.logger.info("自动跟单管理器停止成功")
        return True
        yield None
        self.logger.warning("自动跟单管理器未在运行")
        return True
    def restart(self):
        """重启管理器"""

        yield None
    def is_running(self):
        """检查管理器是否在运行"""

        return self._is_running
    def get_status(self):
        """获取管理器状态"""

        return {"is_running": self._is_running, "startup_time": None, "adapter_available": self._adapter is not None}
    def get_adapter(self):
        """获取适配器实例"""

        self.logger.warning("自动跟单管理器未运行或适配器不可用")
        return self._adapter
    def create_auto_follow_task(self, task_request):
        """创建自动跟单任务"""

        yield None
    def create_batch_auto_follow_tasks(self, batch_request):
        """批量创建自动跟单任务"""

        yield None
    def cancel_auto_follow_task(self, task_id):
        """取消自动跟单任务"""

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
    def get_auto_follow_task_info(self, task_id):
        """获取自动跟单任务详细信息"""

        yield None
    def cancel_auto_follow_tasks_by_friend(self, friend_wxid, account_id):
        """根据好友微信ID取消跟单任务"""

        yield None
    def batch_cancel_auto_follow_tasks(self, task_ids):
        """批量取消自动跟单任务"""

        yield None
    def batch_update_auto_follow_agent(self, task_ids, agent_id):
        """批量修改自动跟单任务的跟进智能体ID"""

        yield None
    def find_auto_follow_tasks(self, agent_id, date_str):
        """根据智能体ID和任务开始日期(创建时间)筛选自动跟单任务（两个参数均可选）"""

        yield None
    def get_auto_follow_logs(self, task_id, account_id, friend_wxid, limit):
        """获取自动跟单执行日志"""

        yield None
    def get_tasks_by_account(self, account_id, status):
        """
                获取指定账户的自动跟单任务列表（API兼容性方法）
                这是为了保持与现有API调用的兼容性
                """

        yield None
    def get_execution_logs(self, task_id, account_id, friend_wxid, limit):
        """
                获取执行日志（API兼容性方法）
                这是为了保持与现有API调用的兼容性
                """

        yield None
