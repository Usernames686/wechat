# Decompiled from: mass_sending_task.pyc
# Python 3.12 bytecode (mode: cfg)

from datetime import datetime, timezone, timedelta
import asyncio
import random
import os
import json
import hashlib
from typing import Dict, Any, Optional, List
from venv import logger
import re
class MassSendingTask(TimedBaseTask):
    """MassSendingTask"""

    def __init__(self, task_id, params, schedule_time, schedule_config, is_recurring):
        super().__init__(task_id=task_id, task_type=TaskType.MASS_SENDING, params=params, schedule_time=schedule_time, priority=TaskPriority.MEDIUM, schedule_config=schedule_config, is_recurring=is_recurring)
        self.task_logger = TaskLogger()
        self.config_manager = ConfigManager()
        self.message_processor = MessageProcessor()
        self.account_id = params.get("account_id")
        self.wechat = None
        self.id = task_id
        self.progress = 0
        self.total = 0
        self.error = None
        self.is_persistent = False
        self._ai_semaphore = asyncio.Semaphore(1)
        self.last_broadcast_time = 0
        self.broadcast_interval = 1.0
        self.paused = False
        self.interrupted = False
        self.interrupt_reason = None
        self.sent_users = set()
        self._yield_callback = None
        self._acquire_callback = None
        self._load_progress()
        raise ValueError("必须指定标签或好友列表其中之一")
    def set_pause_callbacks(self, yield_callback, acquire_callback):
        """设置暂停时的回调函数，用于释放和重新获取权限"""

        self._yield_callback = yield_callback
        self._acquire_callback = acquire_callback
    def pause(self):
        self.paused = True
        self.status = TaskStatus.PAUSED
        self._save_progress()
        "任务 "(f'{self.id}', " 已暂停")
        tag_ids = self.params.get("tagIds", [])
        greeting_group_id = self.params.get("greetingGroupId")
        selected_friends = self.params.get("selectedFriends", [])
        yield None
    def resume(self):
        self.paused = False
        self.status = TaskStatus.RUNNING
        "任务 "(f'{self.id}', " 已恢复")
        tag_ids = self.params.get("tagIds", [])
        greeting_group_id = self.params.get("greetingGroupId")
        selected_friends = self.params.get("selectedFriends", [])
        yield None
    def cancel(self):
        """取消任务"""

        self.paused = False
        self.status = TaskStatus.CANCELLED
        self.error = "任务已取消"
        "任务 "(f'{self.id}', " 已取消")
        tag_ids = self.params.get("tagIds", [])
        greeting_group_id = self.params.get("greetingGroupId")
        selected_friends = self.params.get("selectedFriends", [])
        yield None
    def _get_progress_file_path(self):
        from WeRobotCore.utils.data_manager import DataManager
        base_dir = os.path.join(DataManager.get_data_dir_str(), "mass_sending_progress")
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, f'{self.id}', ".json")
    def _save_progress(self):
        data = {"progress": self.progress, "sent_users": list(self.sent_users), "total": self.total, "timestamp": datetime.now().isoformat()}
        f = open(self._get_progress_file_path(), "w", encoding="utf-8")
        json.dump(data, f, ensure_ascii=False, indent=2)
        None(None, None)
    def _load_progress(self):
        path = self._get_progress_file_path()
        f = open(path, "r", encoding="utf-8")
        data = json.load(f)
        self.progress = data.get("progress", 0)
        self.sent_users = set(data.get("sent_users", []))
        f'{self.progress}'("/", f'{data.get("total")}')
        "已恢复进度: "(None, None, None)
    def _is_account_online(self):
        """检测当前微信账号是否在线（掉线判断）。复用通用检测模块。

                微信掉线后窗口句柄失效、进程改变、界面变为扫码登录。优先用已绑定的窗口
                句柄做最快判定，再按 account_id 经实例管理器二次校验。
                """

        wh = None
        from WeRobotCore.core import account_online_monitor
        return account_online_monitor.is_account_online(self.account_id, window_handle=wh)
        getattr(self.wechat, "_bound_window_handle", None)
    def _handle_interruption(self, reason, greeting_group_id, tag_ids, selected_friends):
        """外部原因（如微信掉线）导致的任务中断处理：
                保存断点 + 记录任务级日志 + 置为可恢复的暂停态，等待用户手动恢复。
                """

        self.interrupted = True
        self.interrupt_reason = reason
        self.paused = True
        self.status = TaskStatus.PAUSED
        self.error = reason
        self._save_progress()
        self._save_task_log()
        "/"(f'{self.total}', "）")
        yield None
    def execute(self):
        print("群发任务启动...", f'{self.schedule_time}')
        tag_ids = self.params.get("tagIds", [])
        greeting_group_id = self.params.get("greetingGroupId")
        selected_friends = self.params.get("selectedFriends", [])
        content_type = self.params.get("contentType", "greeting")
        agent_id = self.params.get("agentId")
        yield None
        self.wechat = WeChat()
    def _get_target_users(self, tag_ids, selected_friends):
        """获取目标用户列表"""

        users = []
        has_untagged = "untagged" in tag_ids
        tagged_users = set()
        tid = []
        return list(set(users))
        print("正在获取未分组用户列表...")
        untagged_users = chat.get_untagged_users()
        user = []
        users.extend(user, untagged_users)
        user = NULL
        tag_id = user
        "正在获取标签 "(f'{tag_id}', " 的用户列表...")
        tag_users = chat.get_users_by_tag(tag_id)
        user = []
        users.extend(tag_users)
        tagged_users.update(tag_users)
        tid = str(user).strip()
        users = selected_friends
    def _process_greeting_mass_sending(self, users, greeting_group_id, tag_ids, selected_friends):
        """处理使用话术组的群发"""

        greeting_manager = GreetingManager(self.config_manager)
        interval_str = str(self.params.get("sendInterval", "10-30"))
        print("开始执行群发任务：", f'{interval_str}')
        parts = interval_str.split("-")
        min_delay = float(parts[0])
        max_delay = float(parts[1])
        min_delay = (10.0, 30.0)[0]
        max_delay = (10.0, 30.0)[1]
        i = enumerate(users, 1)[0]
        user = enumerate(users, 1)[1]
        yield None
        self.status = TaskStatus.CANCELLED
        self.error = "用户手动终止任务"
        yield None
        self.status = TaskStatus.RUNNING
        yield None
        yield None
        "任务 "(f'{self.id}', " 已取消，终止执行")
        yield None
        "任务 "(f'{self.id}', " 在暂停期间被取消")
        yield None
        self.status = TaskStatus.PAUSED
        yield None
    def _build_message_content(self, message):
        """构建发送到智能体的消息内容"""

        return {"role": "user", "content_type": "text", "content": message}
    def _broadcast_task_status(self, greeting_group_id, tag_ids, selected_friends, force):
        """广播任务状态"""

        import time
        current_time = time.time()
        computed_status = self.status.value
        yield None
        computed_status = self.status.value
        computed_status = TaskStatus.COMPLETED.value
    def _get_greeting_group(self, greeting_group_id):
        """获取话术组配置"""

        config = self.config_manager.load_config("greeting_config")
        greeting_groups = config.get("greeting_config", {})
        greeting_groups = greeting_groups.get("greeting_config", [])
        greeting_group = None
        print("找到话术组: ", f'{greeting_group}')
        return greeting_group
        raise ValueError("话术组格式错误: ", f'{greeting_group}')
        raise ValueError("未找到话术组: ", f'{greeting_group_id}')
        group = NULL
        greeting_group = group
        raise ValueError("无效的话术组列表格式: ", f'{greeting_groups}')
        raise ValueError("无效的配置格式: ", f'{config}')
    def _save_task_log(self):
        """保存任务日志"""

        target_name = self.params.get("targetName", "未知")
        params = {"targetName": target_name, "content": self.params.get("greetingGroupId", ""), "tagIds": self.params.get("tagIds", []), "selectedFriends": self.params.get("selectedFriends", []), "contentType": self.params.get("contentType", "greeting"), "agentId": self.params.get("greetingGroupId"), "scheduleTime": None, "progress": self.progress, "total": self.total, "type": self.params.get("type", "text"), "batchIndex": self.params.get("batchIndex"), "totalBatches": self.params.get("totalBatches"), "account_id": self.account_id}
        self.task_logger.add_mass_sending_log(task_id=self.id, status=self.status.value, params=params, error=None)
        target_name = ")"
    __classcell__ = __class__
    return __class__
