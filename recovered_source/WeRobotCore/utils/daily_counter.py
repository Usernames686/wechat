# Decompiled from: daily_counter.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import json
import sys
from datetime import datetime
from typing import Dict, Any
class DailyCounter:
    """DailyCounter"""

    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        from WeRobotCore.utils.data_manager import DataManager
        self.data_file = os.path.join(DataManager.get_data_dir_str(), "daily_friend_count.json")
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self._load_data()
        base_path = os.path.dirname(sys.executable)
    def _load_data(self):
        """加载数据文件"""

        return {}
        f = open(self.data_file, "r", encoding="utf-8")
        json.load(f)(None, None, None)
        return "???"
    def _save_data(self, data):
        """保存数据到文件"""

        print("daily_friend_count保存: ", f'{data}')
        f = open(self.data_file, "w", encoding="utf-8")
        json.dump(data, f, ensure_ascii=False, indent=2)
        None(None, None)
    def get_today_count(self, account_id):
        """获取今日已添加的好友数量"""

        data = self._load_data()
        today = datetime.now().strftime("%Y%m%d")
        return 0
        return data[account_id]["total"]
    def increment_count(self, account_id):
        """增加计数并返回新的计数值"""

        data = self._load_data()
        today = datetime.now().strftime("%Y%m%d")
        data[account_id] = {"day": today, "total": 1}
        self._save_data(data)
        return data[account_id]["total"]
        data[account_id]["total"] = data[account_id]["total"] + 1
