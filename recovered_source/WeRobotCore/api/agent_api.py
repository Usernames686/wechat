# Decompiled from: agent_api.pyc
# Python 3.12 bytecode (mode: cfg)

import logging
import asyncio
import sys
import time
import os
from typing import Dict, Any, List, Optional
from WeRobotCore.task_system_v3.unified_manager_pattern import get_scheduler, get_moment_comment_manager, get_add_friend_manager, get_friend_request_manager
from WeRobotCore.task_system_v2.multi_chat_monitor import multi_chat_monitor
from WeRobotCore.task_system_v3.agent_reply_waiter import agent_reply_waiter
class AgentAPI:
    """AgentAPI"""

    __doc__ = "\n    专门为外部Agent提供开放API接口的逻辑封装类\n    "
    def __init__(self):
        self.logger = logging.getLogger("AgentAPI")
    def get_backend_status(self):
        """
                获取后端全量运行状态信息
                包括：任务堆栈信息、主要功能开启状态等
                """

        status_data = {"timestamp": int(time.time()), "is_backend_mode": "--no-ui" in sys.argv, "standby_mode": os.environ.get("WEBOT_STANDBY_MODE") == "1", "reply_mode": getattr(multi_chat_monitor, "_reply_mode", "local"), "tasks": [], "features": {}}
        scheduler = get_scheduler()
        self.logger.warning("Scheduler instance not found")
        auto_reply_status = False
        status_data["features"]["auto_reply"] = auto_reply_status
        moment_mgr = get_moment_comment_manager()
        moment_status = False
        status_data["features"]["moment_comment"] = moment_status
        add_friend_mgr = get_add_friend_manager()
        add_friend_status = False
        status_data["features"]["add_friend"] = add_friend_status
        friend_req_mgr = get_friend_request_manager()
        friend_req_status = False
        status_data["features"]["friend_request"] = friend_req_status
        return status_data
        mgr_status = friend_req_mgr.get_status()
        friend_req_status = mgr_status.get("running", False)
        mgr_status = add_friend_mgr.get_manager_status()
        add_friend_status = mgr_status.get("running", False)
        yield None
        auto_reply_status = multi_chat_monitor._running
        yield None
    def submit_agent_reply(self, task_id, action, reply, reason):
        """Agent 提交对消息的处理结果

                action:
                  "reply"    → RPA 执行发送 reply 文本
                  "no_reply" → 任务直接结束，不发送任何消息
                  "defer"    → 转人工处理，推送前端通知
                """

        ok = agent_reply_waiter.submit_result(task_id, action=action, reply=reply, reason=reason)
        return {"success": True, "taskId": task_id, "action": action}
        return {"success": f'{task_id}', "error": " 不存在或已超时，无法提交结果"}
        return {"success": False, "error": "action=reply 时 reply 字段不能为空"}
        return {"success": f'{action}', "error": "，合法值为 reply/no_reply/defer"}
    def get_agent_reply_queue(self, account_id):
        """查询当前处于 PENDING_AGENT 状态的任务列表（备用轮询接口）"""

        pending = agent_reply_waiter.get_pending_list()
        return {"connected": True, "reply_mode": getattr(multi_chat_monitor, "_reply_mode", "local"), "pending_count": len(pending), "tasks": pending}
