# Decompiled from: guide.pyc
# Python 3.12 bytecode (mode: cfg)

from fastapi import APIRouter, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from WeRobotCore.utils.config_manager import ConfigManager
from pathlib import Path
import json
import os
router = APIRouter()
API_KEY = os.environ.get("WEBOT_API_KEY", "yoko_test")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
def get_api_key(api_key):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    return api_key
    return api_key
@Security(get_api_key)
def get_guide_status(api_key):
    """
        Check the status of the newcomer guide steps.
        """

    config_manager = ConfigManager.get_active_instance_config()
    is_newcomer = True
    from WeRobotCore.utils.task_logger_v2 import task_logger_v2
    v2_logs = task_logger_v2.get_logs("auto_reply")
    steps = {"step1": False, "step2": False, "step3": False, "step4": False}
    sync_config = config_manager.load_config("sync_time")
    coze_config = config_manager.load_config("coze_settings")
    dify_config = config_manager.load_config("dify_settings")
    has_coze = coze_config
    has_dify = dify_config
    steps["step2"] = True
    agents_config = config_manager.load_config("agents")
    reply_config = config_manager.load_config("reply_strategy_v2")
    return {"success": True, "is_newcomer": is_newcomer, "steps": steps}
    staff = reply_config["staffList"]
    steps["step4"] = True
    steps["step3"] = True
    dify_config.get("baseUrl")
    steps["step1"] = True
    chat_logs_file = Path("logs/chat_logs.json")
    f = open(chat_logs_file, "r", encoding="utf-8")
    logs = json.load(f)
    logs(None, None, None)
    log = coze_config.get("coze_settings", {}).get("token")
    is_newcomer = False
    is_newcomer = False
