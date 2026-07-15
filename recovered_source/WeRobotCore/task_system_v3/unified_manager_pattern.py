# Decompiled from: unified_manager_pattern.pyc
# Python 3.12 bytecode (mode: cfg)

"""
V3框架统一管理器模式规范
======================

本文件定义了V3框架中所有Manager的统一创建和管理规范，
解决当前单例和全局混用的架构不一致问题。

核心设计原则：
1. 统一使用改进的全局管理器模式
2. 保证缓存数据共享和持久性
3. 简化代码复杂度，提高可测试性
4. 渐进式改造，保持向后兼容
"""

__doc__ = "\nV3框架统一管理器模式规范\n======================\n\n本文件定义了V3框架中所有Manager的统一创建和管理规范，\n解决当前单例和全局混用的架构不一致问题。\n\n核心设计原则：\n1. 统一使用改进的全局管理器模式\n2. 保证缓存数据共享和持久性\n3. 简化代码复杂度，提高可测试性\n4. 渐进式改造，保持向后兼容\n"
import asyncio
import logging
from typing import Dict, Any, Optional, TypeVar, Type, Callable
from datetime import datetime
import threading
from abc import ABC, abstractmethod
ManagerType = TypeVar("ManagerType")
class GlobalManagerRegistry:
    """GlobalManagerRegistry"""

    __doc__ = "全局管理器注册表\n    \n    统一管理所有Manager实例，确保：\n    1. 每种Manager类型只有一个全局实例\n    2. 线程安全的实例创建和访问\n    3. 统一的生命周期管理\n    4. 支持测试时的实例重置\n    "
    _instances = {}
    __annotations__["_instances"] = Dict[(str, Any)]
    _locks = {}
    __annotations__["_locks"] = Dict[(str, threading.Lock)]
    _creation_callbacks = {}
    __annotations__["_creation_callbacks"] = Dict[(str, Callable)]
    _main_lock = threading.Lock()
    @classmethod
    def register_manager_type(cls, manager_name, creation_callback):
        """注册管理器类型和创建回调

                Args:
                    manager_name: 管理器名称（如 'auto_reply_manager'）
                    creation_callback: 创建管理器实例的回调函数
                """

        cls._creation_callbacks[manager_name] = creation_callback
        None(None, None)
        cls._locks[manager_name] = threading.Lock()
    @classmethod
    def get_or_create_manager(cls, manager_name):
        """获取或创建管理器实例

                Args:
                    manager_name: 管理器名称
                    *args, **kwargs: 传递给创建回调的参数

                Returns:
                    管理器实例
                """

        creation_callback = cls._creation_callbacks[manager_name]
        instance = creation_callback(*args, **{**{}, **kwargs})
        cls._instances[manager_name] = instance
        instance(None, None, None)
        return "???"
        raise ValueError("未注册的管理器类型: ", f'{manager_name}')
        None(None, None)
        return cls._instances[manager_name]
        None(None, None)
        cls._locks[manager_name] = threading.Lock()
        return cls._instances[manager_name]
    get_manager = classmethod((lambda cls, manager_name: cls._instances.get(manager_name)))
    @classmethod
    def remove_manager(cls, manager_name):
        """移除管理器实例

                Args:
                    manager_name: 管理器名称

                Returns:
                    是否成功移除
                """

        None(None, None)
        return False
        del cls._instances[manager_name]
        None(None, None)
        return True
        return False
    @classmethod
    def shutdown_all_managers(cls):
        """关闭所有管理器实例"""

        managers_to_shutdown = list(cls._instances.items())
        cls._instances.clear()
        managers_to_shutdown(None, None, None)
        manager_name = "???"[0]
        manager = "???"[1]
        manager.stop()
        yield None
    @classmethod
    def reset_for_testing(cls):
        """重置所有实例（仅用于测试）"""

        cls._instances.clear()
        None(None, None)
    get_all_managers = classmethod((lambda cls: cls._instances.copy()))
class BaseManagerV3(ABC):
    """BaseManagerV3"""

    __doc__ = "V3管理器基类\n    \n    定义了所有Manager应该实现的标准接口\n    "
    def __init__(self, scheduler, permission_manager):
        self.scheduler = scheduler
        self.permission_manager = permission_manager
        self._is_running = False
        self._startup_time = None
    @abstractmethod
    def start(self):
        """启动管理器"""
    @abstractmethod
    def stop(self):
        """停止管理器"""
    @abstractmethod
    def pause(self):
        """暂停管理器"""
    @abstractmethod
    def resume(self):
        """恢复管理器"""
    get_status = abstractmethod((lambda self: ...))
    def add_task(self, params, schedule_time):
        """添加任务（标准接口）"""

        raise NotImplementedError("子类必须实现add_task方法")
    def cancel_task(self, task_id):
        """取消任务（标准接口）"""

        raise NotImplementedError("子类必须实现cancel_task方法")
    def get_task(self, task_id):
        """获取任务信息（标准接口）"""

        raise NotImplementedError("子类必须实现get_task方法")
def _start_manager(manager, manager_name):
    """通用的管理器启动函数"""

    manager.start()
    logging.info(f'{manager_name}', "启动成功")
    loop = asyncio.get_running_loop()
    asyncio.create_task(manager.start())
    logging.info(f'{manager_name}', "异步启动任务已创建")
def create_auto_reply_manager(scheduler, permission_manager):
    """内部创建自动回复管理器函数（用于全局注册表）"""

    from WeRobotCore.task_system_v3.auto_reply_manager import AutoReplyManager
    from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
    manager = AutoReplyManager(scheduler, permission_manager)
    return manager
    permission_manager = get_permission_manager()
    scheduler = get_scheduler()
