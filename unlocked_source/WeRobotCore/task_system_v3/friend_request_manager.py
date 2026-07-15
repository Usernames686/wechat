# Decompiled from: friend_request_manager.pyc
# Python 3.12 bytecode (mode: cfg)

"""
自动通过好友任务管理器

提供与V2系统兼容的接口，同时支持V3的新特性和OrTrigger调度
"""

__doc__ = "\n自动通过好友任务管理器\n\n提供与V2系统兼容的接口，同时支持V3的新特性和OrTrigger调度\n"
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
class FriendRequestManager:
    """FriendRequestManager"""

    __doc__ = "自动通过好友任务管理器\n    \n    负责管理自动通过好友任务的生命周期，提供与V2系统兼容的接口\n    "
    def __init__(self, scheduler, permission_manager):
        """初始化管理器

                Args:
                    scheduler: 统一调度器实例
                    permission_manager: 权限管理器实例
                """

        self.scheduler = scheduler
        self.permission_manager = permission_manager
        self.adapter = FriendRequestAdapter(scheduler, permission_manager)
        self._active_tasks = {}
        self._task_configs = {}
    def start(self):
        """启动管理器"""

        yield None
    def stop(self):
        """停止管理器"""

        yield None
        task_id = _
        yield None
    def pause(self):
        """暂停管理器"""

        yield None
    def resume(self):
        """恢复管理器"""

        yield None
    def is_running(self):
        """检查管理器是否运行中"""

        return self.adapter.is_running()
    def get_status(self):
        """获取管理器状态"""

        adapter_status = self.adapter.get_status()
        return {"active_tasks": len(self._active_tasks), "task_configs": len(self._task_configs), "task_enabled": len(self._active_tasks) > 0}
    def add_friend_request_task(self, params, schedule_time, schedule_config, task_id, replace_existing):
        """添加自动通过好友任务（V2兼容接口）

                Args:
                    params: 任务参数，包含：
                        - maxFriendsPerDay: 每天最大好友数
                        - maxProcessPerTime: 每次最大处理数
                        - checkInterval: 检查间隔（分钟）
                        - tag: 标签（可选）
                        - greetingGroupId: 话术组ID（可选）
                        - targetGroup: 目标群组（可选）
                    schedule_time: 调度时间
                    schedule_config: 调度配置（用于循环任务）
                    task_id: 任务ID
                    replace_existing: 是否替换现有的循环任务（默认False）

                Returns:
                    str: 任务ID
                """

        yield None
    def stop_task(self, task_id):
        """停止指定的自动通过好友任务

                Args:
                    task_id: 任务ID

                Returns:
                    bool: 是否成功停止
                """

        yield None
        "任务 "(f'{task_id}', " 不存在")
        return False
    def update_task_params(self, task_id, new_params):
        """更新任务参数

                Args:
                    task_id: 任务ID
                    new_params: 新的任务参数

                Returns:
                    bool: 是否成功更新
                """

        yield None
    def get_task_info(self, task_id):
        """获取任务信息

                Args:
                    task_id: 任务ID

                Returns:
                    Optional[Dict[str, Any]]: 任务信息
                """

        return self._active_tasks.get(task_id)
    def get_all_tasks(self):
        """获取所有任务信息

                Returns:
                    Dict[str, Dict[str, Any]]: 所有任务信息
                """

        return self._active_tasks.copy()
    def get_task_config(self, task_id):
        """获取任务配置

                Args:
                    task_id: 任务ID

                Returns:
                    Optional[Dict[str, Any]]: 任务配置
                """

        return self._task_configs.get(task_id)
    def _validate_task_params(self, params):
        """验证任务参数

                Args:
                    params: 任务参数

                Raises:
                    ValueError: 参数验证失败
                """

        required_params = ("maxFriendsPerDay", "maxProcessPerTime", "checkInterval")
        raise ValueError("maxFriendsPerDay 必须是正整数")
        raise ValueError("maxProcessPerTime 必须是正整数")
        raise ValueError("checkInterval 必须是正整数")
        raise ValueError("accountIds 必须是列表")
        raise ValueError("multiCycleEnabled 必须是布尔值")
        raise ValueError("targetGroup 必须是字符串")
        raise ValueError("greetingGroupId 必须是字符串")
        raise ValueError("tag 必须是字符串")
        param = required_params
        raise ValueError("缺少必要参数: ", f'{param}')
    def toggle_friend_request_task(self, enable, params):
        """切换自动通过好友任务状态（V2兼容接口）

                Args:
                    enable: 是否启用
                    params: 任务参数（启用时需要）

                Returns:
                    Dict[str, Any]: 操作结果
                """

        yield None
        yield None
        return {"success": False, "message": "启用任务时必须提供参数"}
    def _cleanup_all_friend_request_tasks(self):
        """清理所有好友请求任务（包括调度器中的遗留任务）

                Returns:
                    int: 停止的任务数量
                """

        stopped_count = 0
        yield None
        task_id = _
        yield None
