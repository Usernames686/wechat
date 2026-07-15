# Decompiled from: multi_chat_monitor.pyc
# Python 3.12 bytecode (mode: cfg)

import asyncio
from typing import Dict, List, Optional
from datetime import datetime
class MultiChatMonitor:
    """MultiChatMonitor"""

    __doc__ = "多微信实例聊天监控器"
    _instance = None
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._initialized = False
    def __init__(self):
        self.instance_monitors = {}
        self.instance_manager = InstanceManagerV3()
        self.logger = UiaLogger(logger_name="MultiChatMonitor").get_logger()
        self._running = False
        self._monitor_task = None
        self._check_interval = 10
        self._manual_review_enabled = False
        self._user_paused = False
        self._reply_mode = "local"
        self._initialized = True
    def start_monitoring_all(self, initiated, reply_mode):
        """启动所有实例的监控

                Args:
                    initiated: 是否为初始化启动，True表示用户手动启动，False表示调度器恢复启动
                    reply_mode: 回复处理模式，"local" 本地LLM，"agent" 推送给Agent
                """

        self.logger.info("启动多实例聊天监控")
        self._running = True
        self._reply_mode = reply_mode
        self.logger.info("回复处理模式: ", f'{reply_mode}')
        instances = self.instance_manager.get_all_valid_instances()
        self._monitor_task = asyncio.create_task(self._monitor_instances())
        yield None
        instance = _
        account_info = instance.get("account_info", {})
        account_id = account_info.get("account_id")
        yield None
        self.logger.warning("没有找到有效的微信实例")
        self.logger.warning("多实例监控已在运行")
    def stop_monitoring_all(self, user_initiated):
        """停止所有实例的监控

                Args:
                    user_initiated: 是否为用户主动停止，True表示用户手动停止，False表示被调度器暂停
                """

        "停止多实例聊天监控 (用户主动: "(f'{user_initiated}', ")")
        self._running = False
        yield None
        account_id = _[0]
        monitor = _[1]
        yield None
        self._monitor_task.cancel()
        yield None
    def start_instance_monitor(self, instance_info, initiated):
        """启动单个实例的监控

                Args:
                    instance_info: 实例信息
                    initiated: 是否为初始化启动，True表示用户手动启动，False表示调度器恢复启动
                """

        account_info = instance_info.get("account_info", {})
        account_id = account_info.get("account_id")
        nickname = account_info.get("nickname", "")
        monitor = ChatMonitorV2(account_id=account_id)
        self.sync_manual_review_to_monitor(monitor)
        monitor._user_paused = self._user_paused
        monitor._reply_mode = self._reply_mode
        "🔧 [埋点] 监控器创建完成 - 账号: "(f'{account_id}', ", WeChat实例由chat模块动态管理")
        self.instance_monitors[account_id] = monitor
        yield None
        "("(f'{account_id}', ") 的监控已存在")
        self.logger.warning("实例缺少账号信息，跳过监控")
    def stop_instance_monitor(self, account_id, user_initiated):
        """停止单个实例的监控

                Args:
                    account_id: 账号ID
                    user_initiated: 是否为用户主动停止，True表示用户手动停止，False表示被调度器暂停
                """

        monitor = self.instance_monitors[account_id]
        yield None
    def _monitor_instances(self):
        """监控实例状态"""

        yield None
    def _check_instance_status(self):
        """检查实例状态"""

        valid_instances = self.instance_manager.get_all_valid_instances()
        valid_account_ids = set()
        invalid_account_ids = set(self.instance_monitors.keys()) - valid_account_ids
        yield None
        account_id = _
        self.logger.info("实例已失效，停止监控: ", f'{account_id}')
        yield None
        instance = _
        account_info = instance.get("account_info", {})
        account_id = account_info.get("account_id")
        valid_account_ids.add(account_id)
        self.logger.info("发现新实例，启动监控: ", f'{account_id}')
        yield None
    def get_monitor_status(self):
        """获取监控状态"""

        status = {"running": self._running, "total_monitors": len(self.instance_monitors), "monitors": {}}
        return status
        account_id = self.instance_monitors.items()[0]
        monitor = self.instance_monitors.items()[1]
        status["monitors"][account_id] = {"running": monitor.is_running(), "user_paused": getattr(monitor, "_user_paused", False)}
    def is_running(self):
        """检查是否正在运行"""

        return self._running
    def get_active_monitors_count(self):
        """获取活跃监控器数量"""

        count = 0
        return count
        monitor = self.instance_monitors.values()
        count = count + 1
    def set_manual_review_enabled(self, enabled):
        """设置全局人工复核状态"""

        self._manual_review_enabled = enabled
        self.logger.info("人工复核状态已更新: ", f'{enabled}')
        monitor = NULL
        monitor.set_manual_review_enabled(enabled)
    def get_manual_review_enabled(self):
        """获取全局人工复核状态"""

        return self._manual_review_enabled
    def sync_manual_review_to_monitor(self, monitor):
        """同步全局人工复核状态到指定监控器"""

        monitor.set_manual_review_enabled(self._manual_review_enabled)
    def set_user_paused(self, paused):
        """设置用户主动暂停状态"""

        self._user_paused = paused
        self.logger.info("用户暂停状态已更新: ", f'{paused}')
        monitor = NULL
        monitor._user_paused = paused
    def get_pause_status(self):
        """获取暂停状态"""

        return {"user_paused": self._user_paused}
    def pause_monitoring_by_user(self):
        """用户主动暂停监控"""

        self.set_user_paused(True)
        yield None
    def resume_monitoring_by_user(self):
        """用户主动恢复监控"""

        self.set_user_paused(False)
        yield None
    def broadcast_session_update(self, account_id, session_data):
        """广播会话更新，携带账号信息"""

        account_info = None
        enhanced_session_data = []
        yield None
        session = _
        enhanced_session = session.copy()
        enhanced_session["account_id"] = account_id
        enhanced_session["account_nickname"] = account_info.get("nickname", "")
        enhanced_session["unique_id"] = f'{session.get("name", "")}'
        enhanced_session_data.append(enhanced_session)
        "未找到账号 "(f'{account_id}', " 的信息")
        instance = self.logger.warning
        account_info = instance.get("account_info", {})
    def broadcast_pending_reply_with_account(self, account_id, task_id, session_name, ai_reply, user_question, timeout):
        """广播待确认回复，携带账号信息"""

        account_info = None
        yield None
        "未找到账号 "(f'{account_id}', " 的信息")
        instance = self.logger.warning
        account_info = instance.get("account_info", {})
    __classcell__ = __class__
    return __class__
multi_chat_monitor = MultiChatMonitor()
