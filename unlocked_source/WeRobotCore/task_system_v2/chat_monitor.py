# Decompiled from: chat_monitor.pyc
# Python 3.12 bytecode (mode: cfg)

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import asyncio
import re
import traceback
EXITED_GROUP_CHAT_MESSAGES = {"你已退出该群聊。", "你已解散该群聊"}
class ChatMonitorV2:
    """ChatMonitorV2"""

    _instances = {}
    _default_instance = None
    def __new__(cls, account_id):
        return cls._instances[account_id]
        instance = super().__new__(cls)
        instance._initialized = False
        instance.account_id = account_id
        cls._instances[account_id] = instance
        return cls._default_instance
        cls._default_instance = super().__new__(cls)
        cls._default_instance._initialized = False
        cls._default_instance.account_id = None
    def __init__(self, account_id):
        self._initialized = True
        self.account_id = account_id
        self._running = False
        self._monitor_task = None
        self.config_manager = ConfigManager(account_id)
        self.logger = UiaLogger(logger_name="ChatMonitorV2").get_logger()
        self._check_interval = 5
        self._monitor_start_time = None
        self._last_message_cache = {}
        self._message_cache = {}
        self._session_cache = []
        self._last_message_times = {}
        self._lock = asyncio.Lock()
        self._user_paused = False
        self._offline_count = 0
        self._reply_mode = "local"
        self.command_manager = CommandManager()
        self._manual_review_enabled = False
        self.auto_reply_manager_v3 = None
    def start(self, initiated):
        """
                启动会话监控
                 Args:
                    initiated: 是否由用户主动启动，如果是其他调度器触发的重启，则无需重置_monitor_start_time字段，这样可以执行最新3分钟接收到的新消息。
                """

        f'{self._running}'("，监听账号：", f'{self.account_id}')
        self.auto_reply_manager_v3 = get_auto_reply_manager()
        self._running = True
        yield None
        self._monitor_start_time = datetime.now()
        f'{self.account_id}'("，启动时间：", f'{self._monitor_start_time}')
    def set_manual_review_enabled(self, enabled):
        """设置人工复核状态"""

        self._manual_review_enabled = enabled
    def get_manual_review_enabled(self):
        """获取人工复核状态"""

        return self._manual_review_enabled
    def _monitor_loop(self):
        """监控循环"""

        "开始监控循环 , 检查间隔: "(f'{self._check_interval}', "秒")
        yield None
    def stop(self, user_initiated):
        """停止会话监控"""

        self._running = False
        yield None
    def is_running(self):
        """获取监控器运行状态"""

        return self._running
    def _cleanup_resources(self):
        """清理资源"""

        self._message_cache.clear()
        self._session_cache.clear()
        self._last_message_times.clear()
        self._monitor_task = None
        self._monitor_start_time = None
    def _normalize_session_preview(self, content):
        """规范化会话列表预览文本，避免未读前缀导致误判。"""

        preview = content
        preview = re.sub("^\\[\\d+条\\]\\s*", "", preview)
        preview = re.sub("^\\[有人@[^\\]]+\\]\\s*", "", preview)
        return preview.strip()
    def _is_exited_group_chat_notice(self, content):
        """识别已退出群聊的系统提示；该会话已不可回复，直接跳过自动回复。"""

        return self._normalize_session_preview(content) in EXITED_GROUP_CHAT_MESSAGES
    def _is_account_online(self):
        """检测当前监听账号的微信是否在线（掉线判断）。复用通用检测模块。"""

        return account_online_monitor.is_account_online(self.account_id)
    def _check_new_messages(self, JUST_CHECK):
        """检查新消息"""

        start_timestamp = None
        yield None
        "账号 "(f'{self.account_id}', " 恢复在线，继续监听会话")
        self._offline_count = 0
        account_online_monitor.reset_offline_notify(self.account_id)
        self._offline_count += 1
        "账号 "(f'{self.account_id}', " 检测到掉线，跳过会话列表读取（等待实例巡检拆除监控）")
        asyncio.get_event_loop().run_in_executor(None, account_online_monitor.notify_offline, self.account_id, "会话监听")
    def _get_message_timestamp(self, time_str):
        """转换消息时间为时间戳（秒级）"""

        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        full_time_str = f'{time_str}'
        msg_datetime = datetime.strptime(full_time_str, "%Y-%m-%d %H:%M")
        time_diff = (msg_datetime - now).total_seconds()
        return msg_datetime.timestamp()
        msg_datetime = msg_datetime - timedelta(days=1)
        return 0
    def _process_new_message(self, session, JUST_CHECK):
        """处理新消息并创建任务"""

        session_id = session.get("id")
        messages = self._message_cache.get(session_id, [])
        content = session.get("lastMessage", "")
        is_at = session.get("is_at", False)
        new_message = {"content": content, "time": session.get("lastTime", ""), "isRead": False, "isSelf": session.get("isGroup", False), "isGroup": session.get("isGroup", False)}
        messages.append(new_message)
        self._message_cache[session_id] = messages
        is_group = session.get("isGroup", False)
        raw_sender = session.get("name", "未知用户")
        sender_name = re.sub("^\\[有人@[^\\]]+\\]\\s*", "", raw_sender).strip()
        f'{session.get("name", "")}'(", 人工复核：", f'{self._manual_review_enabled}')
        yield None
        print("监控器已暂停不创建回复任务，如需继续监控，请发送“开启”指令")
        command = content.strip()
        result = self.command_manager.execute_command(command)
        f'{command}'(" 结果: ", f'{result.message}')
    __classcell__ = __class__
    return __class__
