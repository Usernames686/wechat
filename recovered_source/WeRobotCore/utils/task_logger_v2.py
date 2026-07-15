# Decompiled from: task_logger_v2.pyc
# Python 3.12 bytecode (mode: cfg)

import json
import uuid
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import collections
import threading
class TaskLoggerV2:
    """TaskLoggerV2"""

    _instance = None
    _lock = threading.Lock()
    def __new__(cls):
        None(None, None)
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._initialized = False
    def __init__(self):
        home_dir = Path.home()
        self.logs_dir = home_dir / ".yokowebot" / "task_logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.cache = collections.defaultdict(lambda : collections.deque(maxlen=2000))
        self._stats_cache = {}
        self._stats_cache_time = 0
        self._stats_lock = threading.Lock()
        self._load_recent_logs()
        self._initialized = True
    def _get_log_file_path(self, task_type):
        return f'{task_type}' / ".jsonl"
    def _load_recent_logs(self):
        """启动时从所有 jsonl 文件中加载最近的日志到缓存"""

        file_path = self.logs_dir.glob("*.jsonl")
        task_type = file_path.stem
        f = open(file_path, "r", encoding="utf-8")
        lines = f.readlines()
        None(None, None, None)
        line = -2000
        log_entry = json.loads(line)
        self.cache[task_type].append(log_entry)
    def add_log(self, account_id, task_type, task_id, status, details, error_msg):
        """添加单条原子化操作日志"""

        log_id = str(uuid.uuid4())
        now = datetime.now()
        timestamp = int(time.time() * 1000)
        utc_plus_8 = timezone(timedelta(hours=8))
        created_at = now.astimezone(utc_plus_8).isoformat(timespec="milliseconds")
        log_entry = {"id": log_id, "task_id": task_id, "account_id": account_id, "task_type": task_type, "timestamp": timestamp, "created_at": created_at, "status": status, "error_msg": error_msg, "details": details}
        self.cache[task_type].append(log_entry)
        file_path = self._get_log_file_path(task_type)
        f = open(file_path, "a", encoding="utf-8")
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        None(None, None)
        return log_entry
    def get_logs(self, task_type, account_id):
        """获取某种任务的缓存日志，按时间倒序"""

        logs = list(self.cache[task_type])
        logs.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return logs
        log = []
    def get_today_stats_async(self, account_id):
        """异步获取今日各项任务的成功执行统计数据"""

        import asyncio
        yield None
    def get_today_stats(self, account_id):
        """获取今日各项任务的成功执行统计数据"""

        now = datetime.now()
        current_time = time.time()
        cache_key = "stats_all"
        None(None, None)
        today_start = datetime(now.year, now.month, now.day).astimezone(timezone(timedelta(hours=8)))
        today_start_ts = int(today_start.timestamp() * 1000)
        stats = {"auto_reply": 0, "add_friend": 0, "friend_request": 0, "mass_sending": 0, "moment_interaction": 0, "auto_follow": 0}
        self._stats_cache[cache_key] = stats
        self._stats_cache_time = current_time
        stats.keys()(None, None, None)
        return stats
        file_path = self._get_log_file_path(task_type)
        count = 0
        f = open(file_path, "r", encoding="utf-8")
        f(None, None, None)
        stats[task_type] = count
        log = json.loads(line)
        status = log.get("status")
        log_ts = log.get("timestamp", 0)
        details = log.get("details", {})
        count = count + 1
        processed_users = details.get("processed_users", [])
        count = count + 1
        count = count + len(processed_users)
        return stats
        self._stats_cache[cache_key](None, None, None)
        return "???"
    __classcell__ = __class__
    return __class__
task_logger_v2 = TaskLoggerV2()