def create_friend_request_manager(scheduler, permission_manager):
    """创建好友请求管理器"""

    from WeRobotCore.task_system_v3.friend_request_manager import FriendRequestManager
    from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
    manager = FriendRequestManager(scheduler, permission_manager)
    return manager
    permission_manager = get_permission_manager()
    scheduler = get_scheduler()
def create_mass_sending_manager(scheduler, permission_manager):
    """创建群发管理器"""

    from WeRobotCore.task_system_v3.mass_sending_manager import MassSendingManager
    from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
    manager = MassSendingManager(scheduler, permission_manager)
    _start_manager(manager, "群发管理器")
    return manager
    permission_manager = get_permission_manager()
    scheduler = get_scheduler()
def create_moment_comment_manager(scheduler, permission_manager):
    """创建朋友圈评论管理器"""

    from WeRobotCore.task_system_v3.moment_comment_manager import MomentCommentManager
    from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
    manager = MomentCommentManager(scheduler, permission_manager)
    return manager
    permission_manager = get_permission_manager()
    scheduler = get_scheduler()
def create_moment_post_manager(scheduler, permission_manager):
    """创建朋友圈评论管理器"""

    from WeRobotCore.task_system_v3.moment_post_manager import MomentPostManager
    from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
    manager = MomentPostManager(scheduler, permission_manager)
    return manager
    permission_manager = get_permission_manager()
    scheduler = get_scheduler()
def create_add_friend_manager(scheduler, permission_manager):
    """创建自动添加好友管理器"""

    from WeRobotCore.task_system_v3.add_friend_manager import AddFriendManager
    from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
    manager = AddFriendManager(scheduler, permission_manager)
    return manager
    permission_manager = get_permission_manager()
    scheduler = get_scheduler()
def create_auto_follow_manager(scheduler, permission_manager):
    """创建自动跟单管理器 V1"""

    from WeRobotCore.task_system_v3.auto_follow_manager import AutoFollowManager
    from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
    manager = AutoFollowManager(scheduler, permission_manager)
    return manager
    permission_manager = get_permission_manager()
    scheduler = get_scheduler()
def create_sync_contacts_manager(scheduler, permission_manager):
    """创建自动同步通讯录管理器"""

    from WeRobotCore.task_system_v3.sync_contacts_manager import SyncContactsManager
    from WeRobotCore.task_system_v3.permission_manager import get_permission_manager
    manager = SyncContactsManager(scheduler, permission_manager)
    return manager
    permission_manager = get_permission_manager()
    scheduler = get_scheduler()
def create_unified_scheduler():
    """创建统一调度器"""

    from WeRobotCore.task_system_v3.unified_scheduler import UnifiedScheduler
    scheduler = UnifiedScheduler()
    return scheduler
def register_all_managers():
    """注册所有管理器类型到全局注册表"""

    GlobalManagerRegistry.register_manager_type("auto_reply_manager", create_auto_reply_manager)
    GlobalManagerRegistry.register_manager_type("friend_request_manager", create_friend_request_manager)
    GlobalManagerRegistry.register_manager_type("mass_sending_manager", create_mass_sending_manager)
    GlobalManagerRegistry.register_manager_type("moment_comment_manager", create_moment_comment_manager)
    GlobalManagerRegistry.register_manager_type("moment_post_manager", create_moment_post_manager)
    GlobalManagerRegistry.register_manager_type("add_friend_manager", create_add_friend_manager)
    GlobalManagerRegistry.register_manager_type("auto_follow_manager", create_auto_follow_manager)
    GlobalManagerRegistry.register_manager_type("sync_contacts_manager", create_sync_contacts_manager)
    GlobalManagerRegistry.register_manager_type("unified_scheduler", create_unified_scheduler)
def get_auto_reply_manager(scheduler, permission_manager):
    """获取自动回复管理器全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("auto_reply_manager", scheduler, permission_manager)
def get_friend_request_manager(scheduler, permission_manager):
    """获取好友请求管理器全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("friend_request_manager", scheduler, permission_manager)
def get_mass_sending_manager():
    """获取群发管理器全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("mass_sending_manager")
def get_moment_comment_manager(scheduler, permission_manager):
    """获取朋友圈评论管理器全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("moment_comment_manager", scheduler, permission_manager)
def get_moment_post_manager(scheduler, permission_manager):
    """获取朋友圈评论管理器全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("moment_post_manager", scheduler, permission_manager)
def get_add_friend_manager(scheduler, permission_manager):
    """获取自动添加好友管理器全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("add_friend_manager", scheduler, permission_manager)
def get_auto_follow_manager(scheduler):
    """获取自动跟单管理器 V1 全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("auto_follow_manager", scheduler)
def get_sync_contacts_manager(scheduler, permission_manager):
    """获取自动同步通讯录管理器全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("sync_contacts_manager", scheduler, permission_manager)
def get_scheduler():
    """获取统一调度器全局实例"""

    return GlobalManagerRegistry.get_or_create_manager("unified_scheduler")
def initialize_all_managers_and_process_tasks():
    """初始化所有管理器并处理已存在的任务

        这个函数确保所有adapter都已注册自动恢复任务类型后，再处理已存在的持久化任务
        """

    register_all_managers()
    scheduler = get_scheduler()
    managers = [get_auto_reply_manager(), get_friend_request_manager(), get_mass_sending_manager(), get_moment_comment_manager(), get_moment_post_manager(), get_add_friend_manager(), get_auto_follow_manager(), get_sync_contacts_manager()]
    yield None
print("所有管理器: ", f'{GlobalManagerRegistry.get_all_managers()}')
