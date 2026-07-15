# Decompiled from: logger.pyc
# Python 3.12 bytecode (mode: cfg)

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List
class TaskLogger:
    """TaskLogger"""

    _instance = None
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._initialized = False
    def __init__(self):
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.chat_logs_file = self.logs_dir / "chat_logs.json"
        self.mass_sending_logs_file = self.logs_dir / "mass_sending_logs.json"
        self.moment_logs_file = self.logs_dir / "moment_interactions.json"
        self.friend_request_logs_file = self.logs_dir / "friend_request_logs.json"
        self.add_friend_logs_file = self.logs_dir / "add_friend_logs.json"
        self.auto_follow_logs_file = self.logs_dir / "auto_follow_logs.json"
        self.moment_post_logs_file = self.logs_dir / "moment_post_logs.json"
        self._initialized = True
    def _load_logs(self, file_path):
        """从指定文件加载日志，只返回最近48小时内的日志"""

        return []
        f = open(file_path, "r", encoding="utf-8")
        logs = json.load(f)
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=48)
        filtered_logs = []
        logs(None, None, None)
        return filtered_logs
        timestamp = log.get("timestamp")
        log_time = datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc)
        filtered_logs.append(log)
        log_time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    def add_friend_request_log(self, task_id, status, processed_count, tag, error):
        """
                添加好友请求任务日志
                """

        log_file = self.logs_dir / "friend_request_logs.json"
        current_time = datetime.now().isoformat()
        log_entry = {"time": current_time, "task_id": task_id, "status": status, "processed_count": processed_count, "tag": tag, "error": error}
        logs = []
        logs.insert(0, log_entry)
        f = open(log_file, "w", encoding="utf-8")
        json.dump(logs, f, ensure_ascii=False, indent=2)
        None(None, None)
        f = open(log_file, "r", encoding="utf-8")
        content = f.read().strip()
        None(None, None)
        logs = json.loads(content)
    def add_friend_request_action_log(self, account_id, task_id, status, details, error_msg):
        """记录自动通过好友的V2版本日志"""

        task_logger_v2.add_log(account_id=account_id, task_type="friend_request", task_id=task_id, status=status, details=details, error_msg=error_msg)
    def get_friend_request_logs(self):
        """获取好友请求日志"""

        v2_logs = task_logger_v2.get_logs("friend_request")
        new_logs = []
        old_logs = self._load_logs(self.friend_request_logs_file)
        result = new_logs + old_logs
        get_time = (lambda x: t.replace("Z", "+00:00"))
        result.sort(key=lambda x: get_time(x), reverse=True)
        return result
        log = v2_logs
        time_str = log.get("created_at", "")
        details = log.get("details", {})
        processed_users = details.get("processed_users", [])
        processed_count = 0
        new_logs.append({"time": time_str, "task_id": log.get("task_id"), "account_id": log.get("account_id"), "status": log.get("status"), "processed_count": processed_count, "tag": details.get("tag", ""), "greetingGroupId": details.get("greeting_group_id", ""), "targetGroup": details.get("target_group", ""), "processed_users": processed_users, "error": log.get("error_msg")})
        time_str = time_str.replace("+08:00", "Z")
    def _save_logs(self, logs, file_path):
        """保存日志到指定文件"""

        f = open(file_path, "w", encoding="utf-8")
        json.dump(logs, f, ensure_ascii=False, indent=2)
        None(None, None)
    def add_chat_log(self, session_name, message, content, status, chat_type, error, account_id):
        """添加自动回复日志"""

        logs = self._load_logs(self.chat_logs_file)
        log_entry = {"timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "targetName": session_name, "content": content, "status": status, "error": None, "chatType": chat_type, "message": message, "account_id": account_id}
        logs.insert(0, log_entry)
        logs(None, 500, self.chat_logs_file)
        return log_entry
    def _generate_random_id(self):
        """生成随机ID"""

        import random
        import string
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
    def add_mass_sending_log(self, task_id, status, params, error):
        """记录群发任务日志 (V2)"""

        account_id = "unknown"
        task_logger_v2.add_log(account_id=account_id, task_type="mass_sending", task_id=task_id, status=status, details=params, error_msg=error)
        account_id = params["account_id"]
    def add_chat_collection_log(self, task_id, status, params, error):
        """添加聊天记录采集任务日志"""

        chat_collection_logs_file = self.logs_dir / "chat_collection_logs.json"
        logs = self._load_logs(chat_collection_logs_file)
        log_entry = {"id": task_id, "timestamp": datetime.now().isoformat(), "type": "chat_collection", "status": status, "params": params, "error": error}
        logs.insert(0, log_entry)
        logs(None, 1000, chat_collection_logs_file)
        return log_entry
    def add_moment_log(self, content, status, error):
        """添加朋友圈互动日志"""

        logs = self._load_logs(self.moment_logs_file)
        log_entry = {"id": f'{datetime.now().timestamp()}', "timestamp": datetime.now().isoformat(), "type": "moment", "content": content, "status": status, "error": error}
        logs.insert(0, log_entry)
        logs(None, 1000, self.moment_logs_file)
        return log_entry
    def add_auto_reply_action_log(self, account_id, task_id, status, details, error_msg):
        """记录单条原子化的自动回复日志 (V2)"""

        task_logger_v2.add_log(account_id=account_id, task_type="auto_reply", task_id=task_id, status=status, details=details, error_msg=error_msg)
    def get_chat_logs(self):
        """获取自动回复日志"""

        v2_logs = task_logger_v2.get_logs("auto_reply")
        new_logs = []
        old_logs = self._load_logs(self.chat_logs_file)
        result = new_logs + old_logs
        get_time = (lambda x: t.replace("Z", "+00:00"))
        result.sort(key=lambda x: get_time(x), reverse=True)
        return result
        log = v2_logs
        time_str = log.get("created_at", "")
        details = log.get("details", {})
        new_logs.append({"timestamp": time_str, "targetName": details.get("session_name", ""), "content": details.get("reply_msg", ""), "status": log.get("status"), "error": log.get("error_msg"), "chatType": details.get("chat_type", "single"), "message": details.get("receive_msg", ""), "account_id": log.get("account_id")})
        time_str = time_str.replace("+08:00", "Z")
    def get_mass_sending_logs(self):
        """获取群发任务日志"""

        v2_logs = task_logger_v2.get_logs("mass_sending")
        new_logs = []
        old_logs = self._load_logs(self.mass_sending_logs_file)
        result = new_logs + old_logs
        get_time = (lambda x: t.replace("Z", "+00:00"))
        result.sort(key=lambda x: get_time(x), reverse=True)
        return result
        log = v2_logs
        time_str = log.get("created_at", "")
        new_logs.append({"id": log.get("task_id", log.get("id")), "timestamp": time_str, "type": "mass_sending", "status": log.get("status"), "params": log.get("details", {}), "error": log.get("error_msg"), "account_id": log.get("account_id")})
        time_str = time_str.replace("+08:00", "Z")
    def get_chat_collection_logs(self):
        """获取聊天采集任务日志"""

        chat_collection_logs_file = self.logs_dir / "chat_collection_logs.json"
        return self._load_logs(chat_collection_logs_file)
    def get_moment_logs(self):
        """获取朋友圈互动日志"""

        v2_logs = task_logger_v2.get_logs("moment_interaction")
        new_logs = []
        logs = self._load_logs(self.moment_logs_file)
        merged_logs = new_logs + logs
        filtered_logs = []
        get_time = (lambda x: t.replace("Z", "+00:00"))
        filtered_logs.sort(key=lambda x: get_time(x), reverse=True)
        return filtered_logs
        log = merged_logs
        operation_types = log.get("type", [])
        comment_content = log.get("comment_content", "")
        filtered_logs.append(log)
        log = v2_logs
        details = log.get("details", {})
        time_str = log.get("created_at", "")
        new_log = {"id": log.get("id"), "timestamp": time_str, "type": details.get("action_type", []), "publisher": details.get("publisher", ""), "content": details.get("content", ""), "publish_time": details.get("publish_time", ""), "comment_content": details.get("comment_content", ""), "account_id": log.get("account_id", ""), "status": log.get("status"), "error": log.get("error_msg")}
        new_logs.append(new_log)
        time_str = time_str.replace("+08:00", "Z")
    def add_moment_action_log(self, account_id, task_id, status, details, error_msg):
        """记录单条原子化的朋友圈互动日志"""

        task_logger_v2.add_log(account_id=account_id, task_type="moment_interaction", task_id=task_id, status=status, details=details, error_msg=error_msg)
    def add_friend_log(self, task_id, processed_count, tags, attempt_count):
        """
                添加自动添加好友任务日志

                Args:
                    task_id: 任务ID
                    processed_count: 成功数量
                    tags: 打招呼话术
                    attempt_count: 尝试总数
                """

        log_file = self.logs_dir / "add_friend_logs.json"
        current_time = datetime.now().isoformat()
        log_entry = {"time": current_time, "task_id": task_id, "processed_count": processed_count, "attempt_count": attempt_count, "tag": ""}
        logs = []
        logs.insert(0, log_entry)
        f = open(log_file, "w", encoding="utf-8")
        json.dump(logs, f, ensure_ascii=False, indent=2)
        None(None, None)
        f = open(log_file, "r", encoding="utf-8")
        content = f.read().strip()
        None(None, None)
        logs = json.loads(content)
    def get_add_friend_logs(self):
        """获取自动添加好友日志 (聚合转换)"""

        v2_logs = task_logger_v2.get_logs("add_friend")
        aggregated = {}
        new_logs = list(aggregated.values())
        old_logs = self._load_logs(self.logs_dir / "add_friend_logs.json")
        result = new_logs + old_logs
        get_time = (lambda x: t.replace("Z", "+00:00"))
        result.sort(key=lambda x: get_time(x), reverse=True)
        return result
        log = v2_logs
        task_id = log.get("task_id")
        details = log.get("details", {})
        aggregated[task_id]["targets"].append({"wxid": details.get("wxid", ""), "nickname": details.get("name", ""), "status": log.get("status"), "error_msg": log.get("error_msg", "")})
        aggregated[task_id]["attempt_count"] = aggregated[task_id]["attempt_count"] + 1
        aggregated[task_id]["processed_count"] = aggregated[task_id]["processed_count"] + 1
        time_str = log.get("created_at", "")
        aggregated[task_id] = {"time": time_str, "task_id": task_id, "account_id": log.get("account_id", ""), "processed_count": 0, "attempt_count": 0, "tag": log.get("details", {}).get("hello_msg", ""), "targets": []}
        time_str = time_str.replace("+08:00", "Z")
    def add_friend_action_log(self, account_id, task_id, status, details, error_msg):
        """记录单条原子化的加好友日志"""

        task_logger_v2.add_log(account_id=account_id, task_type="add_friend", task_id=task_id, status=status, details=details, error_msg=error_msg)
    def log_auto_follow_execution(self, log_data):
        """记录自动跟单任务执行日志 (已适配 V2 原子化日志)

                Args:
                    log_data: 日志数据，包含：
                        - task_id: 任务ID
                        - friend_wxid: 好友微信ID
                        - friend_name: 好友昵称
                        - account_id: 微信账号ID
                        - agent_id: 智能体ID
                        - follow_scenario: 跟单场景
                        - execution_time: 执行时间
                        - success: 是否成功
                        - generated_message: 生成的消息内容
                        - error: 错误信息（如果有）
                """

        task_logger_v2.add_log(account_id=log_data.get("account_id", ""), task_type="auto_follow", task_id=log_data.get("task_id", ""), status="failed", details={"friend_wxid": log_data.get("friend_wxid", ""), "friend_name": log_data.get("friend_name", ""), "agent_id": log_data.get("agent_id", ""), "follow_scenario": log_data.get("follow_scenario", ""), "generated_message": log_data.get("generated_message", "")}, error_msg=log_data.get("error"))
    def get_auto_follow_logs(self):
        """获取自动跟单日志"""

        v2_logs = task_logger_v2.get_logs("auto_follow")
        new_logs = []
        old_logs = self._load_logs(self.auto_follow_logs_file)
        result = new_logs + old_logs
        get_time = (lambda x: t.replace("Z", "+00:00"))
        result.sort(key=lambda x: get_time(x), reverse=True)
        return result
        log = v2_logs
        time_str = log.get("created_at", "")
        details = log.get("details", {})
        new_logs.append({"timestamp": time_str, "execution_time": time_str, "task_id": log.get("task_id"), "friend_wxid": details.get("friend_wxid", ""), "friend_name": details.get("friend_name", ""), "account_id": log.get("account_id"), "agent_id": details.get("agent_id", ""), "follow_scenario": details.get("follow_scenario", ""), "success": log.get("status") == "success", "generated_message": details.get("generated_message", ""), "error": log.get("error_msg")})
        time_str = time_str.replace("+08:00", "Z")
    def get_auto_follow_logs_by_friend(self, friend_wxid):
        """根据好友微信ID获取跟单日志"""

        all_logs = self.get_auto_follow_logs()
        log = []
        return all_logs
    def add_moment_post_log(self, task_id, status, folder_path, text, media_count, account, error):
        logs = self._load_logs(self.moment_post_logs_file)
        log_entry = {"id": task_id, "timestamp": datetime.now().isoformat(), "type": "moment_post", "status": status, "folder_path": folder_path, "text": text, "media_count": media_count, "account": account, "error": error}
        logs.insert(0, log_entry)
        logs(None, 1000, self.moment_post_logs_file)
        return log_entry
    def get_moment_post_logs(self):
        return self._load_logs(self.moment_post_logs_file)
    __classcell__ = __class__
    return __class__
task_logger = TaskLogger()
import logging
def get_logger(name):
    """
        获取指定名称的日志记录器

        Args:
            name: 日志记录器名称

        Returns:
            logging.Logger: 配置好的日志记录器
        """

    logger = logging.getLogger(name)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_dir, f'{name}' / ".log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    import sys
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger
    return logger
