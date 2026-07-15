# Decompiled from: auto_reply_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

"""
自动回复任务适配器 - V3系统

完全兼容V2自动回复任务的业务逻辑，包括：
1. 账号分区管理
2. 消息缓存和去重
3. 任务聚合机制
4. 状态管理和生命周期
5. 错误处理和恢复
"""

__doc__ = "\n自动回复任务适配器 - V3系统\n\n完全兼容V2自动回复任务的业务逻辑，包括：\n1. 账号分区管理\n2. 消息缓存和去重\n3. 任务聚合机制\n4. 状态管理和生命周期\n5. 错误处理和恢复\n"
import asyncio
import re
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field
from WeRobotCore.task_system_v3.types import TaskType, TaskStatus, TaskPriority, ScheduleConfig, TaskExecutionContext, TriggerType, ExecutionMode, PermissionLevel, PermissionRequest
from WeRobotCore.task_system_v2.base import BaseTask
from WeRobotCore.utils.logger import task_logger, get_logger
class AccountPartition:
    """AccountPartition"""

    __doc__ = "账号分区 - 优化版本，减少内存开销"
    __annotations__["account_id"] = Optional[str]
    task_map = field(default_factory=dict)
    __annotations__["task_map"] = Dict[(str, BaseTask)]
    message_cache = field(default_factory=dict)
    __annotations__["message_cache"] = Dict[(int, Dict)]
    last_reply_cache = field(default_factory=dict)
    __annotations__["last_reply_cache"] = Dict[(int, str)]
    suspended_sessions = field(default_factory=dict)
    __annotations__["suspended_sessions"] = Dict[(str, float)]
    _last_cleanup = field(default_factory=lambda : datetime.now().timestamp())
    __annotations__["_last_cleanup"] = float
    def __post_init__(self):
        """初始化后处理"""

        self.suspended_sessions = {}
        self.last_reply_cache = {}
        self.message_cache = {}
        self.task_map = {}
    def should_cleanup(self):
        """检查是否需要清理过期数据"""

        current_time = datetime.now().timestamp()
        return current_time - self._last_cleanup > 300
    def cleanup_expired_data(self):
        """清理过期数据，减少内存占用"""

        current_time = datetime.now().timestamp()
        expired_sessions = []
        completed_tasks = []
        self._last_cleanup = current_time
        return len(expired_sessions) + len(completed_tasks)
        return 0
        session_name = completed_tasks
        del self.task_map[session_name]
        session_name = self.task_map.items()[0]
        task = self.task_map.items()[1]
        completed_tasks.append(session_name)
        session_id = expired_sessions
        del self.message_cache[session_id]
        del self.last_reply_cache[session_id]
        session_id = self.message_cache.items()[0]
        cache_data = self.message_cache.items()[1]
        expired_sessions.append(session_id)
    def get_components(self):
        """获取分区组件 - 兼容V2版本接口"""

        from WeRobotCore.utils.config_manager import ConfigManager
        from WeRobotCore.core.WeChatType import WeChat
        wechat = WeChat()
        config_manager = ConfigManager()
        return {"wechat": wechat, "config": config_manager}
        wechat = WeChat(account_id=self.account_id)
        config_manager = ConfigManager(user_id=self.account_id)
