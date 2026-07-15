# Decompiled from: risk_control_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import json
import os
from datetime import datetime, timedelta
import pytz
from enum import Enum
from pathlib import Path
from WeRobotCore.utils.data_manager import DataManager
class RiskControlType(Enum):
    """RiskControlType"""

    ADD_FRIEND_FREQUENT = "ADD_FRIEND_FREQUENT"
class RiskControlManager:
    """RiskControlManager"""

    _instance = None
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._init()
    def _init(self):
        data_dir = DataManager.get_data_dir_str()
        self.record_file = os.path.join(data_dir, "risk_control_records.jsonl")
        self.tz = pytz.timezone("Asia/Shanghai")
    def add_record(self, account_id, risk_type, remark):
        """
                记录风控违规信息
                :param account_id: 微信账号
                :param risk_type: 风控类型
                :param remark: 备注说明
                """

        record = {"time": datetime.now(self.tz).strftime("%Y-%m-%d %H:%M:%S"), "risk_type": risk_type, "account_id": account_id, "remark": remark}
        f = open(self.record_file, "a", encoding="utf-8")
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        None(None, None)
    def get_recent_records(self, hours):
        """
                获取最近N小时内的风控记录
                :param hours: 小时数，默认24
                """

        records = []
        cutoff_time = datetime.now(self.tz) - timedelta(hours=hours)
        f = open(self.record_file, "r", encoding="utf-8")
        f(None, None, None)
        return records
        record = json.loads(line.strip())
        record_time = datetime.strptime(record["time"], "%Y-%m-%d %H:%M:%S")
        record_time = self.tz.localize(record_time)
        records.append(record)
        return []
    def is_account_restricted(self, account_id, risk_type, hours):
        """
                判断指定账号在最近N小时内是否触发了指定的风控
                :param account_id: 微信账号
                :param risk_type: 风控类型
                :param hours: 小时数，默认24
                """

        records = self.get_recent_records(hours=hours)
        risk_value = risk_type
        return False
        record = records
        return True
    __classcell__ = __class__
    return __class__
