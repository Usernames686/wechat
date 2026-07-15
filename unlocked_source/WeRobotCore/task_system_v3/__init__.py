# Decompiled from: __init__.pyc
# Python 3.12 bytecode (mode: cfg)

"""Task System V3 - 基于APScheduler 4.0的新一代任务调度系统

这是对现有task_system_v2的重构，目标是：
1. 保持与v2系统的兼容性
2. 提供更强大的调度能力
3. 简化权限管理

核心组件：
- UnifiedScheduler: 统一调度器，封装APScheduler 4.0
- PermissionManager: 权限管理器，维护互斥执行机制
- Manager+Adapter: 管理器+适配器模式，兼容现有任务
"""

__doc__ = "Task System V3 - 基于APScheduler 4.0的新一代任务调度系统\n\n这是对现有task_system_v2的重构，目标是：\n1. 保持与v2系统的兼容性\n2. 提供更强大的调度能力\n3. 简化权限管理\n\n核心组件：\n- UnifiedScheduler: 统一调度器，封装APScheduler 4.0\n- PermissionManager: 权限管理器，维护互斥执行机制\n- Manager+Adapter: 管理器+适配器模式，兼容现有任务\n"
__version__ = "3.0.0-alpha"
__all__ = ("TaskType", "TaskStatus", "TaskPriority", "SchedulerType", "ExecutionMode", "TriggerType", "PermissionLevel", "ScheduleConfig", "TaskExecutionContext", "PermissionRequest", "SchedulerState", "SchedulerStatus", "UnifiedScheduler", "PermissionManager", "MassSendingAdapter", "MassSendingManager", "AutoReplyAdapterV3", "AutoReplyManager", "MomentCommentAdapter", "MomentCommentManager", "create_moment_comment_manager", "FriendRequestAdapter", "FriendRequestManager", "create_friend_request_manager", "AddFriendAdapter", "AddFriendManager", "AutoFollowAdapter", "AutoFollowManager", "SyncContactsAdapter", "SyncContactsManager", "MomentPostAdapter", "MomentPostManager", "get_moment_post_manager", "get_auto_reply_manager", "get_friend_request_manager", "get_mass_sending_manager", "get_moment_comment_manager", "get_moment_post_manager", "get_add_friend_manager", "get_sync_contacts_manager", "get_scheduler")