class AutoReplyAdapterV3:
    """AutoReplyAdapterV3"""

    __doc__ = "自动回复任务适配器 V3版本"
    def __init__(self, unified_scheduler, permission_manager):
        self.scheduler = unified_scheduler
        self.permission_manager = permission_manager
        self.logger = get_logger("auto_reply_adapter_v3")
        self.task_logger = task_logger
        self._partitions = {}
        self._partition_lock = asyncio.Lock()
        self._task_instances = {}
        self._task_instance_timestamps = {}
        self._execution_contexts = {}
        self._max_cached_instances = 100
        self._instance_ttl = 1800
        self._message_num_lock = asyncio.Lock()
        self._mass_sending_cache = {}
        self._cache_lock = asyncio.Lock()
        self._greeted_join_groups = {}
        self._greeted_join_ttl = 120
        self._friend_pass_sop = {}
        self._friend_pass_sop_ttl = 300
        self._new_contact_bypass = {}
        self._new_contact_bypass_ttl = 300
        self._confirmed_non_group = {}
        self._confirmed_non_group_ttl = 1800
        self._running = False
        self._paused = False
        self.scheduler.register_task_executor(TaskType.AUTO_REPLY, self.execute_task)
        self.scheduler.register_task_executor(TaskType.SOP_FLOW, self.execute_sop_task)
    def start(self):
        """启动适配器"""

        self._running = True
        self._paused = False
        self.logger.info("自动回复适配器启动..")
        return True
        self.logger.info("自动回复适配器已在运行")
        return True
    def stop(self):
        """停止适配器"""

        self._running = False
        self._task_instances.clear()
        self._execution_contexts.clear()
        self._greeted_join_groups.clear()
        self._friend_pass_sop.clear()
        self._confirmed_non_group.clear()
        return True
        partition = self._partitions.values()
        partition.suspended_sessions.clear()
        task_id = self._task_instances.items()[0]
        task = self._task_instances.items()[1]
        task.status = TaskStatus.CANCELLED
        return True
    def pause(self):
        """暂停适配器"""

        self._paused = True
        self.logger.info("自动回复适配器已暂停")
    def resume(self):
        """恢复适配器"""

        self._paused = False
        self.logger.info("自动回复适配器已恢复")
        yield None
    def get_account_partition(self, account_id):
        """获取账号分区（兼容V2逻辑）"""

        partition = self._partitions[account_id]
        return partition
        cleaned_count = partition.cleanup_expired_data()
        " 清理了 "(f'{cleaned_count}', " 个过期项")
        self._partitions[account_id] = AccountPartition(account_id=account_id)
    def suspend_session(self, account_id, session_name):
        """挂起会话"""

        partition = self.get_account_partition(account_id)
        partition.suspended_sessions[session_name] = datetime.now().timestamp()
        " 会话 "(f'{session_name}', " 已挂起")
        return True
    def unsuspend_session(self, account_id, session_name):
        """解除会话挂起"""

        partition = self.get_account_partition(account_id)
        return False
        del partition.suspended_sessions[session_name]
        " 会话 "(f'{session_name}', " 已解除挂起")
        return True
    def is_session_suspended(self, account_id, session_name):
        """检查会话是否被挂起"""

        partition = self.get_account_partition(account_id)
        return session_name in partition.suspended_sessions
    def clear_all_suspended_sessions(self):
        """清除所有挂起会话

                Returns:
                    int: 被清除的会话总数
                """

        count = 0
        "已清除所有挂起会话，共 "(f'{count}', " 个")
        return count
        partition = self.logger.info
        count = count + len(partition.suspended_sessions)
        partition.suspended_sessions.clear()
    def get_suspended_sessions(self, account_id):
        """获取挂起会话列表
                Args:
                    account_id: 指定账号ID，如果为None则返回所有账号的挂起会话
                Returns:
                    List[Dict]: 挂起会话列表，包含 session_name, suspended_at, account_id
                """

        result = []
        return result
        acc_id = self._partitions.items()[0]
        partition = self._partitions.items()[1]
        name = partition.suspended_sessions.items()[0]
        ts = partition.suspended_sessions.items()[1]
        result.append({"session_name": name, "suspended_at": ts, "account_id": acc_id})
        partition = self.get_account_partition(account_id)
        return result
        name = partition.suspended_sessions.items()[0]
        ts = partition.suspended_sessions.items()[1]
        result.append({"session_name": name, "suspended_at": ts, "account_id": account_id})
    def _get_auto_reply_task_class(self):
        """延迟导入AutoReplyTask类，避免循环导入"""

        from WeRobotCore.task_system_v2.tasks.auto_reply_task import AutoReplyTask
        return AutoReplyTask
    def _cleanup_task_instances(self):
        """清理过期的任务实例缓存"""

        current_time = datetime.now().timestamp()
        expired_tasks = []
        "清理了 "(f'{len(expired_tasks)}', " 个过期任务实例")
        sorted_tasks = sorted(self._task_instance_timestamps.items(), key=lambda x: x[1])
        tasks_to_remove = len(self._task_instances) - self._max_cached_instances
        i = range(tasks_to_remove)
        task_id = sorted_tasks[i][0]
        del self._execution_contexts[task_id]
        del self._task_instance_timestamps[task_id]
        del self._task_instances[task_id]
        task_id = self.logger.debug
        del self._execution_contexts[task_id]
        del self._task_instance_timestamps[task_id]
        del self._task_instances[task_id]
        task_id = NULL[0]
        timestamp = NULL[1]
        expired_tasks.append(task_id)
    def _cache_task_instance(self, task_id, task_instance):
        """缓存任务实例"""

        self._task_instances[task_id] = task_instance
        self._task_instance_timestamps[task_id] = datetime.now().timestamp()
        self._cleanup_task_instances()
    def _get_cached_task_instance(self, task_id):
        """获取缓存的任务实例"""

        self._task_instance_timestamps[task_id] = datetime.now().timestamp()
        return self._task_instances[task_id]
    def add_task(self, account_id, params, schedule_time):
        """添加自动回复任务（兼容AutoReplyManager调用）

                Args:
                    account_id: 账号ID
                    params: 任务参数
                    schedule_time: 调度时间（可选）

                Returns:
                    Optional[str]: 任务ID，失败时返回None
                """

        AutoReplyTask = self._get_auto_reply_task_class()
        task = uuid.uuid4().hex(None, task_id=f'{8}', params=params, account_id=account_id, schedule_time=schedule_time)
        yield None
    def add_auto_reply_task(self, task):
        """添加自动回复任务（兼容V2的去重和聚合逻辑）"""

        session_name = task.params.get("session_name")
        account_id = getattr(task, "account_id", None)
        partition = self.get_account_partition(account_id)
        yield None
        self.logger.warning("缺少会话名称，任务添加失败")
    def _pre_check_task(self, task, partition):
        """任务前置检查（完全兼容V2逻辑）"""

        params = task.params
        session_id = params.get("session_id")
        message = params.get("message")
        session_name = params.get("session_name")
        is_group = params.get("is_group", False)
        user_name = params.get("user_name")
        is_at = params.get("is_at", False)
        account_id = params.get("account_id")
        components = partition.get_components()
        config_manager = components["config"]
        wechat_instance = components["wechat"]
        account_id = None
        agent_result = config_manager.get_agent_id_by_tags(account_id, session_name, is_group)
        agent_id = agent_result.get("agent_id")
        user_exists_in_db = agent_result.get("user_exists_in_db", True)
        return True
        "没有配置 "(f'{user_name}', " 对应标签的AI助理，跳过回复")
        return False
        self.logger.info("没有配置群聊的AI助理，跳过回复: ", f'{session_name}')
        return False
        "检测到新用户 "(f'{user_name}', "，将在任务处理阶段获取用户信息")
        return True
        "没有配置 "(f'{user_name}', " 对应标签的AI助理，跳过回复")
        return False
        self.logger.info("没有配置群聊的AI助理，跳过回复: ", f'{session_name}')
        return False
        self.logger.info("全新联系人会话(未入库)，放行至执行阶段好友通过识别: ", f'{session_name}')
        return True
        self.logger.info("会话类型未确认(可能是新群)，放行至开窗确认: ", f'{session_name}')
        return True
        whitelist = config_manager.get_whitelist()
        f'{whitelist}'(",", f'{session_name}')
        "会话 "(f'{session_name}', " 不在白名单中，跳过处理")
        return False
        colleague_names_str = config_manager.get_colleague_names_to_ignore()
        self.logger.info("群聊消息未被@，跳过回复: ", f'{message}')
        return False
        colleague_list = colleague_names_str.split("//")
        name = []
        "' 的同事 '"(f'{user_name}', "' 消息")
        return False
        name = f'{session_name}'
        self.logger.info("没有活跃的AI助理")
        return False
        self.logger.info("好友通过标志消息，放行至执行阶段事件识别: ", f'{session_name}')
        return True
        "会话 "(f'{session_name}', " 处于挂起状态，跳过回复")
        return False
        self.logger.info("跳过推送消息: ", f'{message}')
        return False
        self.logger.info("跳过官方账号消息: ", f'{session_name}')
        return False
        self.logger.info("跳过自动回复消息: ", f'{message}')
        return False
        self.logger.info("跳过撤回消息提示: ", f'{message}')
        return False
        f'{message}'(", session_name=", f'{session_name}')
        return False
    def _is_type_unknown_session(self, config_manager, account_id, session_name):
        """判断会话是否"类型未确认"、需放行到开窗阶段用权威类型重判。

                条件（需全部满足）：
                - 本账号配置了群聊助理（否则开窗也不可能命中群聊助理，纯属浪费）；
                - 会话不在群缓存中（已知群无需重判，且已知群会被直接按群处理）；
                - 会话不是已知单聊联系人（只有全新会话才可能是尚未识别的新群）；
                - 近期未被开窗确认为非群聊（TTL 内不对同一会话反复开窗）。
                """

        last_ts = self._confirmed_non_group.get((account_id, session_name))
        return True
        return False
        return False
        return False
        return False
    def _is_unsynced_new_contact(self, config_manager, account_id, session_name):
        """单聊会话是否为"尚未入库的全新联系人"（疑似刚通过的新好友）。

                条件（需全部满足）：
                - 配置了好友通过SOP或旧版自动打招呼（否则放行到执行阶段也无事可做，纯属浪费开窗）；
                - 会话不在群缓存中且不是已知单聊联系人（联系人同步是定时任务，
                  刚通过的新好友尚不在 friends 表中，恰好以此识别全新会话）；
                - TTL 内未放行过（事件识别一次就够，避免对同一会话反复开窗）。
                命中后立即记入 TTL 缓存。
                """

        key = (account_id, session_name)
        now = datetime.now().timestamp()
        last_ts = self._new_contact_bypass.get(key)
        self._new_contact_bypass[key] = now
        return True
        return False
        return False
        return False
        return False
    def _is_auto_reply_message_in_partition(self, session_id, message, partition):
        """检查是否是自动回复消息（使用分区缓存）"""

        cache = partition.message_cache.get(session_id)
        return False
        normalized_message = message.replace("\n", "").replace("﻿", "").strip()
        normalized_replies = cache["reply_messages"]
        reply = []
        return normalized_message in normalized_replies
        base = -3
        last_reply = ""
        return last_reply.startswith(base)
        reply = normalized_replies[-1]
    def _normalize_ref_content(self, content):
        """标准化消息内容，用于去重比较"""

        text = content.replace("\n", "").replace("\r", "").replace("﻿", "").strip()
        return text
        text = -3
        return ""
    def _pre_execution_check(self, task):
        """任务执行前的二次检查，防止已被过滤的任务继续执行"""

        partition = self.get_account_partition(task.account_id)
        components = partition.get_components()
        config_manager = components["config"]
        wechat_instance = components.get("wechat")
        params = task.params
        message = params.get("message")
        session_name = params.get("session_name")
        is_group = params.get("is_group", False)
        user_name = params.get("user_name")
        is_at = params.get("is_at", False)
        resolved_account_id = task.account_id
        agent_result = config_manager.get_agent_id_by_tags(resolved_account_id, session_name, is_group)
        return True
        self.logger.info("[二次检查]开窗确认为单聊但无匹配单聊助理，跳过回复: ", f'{session_name}')
        return False
        self.logger.info("[二次检查]开窗确认为群聊但无匹配群聊助理，跳过回复: ", f'{session_name}')
        return False
        resolved_account_id = wechat_instance.account_info.get("account_id")
        self.logger.debug("[任务执行情二次检查]执行前检查：跳过官方账号消息")
        return False
        colleague_names_str = config_manager.get_colleague_names_to_ignore()
        print("[任务执行情二次检查]群聊消息未被@，跳过回复: ", f'{message}')
        return False
        colleague_list = colleague_names_str.split("//")
        name = []
        "' 的同事 '"(f'{user_name}', "' 消息")
        return False
        name = f'{session_name}'
        "[任务执行前二次检查]会话 "(f'{params.get("session_name")}', " 处于挂起状态，跳过执行")
        return False
    def _is_official_account(self, session_name):
        """检查是否为官方账号（兼容V2逻辑）"""

        normalized_name = session_name.strip()
        strong_match_keywords = {"微信团队", "微信支付"}
        strict_patterns = ("^[\\[(（【]?\\s*公众号\\s*[\\])）】]?$", "^[\\[(（【]?\\s*服务号\\s*[\\])）】]?$", "^[\\[(（【]?\\s*微信游戏\\s*[\\])）】]?$", "^[\\[(（【]?\\s*服务通知\\s*[\\])）】]?$", "^[\\[(（【]?\\s*微信支付商家助手\\s*[\\])）】]?$", "^[\\[(（【]?\\s*小程序助手\\s*[\\])）】]?$")
        return any((pattern for pattern in _iter)(strict_patterns))
        return True
        return False
    def _is_mass_sending_message(self, session_name, message):
        """检查是否是推送消息（使用v3缓存机制）"""

        cache = self._mass_sending_cache.get(session_name)
        normalized_message = message.replace("\n", "").replace("﻿", "").strip()
        normalized_cache = cache.get("messages", [])
        m = []
        return normalized_message in normalized_cache
        base = -3
        return any((cm for cm in _iter)(normalized_cache))
        m = None
        return False
    def cache_mass_sending_message(self, session_name, message):
        """缓存推送消息，用于避免自动回复（兼容V2接口）"""

        yield None
    def clear_mass_sending_cache(self, session_name):
        """清理推送消息缓存（兼容V2接口）"""

        yield None
    def _clean_expired_cache(self, expire_seconds):
        """清理过期的推送消息缓存"""

        current_time = datetime.now().timestamp()
        expired_sessions = self._mass_sending_cache.items()
        session_name = []
        cache = session_name
        f'{expire_seconds}'("秒): ", f'{expired_sessions}')
        session_name = "清理过期推送缓存("
        del self._mass_sending_cache[session_name]
        session_name = self.logger.debug[0]
        cache = self.logger.debug[1]
    def schedule_clear_mass_sending_cache(self, delay_seconds):
        """延迟清空所有推送消息缓存（兼容V2接口）"""

        "启动推送缓存清理倒计时: "(f'{delay_seconds}', "秒后清空所有缓存")
        yield None
    def start_clear_cache_countdown(self, delay_seconds):
        """启动推送缓存清理倒计时（非阻塞，兼容V2接口）"""

        asyncio.create_task(self.schedule_clear_mass_sending_cache(delay_seconds))
    def execute_task(self, context, params):
        """执行自动回复任务（完全兼容V2执行逻辑）"""

        self.logger.debug("开始执行自动回复任务 ", f'{context.task_id}')
        task_instance = self._get_cached_task_instance(context.task_id)
        self._execution_contexts[context.task_id] = context
        task_instance.status = TaskStatus.RUNNING
        task_instance.started_at = datetime.now()
        self.logger.debug("开始执行任务：", f'{task_instance.params.get("session_name")}')
        t_prepare_start = datetime.now().timestamp()
        yield None
        yield None
    def _resolve_monitor_only(self, task_instance):
        """解析当前会话命中的AI助理是否为"仅监控"模式。

                仅监控：该助理只监听消息、参与事件识别（如新进群），但不实际调用智能体生成并发送回复。
                """

        account_id = getattr(task_instance, "account_id", None)
        partition = self.get_account_partition(account_id)
        components = partition.get_components()
        config_manager = components["config"]
        wechat_instance = components["wechat"]
        resolved_account_id = None
        session_name = task_instance.params.get("session_name")
        is_group = task_instance.params.get("is_group", False)
        agent_result = config_manager.get_agent_id_by_tags(resolved_account_id, session_name, is_group)
        return bool(agent_result)
        resolved_account_id = wechat_instance.account_info.get("account_id")
    def _save_monitor_chat_history(self, task_instance):
        """仅监控模式下保存最新聊天记录（充当聊天记录员）。

                - 仅监控助理不调用智能体回复，但需把本次拉取到的完整消息落库，
                  供后续群聊分析、群运营等场景使用；
                - 复用回复路径相同的 ChatHistoryManager.save_messages，依赖消息指纹去重，
                  重复保存不会产生脏数据；
                - 消息已在 _prepare_task_messages 阶段拉取并写入 params['all_messages']，此处直接复用，不再触发UIA读取。
                """

        session_name = task_instance.params.get("session_name")
        all_messages = task_instance.params.get("all_messages")
        account_id = getattr(task_instance, "account_id", None)
        is_group = task_instance.params.get("is_group", False)
        from WeRobotCore.utils.chat_history import ChatHistoryManager
        chat_history = ChatHistoryManager(account_id)
        yield None
        self.logger.debug("[仅监控] 无账号ID，跳过保存聊天记录: ", f'{session_name}')
    def _handle_first_join_greeting(self, task_instance):
        """检测到本账号首次进群后，按"新建群聊执行运营SOP"配置触发所选 SOP。

                - 仅对群聊生效；仅当配置了 groupJoinSopId 时触发；
                - 进群处理统一走运营SOP（打招呼/创建跟单等均作为 SOP 里的动作），不再有旧版"新建群聊自动打招呼"分支；
                - 短期去重（TTL）覆盖触发窗口并发；长期去重依赖 SOP 内动作（如打招呼）成为本人消息使 is_first_join 自然变 False。
                  同名群解散重建后，TTL 过期即可再次触发，不会被永久锁死。
                """

        session_name = task_instance.params.get("session_name")
        account_id = getattr(task_instance, "account_id", None)
        partition = self.get_account_partition(account_id)
        components = partition.get_components()
        config_manager = components["config"]
        wechat_instance = components["wechat"]
        resolved_account_id = None
        dedup_key = (resolved_account_id, session_name)
        now = datetime.now().timestamp()
        last_ts = self._greeted_join_groups.get(dedup_key)
        group_join_sop_id = config_manager.get_group_join_sop_id()
        sop = config_manager.get_sop_by_id(group_join_sop_id)
        self._greeted_join_groups[dedup_key] = now
        yield None
        f'{group_join_sop_id}'(")，跳过: ", f'{session_name}')
        "[新进群] 检测到本账号进群: "(f'{session_name}', "（未配置进群SOP，跳过）")
        f'{self._greeted_join_ttl}'("s内已处理过，跳过重复触发: ", f'{session_name}')
        resolved_account_id = wechat_instance.account_info.get("account_id")
    def enqueue_sop_flow(self, account_id, target_name, sop_id, chat_type, source):
        """把一个运营SOP作为一次 SOP_FLOW 立即任务入队（进群/新好友等触发点共用）。

                入队后由统一调度器排队、抢 EXCLUSIVE 独占锁后执行，与其它 RPA 任务串行，不会冲突。
                """

        params = {"sop_id": sop_id, "target_name": target_name, "chat_type": chat_type, "source": source, "account_id": account_id}
        yield None
    def _enqueue_group_join_sop(self, account_id, session_name, sop_id):
        """把"拉新群触发的运营SOP"作为一次 SOP_FLOW 立即任务入队（拉新群场景目标是群）。"""

        yield None
    @staticmethod
    def _is_friend_pass_marker(content):
        """容错判断一条消息内容是否为"对方通过我方好友申请"的标志（吸收标点/微信版本差异）。

                典型标志："我通过了你的朋友验证请求，现在我们可以开始聊天了"（对方气泡，isSelf=False）。
                """

        c = content.strip()
        return "通过了你的朋友验证" in c
        return False
    @classmethod
    def _is_fresh_friend_pass(cls, all_messages):
        """判断是否为"尚未应答的好友通过事件"。all_messages 按时间正序(oldest→newest)。

                True 当且仅当：存在好友通过标志消息(对方发出)，且其后【没有对方的新消息】
                ——即对方尚未开口。一旦对方回复，视为进入正常对话，不再触发打招呼/SOP。
                这是【持久去重】：我方打招呼/SOP 发出后对方若回复，标志后就有了对方消息，
                自然不再重复触发；不依赖进程内状态，重启也成立。
                我方消息（验证说明"我是Leo…"、我方打招呼话术）isSelf=True，不算对方回复，不影响判定。
                """

        msgs = all_messages
        marker_idx = -1
        return True
        msg = None
        return False
        return False
        i = ""[0]
        msg = ""[1]
        marker_idx = i
        enumerate(msgs)
    def _handle_friend_pass(self, task_instance):
        """检测"对方通过我方好友申请"事件并触发运营SOP / 旧版自动打招呼。

                - 与新进群同属"事件副作用"，独立于"是否有待回复消息"先行触发；
                - 双通道识别，任一命中即触发：
                  ① 对方气泡标志"我通过了你的朋友验证请求…"（对方手动通过时发送），扫 all_messages
                     （完整一屏读取）而非 valid_messages，绕开锚点/末条是我方消息导致的漏判；
                  ② is_friend_pass 信号：系统提示"你已添加了xxx，现在可以开始聊天了"（对方开启
                     自动通过时无①的气泡，仅有此系统提示），由 chat.py 解析阶段识别后透传；
                - 仅单聊生效；持久去重靠"标志/提示后双方是否已有实质消息"，TTL 仅兜底我方打招呼后的瞬时并发重触发；
                - 绑定了 friendPassSopId → 入队 SOP_FLOW（单聊目标）；否则回退旧版 autoGreeting 话术组。
                """

        session_name = task_instance.params.get("session_name")
        all_messages = task_instance.params.get("all_messages")
        account_id = getattr(task_instance, "account_id", None)
        partition = self.get_account_partition(account_id)
        components = partition.get_components()
        config_manager = components["config"]
        wechat_instance = components["wechat"]
        resolved_account_id = None
        dedup_key = (resolved_account_id, session_name)
        now = datetime.now().timestamp()
        last_ts = self._friend_pass_sop.get(dedup_key)
        self._friend_pass_sop[dedup_key] = now
        friend_pass_sop_id = config_manager.get_friend_pass_sop_id()
        greeting_group_id = config_manager.get_greeting_group_id()
        from WeRobotCore.utils.greeting_manager import GreetingManager
        gm = GreetingManager(config_manager)
        yield None
        yield None
        f'{self._friend_pass_sop_ttl}'("s内已处理过，跳过重复触发: ", f'{session_name}')
        resolved_account_id = wechat_instance.account_info.get("account_id")
    def execute_sop_task(self, context, params):
        """SOP_FLOW 任务执行器：加载 SOP 定义并对目标按序执行（已持有独占锁）。"""

        sop_id = params.get("sop_id")
        target_name = params.get("target_name")
        chat_type = params.get("chat_type", "single")
        source = params.get("source", "")
        account_key = params.get("account_id")
        partition = self.get_account_partition(account_key)
        components = partition.get_components()
        config_manager = components["config"]
        wechat_instance = components["wechat"]
        resolved_account_id = None
        sop = config_manager.get_sop_by_id(sop_id)
        from WeRobotCore.task_system_v3.sop_runner import SopRunner
        runner = SopRunner(config_manager, wechat_instance, resolved_account_id)
        yield None
        self.logger.warning("[SOP] 未找到SOP定义，跳过: ", f'{sop_id}')
        return True
        resolved_account_id = wechat_instance.account_info.get("account_id")
    def _dispatch_to_agent(self, context, task_instance):
        """将任务推送给 Agent 处理，等待 Agent 回调后执行对应动作"""

        from WeRobotCore.task_system_v3.agent_reply_waiter import agent_reply_waiter
        from WeRobotCore.task_system_v2.websocket_manager import websocket_manager
        task_id = context.task_id
        params = task_instance.params
        session_name = params.get("session_name", "")
        account_id = getattr(task_instance, "account_id", None)
        agent_reply_waiter.register(task_id, session_name=session_name)
        task_instance.status = TaskStatus.PENDING_AGENT
        yield None
    def _send_agent_reply(self, task_instance, reply_text):
        """发送 Agent 决定的回复文本，并更新缓存"""

        from WeRobotCore.api import chat
        from WeRobotCore.task_system_v2.websocket_manager import websocket_manager
        params = task_instance.params
        session_name = params.get("session_name", "")
        session_id = params.get("session_id")
        account_id = getattr(task_instance, "account_id", None)
        self.logger.warning("[Agent模式] 回复内容或会话名为空，跳过发送")
        return False
        task_instance.status = TaskStatus.RUNNING
        yield None
    def _rebuild_task_from_params(self, task_id, params):
        """从参数重建任务实例"""

        task_data = params.get("task_data", {})
        original_params = task_data.get("params", {})
        required_params = ("session_id", "message", "user_name", "session_name")
        missing_params = required_params
        param = []
        AutoReplyTask = self._get_auto_reply_task_class()
        task_instance = AutoReplyTask(task_id=task_id, params=original_params, account_id=task_data.get("account_id"), schedule_time=task_data.get("schedule_time"))
        return task_instance
        task_instance.message_num = task_data["message_num"]
        task_instance.status = TaskStatus(task_data["status"])
        self.logger.error("缺少必要参数: ", f'{missing_params}')
        param = NULL
    def _handle_task_result(self, context, task, result):
        """处理任务执行结果（兼容V2逻辑）"""

        task.status = TaskStatus.FAILED
        task.completed_at = datetime.now()
        task.result = result
        yield None
        task.status = TaskStatus.COMPLETED
    def _cleanup_task(self, task_id, task):
        """清理任务资源（兼容V2清理逻辑）"""

        self._execution_contexts.pop(task_id, None)
        session_name = task.params.get("session_name")
        account_id = getattr(task, "account_id", None)
        partition = self.get_account_partition(account_id)
        self.logger.debug("任务清理完成: ", f'{task_id}')
        del self._task_instance_timestamps[task_id]
        del self._task_instances[task_id]
        del partition.task_map[session_name]
    def _prepare_task_messages(self, task_instance):
        """准备任务消息参数（模拟V2调度器逻辑）"""

        session_name = task_instance.params.get("session_name")
        session_id = task_instance.params.get("session_id")
        task_account_id = getattr(task_instance, "account_id", None)
        f'{session_name}'(", 账号: ", f'{task_account_id}')
        yield None
    def _get_chat_messages(self, session_name, account_id):
        """获取聊天消息（模拟V2调度器逻辑）"""

        from WeRobotCore.api import chat
        yield None
    def _get_valid_messages(self, session_id, all_messages, reference_message, task_created_ts, account_id):
        """获取有效消息（使用V3优化的逻辑）"""

        valid_messages = []
        return self.get_valid_messages(session_id=session_id, all_messages=valid_messages, reference_message=reference_message, task_created_ts=task_created_ts, account_id=account_id)
        self.logger.debug("没有有效的消息格式")
        return []
        msg = all_messages
        self.logger.warning("消息不是字典格式: ", f'{type(msg)}')
        valid_messages.append(msg)
        self.logger.warning("all_messages不是列表格式: ", f'{type(all_messages)}')
        return []
    def _update_message_cache(self, task_id, result):
        """更新消息缓存（兼容V2缓存逻辑）"""
    def convert_task_to_params(self, task):
        """将V2任务转换为V3参数格式"""

        required_params = ("session_id", "message", "user_name", "session_name")
        missing_params = required_params
        param = []
        self.logger.debug("所有关键参数都存在")
        result = {"task_class": "AutoReplyTask", "task_data": {"task_id": task.id, "params": task.params, "account_id": getattr(task, "account_id", None), "schedule_time": task.schedule_time, "priority": task.priority, "status": task.status, "message_num": getattr(task, "message_num", 1)}, "keep_instance": True}
        self.logger.debug("转换结果task_data.params: ", f'{result["task_data"]["params"]}')
        return result
        self.logger.warning("缺少关键参数: ", f'{missing_params}')
        param = NULL
    def get_schedule_config(self, task):
        """获取调度配置（自动回复任务通常是立即执行）"""

        return ScheduleConfig(trigger_type=TriggerType.DATE, trigger_args={"run_date": datetime.now()}, execution_mode=ExecutionMode.IMMEDIATE, max_instances=1, coalesce=True, misfire_grace_time=30)
    def clear_task_map(self, account_id):
        """清理任务映射（兼容V2接口）"""

        partition = self.get_account_partition(account_id)
        partition.task_map.clear()
        partition = self._partitions.values()
        partition.task_map.clear()
    def clear_message_cache(self, account_id):
        """清理消息缓存（兼容V2接口）"""

        partition = self.get_account_partition(account_id)
        partition.message_cache.clear()
        partition.last_reply_cache.clear()
        partition = self._partitions.values()
        partition.message_cache.clear()
        partition.last_reply_cache.clear()
    def update_message_mapping(self, session_id, user_message, reply_message, sender_name, fingerprint, account_id):
        """更新消息映射（完全兼容V2接口）"""

        partition = self.get_account_partition(account_id)
        session_id = int(session_id)
        cache = partition.message_cache[session_id]
        cache["timestamp"] = datetime.now().timestamp()
        self._clean_expired_cache_for_partition(partition)
        cache["reply_messages"].append(reply_message)
        cache["user_message"] = user_message
        cache["reply_messages"] = []
        cache["sender_name"] = sender_name
        cache["fingerprint"] = fingerprint
        partition.message_cache[session_id] = {"user_message": None, "reply_messages": [], "timestamp": datetime.now().timestamp(), "sender_name": None, "fingerprint": None}
    def _clean_expired_cache_for_partition(self, partition, max_age):
        """清理分区中超过指定时间的缓存（默认1小时，兼容V2）"""

        current_time = datetime.now().timestamp()
        expired_sessions = partition.message_cache.items()
        session_id = []
        cache = session_id
        session_id = expired_sessions
        del partition.message_cache[session_id]
        session_id = cache[0]
        cache = cache[1]
    def update_last_reply_cache(self, session_id, content, account_id):
        """更新最后回复缓存（兼容V2任务调用）"""

        partition = self.get_account_partition(account_id)
        partition.last_reply_cache[session_id] = content
        f'{session_id}'(", account_id=", f'{account_id}')
        self.update_message_mapping(session_id=session_id, reply_message=content, account_id=account_id)
    def get_valid_messages(self, session_id, all_messages, reference_message, task_created_ts, account_id):
        """获取有效消息（从V2平移的完整逻辑）"""

        def normalize_content(content):
            """标准化消息内容，去除特殊字符"""

            text = content.replace("\n", "").replace("\r", "").replace("﻿", "").strip()
            return text
            text = -3
            return ""
        valid_messages = []
        ref_content = normalize_content(reference_message.get("content", ""))
        is_group = reference_message.get("isGroup", False)
        partition = self.get_account_partition(account_id)
        cache = partition.message_cache.get(int(session_id), {})
        current_time = datetime.now().timestamp()
        cache_time = cache.get("timestamp", 0)
        time_diff = current_time - cache_time
        last_user_message = None
        last_sender_name = cache.get("sender_name")
        f'{last_sender_name}'("：", f'{last_user_message}')
        recent_messages = reversed(all_messages(-10, None))
        temp_messages = []
        ref_index = None
        real_ref_index = None
        last_msg_index = None
        _anchor_rect_for_collection = None
        start_index = ref_index
        end_index = ref_index
        valid_messages = temp_messages
        msg = []
        "需要回复的消息列表："(msg, f'{valid_messages}')
        return valid_messages
        msg = print
        i = msg.get("content")
        msg = recent_messages[i]
        content = msg.get("content", "")
        temp_messages.append(msg)
        _msg_rect = msg.get("rect_info")
        _block_rect = None
        _msg_rect = _block_rect
        _bk = range(i + 1, min(i + 5, len(recent_messages)))
        _bm = recent_messages[_bk]
        _br = _bm.get("rect_info")
        _block_rect = float(_br)
        range(start_index, end_index - 1, -1)
        _msg_rect = float(_msg_rect)
        start_index = last_msg_index - 1
        end_index = ref_index
        "警告：未找到锚点消息："(f'{ref_content}', "，可能已经被撤回")
        end_index = 0
        i = real_ref_index[0]
        msg = real_ref_index[1]
        content = normalize_content(msg.get("content", ""))
        compare_content = content
        msg_sender_name = msg.get("sender", {}).get("name")
        is_ref_match = content == ref_content
        msg_fingerprint = msg.get("fingerprint")
        cache_fingerprint = cache.get("fingerprint")
        last_msg_index = i
        last_msg_index = i
        real_ref_index = i
        ref_index = i
        temp_ref_index = i
        additional_count = 0
        max_additional = 3
        anchor_rect = None
        ref_index = temp_ref_index
        j = range(i + 1, min(i + 1 + max_additional, len(recent_messages)))
        additional_count = additional_count + 1
        next_msg = recent_messages[j]
        f'{j}'(",", f'{next_msg}')
        msg_timestamp = next_msg.get("timestamp")
        time_diff = task_created_ts - msg_timestamp
        print("2分钟内的消息：", f'{content}')
        temp_ref_index = j
        _candidate_rect = next_msg.get("rect_info")
        _resolved = None
        _candidate_rect = _resolved
        _k2 = range(j + 1, min(j + max_additional + 1, len(recent_messages)))
        _km2 = recent_messages[_k2]
        _r2 = _km2.get("rect_info")
        _resolved = float(_r2)
        _candidate_rect = float(_candidate_rect)
        _anchor_r = recent_messages[i].get("rect_info")
        anchor_rect = float(_anchor_r)
        _anchor_rect_for_collection = anchor_rect
        is_ref_match = content.startswith(ref_content)
        is_ref_match = content.startswith(ref_content)
        compare_content = content.replace(",未播放", "")
        voice_text = msg.get("voice_text", "")
        compare_content = voice_text
        real_ref_index = i
        ref_index = i
        temp_ref_index = i
        additional_count = 0
        max_additional = 3
        anchor_rect = None
        ref_index = temp_ref_index
        j = range(i + 1, min(i + 1 + max_additional, len(recent_messages)))
        additional_count = additional_count + 1
        next_msg = recent_messages[j]
        msg_timestamp = next_msg.get("timestamp")
        enumerate(recent_messages)
        time_diff = task_created_ts - msg_timestamp
        self.logger.debug("2分钟内的消息：", f'{content}')
        temp_ref_index = j
        _candidate_rect = next_msg.get("rect_info")
        _resolved = None
        _candidate_rect = _resolved
        _k2 = range(j + 1, min(j + max_additional + 1, len(recent_messages)))
        _km2 = recent_messages[_k2]
        _r2 = _km2.get("rect_info")
        _resolved = float(_r2)
        _candidate_rect = float(_candidate_rect)
        _anchor_r = recent_messages[i].get("rect_info")
        anchor_rect = float(_anchor_r)
        _anchor_rect_for_collection = anchor_rect
        return []
    def get_status(self):
        """获取适配器状态"""

        return {"running": self._running, "paused": self._paused, "active_tasks": len(self._task_instances), "partitions": len(self._partitions), "total_cached_messages": sum((p for p in _iter)(self._partitions.values()))}
_global_adapter_instance = None
__annotations__["_global_adapter_instance"] = Optional[AutoReplyAdapterV3]
def get_v3_adapter_instance():
    """获取全局V3适配器实例（用于V2任务兼容）"""

    return _global_adapter_instance
def set_v3_adapter_instance(adapter):
    """设置全局V3适配器实例"""

    _global_adapter_instance = adapter
