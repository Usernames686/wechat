# Decompiled from: agent_reply_waiter.pyc
# Python 3.12 bytecode (mode: cfg)

"""
Agent 回复等待器

持有所有处于 PENDING_AGENT 状态的任务等待句柄。
AutoReplyAdapter 调用 register/wait_result，
Agent 通过 HTTP 回调时调用 submit_result。
"""

__doc__ = "\nAgent 回复等待器\n\n持有所有处于 PENDING_AGENT 状态的任务等待句柄。\nAutoReplyAdapter 调用 register/wait_result，\nAgent 通过 HTTP 回调时调用 submit_result。\n"
import asyncio
import time
from typing import Dict, Optional
class AgentReplyWaiter:
    """AgentReplyWaiter"""

    def __init__(self):
        self._pending = {}
    def register(self, task_id, session_name):
        """注册一个等待 Agent 回调的任务"""

        self._pending[task_id] = {"event": asyncio.Event(), "result": None, "registered_at": time.time(), "session_name": session_name}
    def wait_result(self, task_id, timeout):
        """阻塞等待 Agent 回调，超时返回 None"""

        entry = self._pending.get(task_id)
        yield None
    def submit_result(self, task_id, action, reply, reason):
        """Agent 提交处理结果，唤醒等待协程"""

        entry = self._pending.get(task_id)
        entry["result"] = {"action": action, "reply": reply, "reason": reason}
        entry["event"].set()
        return True
        return False
    def is_pending(self, task_id):
        return task_id in self._pending
    def get_pending_list(self):
        """返回所有待处理任务摘要（用于队列查询接口）"""

        now = time.time()
        entry = tid
        tid = []
        return self._pending.items()
        tid = entry[0]
        entry = entry[1]
agent_reply_waiter = AgentReplyWaiter()
