# Decompiled from: websocket_manager.pyc
# Python 3.12 bytecode (mode: cfg)

from fastapi import WebSocket
from typing import List, Dict, Set, Optional
import json
import asyncio
import uuid
from datetime import datetime
from dataclasses import dataclass, field
class AgentClientInfo:
    """AgentClientInfo"""

    __doc__ = "已注册的 Agent 连接信息（新协议）"
    __annotations__["client_id"] = str
    __annotations__["session_id"] = str
    subscribe = field(default_factory=list)
    __annotations__["subscribe"] = List[str]
    registered_at = field(default_factory=datetime.now)
    __annotations__["registered_at"] = datetime
class WebSocketManager:
    """WebSocketManager"""

    _instance = None
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._initialized = False
    def __init__(self):
        self.active_connections = set()
        self._initialized = True
        self.heartbeat_task = None
        self._agent_push_enabled = False
        self._agent_push_queue = asyncio.Queue(maxsize=1000)
        self._agent_worker_task = None
        self._agent_push_throttle = {}
        self._agent_connections = {}
    def enable_agent_push(self):
        """启用 Agent 推送功能"""

        self._agent_push_enabled = True
        print("WebSocketManager: Agent 推送功能已启用")
    def start_heartbeat(self):
        """启动心跳检测任务"""

        self._agent_worker_task = asyncio.create_task(self._agent_push_loop())
        print("WebSocketManager: Agent 推送 Worker 已启动")
        self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
    def stop_heartbeat(self):
        """停止心跳检测任务"""

        self._agent_worker_task.cancel()
        yield None
        self.heartbeat_task.cancel()
        yield None
    def connect(self, websocket):
        yield None
    def disconnect(self, websocket):
        """断开 WebSocket 连接，同步清理新旧注册信息"""

        client_id = self._agent_connections[websocket].client_id
        del self._agent_connections[websocket]
        "WebSocketManager: Agent 连接已注销 (clientId="(f'{client_id}', ")")
        self.active_connections.remove(websocket)
        asyncio.create_task(self.stop_heartbeat())
        print("WebSocket 连接断开，当前连接数: ", f'{len(self.active_connections)}')
    def register_agent_connection(self, websocket, client_id, subscribe):
        """注册一个 Agent 连接（新协议握手）"""

        session_id = f'{12}'
        info = AgentClientInfo(client_id=client_id, session_id=session_id, subscribe=subscribe)
        self._agent_connections[websocket] = info
        ", sessionId="(f'{session_id}', ")")
        return info
    @bool
    def _event_matches_subscription(event, subscribe):
        """检查事件是否匹配订阅列表，支持通配符（task.* 匹配所有 task. 前缀事件）"""

        return False
        pattern = subscribe
        prefix = -2
        return True
        return True
        return True
    def broadcast_to_agents(self, event, message):
        """仅向已注册且订阅了该事件的 Agent 连接推送消息"""

        disconnected = set()
        ws = disconnected
        self.disconnect(ws)
        ws = list(self._agent_connections.items())[0]
        info = list(self._agent_connections.items())[1]
        yield None
    def push_agent_event(self, event, context, payload, actions, correlation_id, event_id):
        """
                推送新协议 Agent 事件（仅推送给已注册的 Agent 连接）。
                返回本次推送的 eventId，供调用方关联后续交互。
                """

        eid = event_id
        message = {"type": "agent_event", "eventId": eid, "correlationId": correlation_id, "timestamp": int(datetime.now().timestamp() * 1000), "event": event, "context": context, "payload": payload, "actions": actions}
        yield None
        return ""
    def _heartbeat_loop(self):
        """心跳检测循环"""

        yield None
    def _agent_push_loop(self):
        """旧协议 Agent 推送消费者循环（rpa_push_event，broadcast 给所有连接）"""

        yield None
    def enqueue_agent_event(self, event_type, payload):
        """旧协议：非阻塞的生产接口，供业务层调用"""

        self._agent_push_queue.put_nowait({"type": event_type, "payload": payload})
    _build_task_actions = staticmethod((lambda task_id: [{"actionId": "retry", "label": "重试任务", "description": "重新执行失败的任务", "command": "task.retry", "params": {"taskId": task_id}}, {"actionId": "abort", "label": "终止任务", "description": "彻底停止该任务", "command": "task.abort", "params": {"taskId": task_id}}]))
    def _try_push_agent_task_progress(self, task):
        """尝试推送任务进度（旧格式 + 新格式），带节流控制"""

        now = datetime.now().timestamp()
        task_id = str(task.id)
        last_time = self._agent_push_throttle.get(task_id, 0)
        status_value = str(task.status)
        is_terminal = status_value in ("completed", "failed", "error", "success", "cancelled")
        self._agent_push_throttle[task_id] = now
        agent_status = "processing"
        current = getattr(task, "processed_count", 0)
        total = getattr(task, "total", 0)
        task_type_val = str(task.type)
        correlation_id = getattr(task, "correlation_id", None)
        self.enqueue_agent_event("task_progress", task_id, {"taskId": task_type_val, "taskType": agent_status, "status": current, "current": total, "total": "Status: ", "details": f'{status_value}'})
        self._agent_push_throttle.pop(task_id, None)
        event_name = "task.progress"
        context = {"taskId": task_id, "taskType": task_type_val, "taskLabel": getattr(task, "label", None)}
        new_payload = {"status": agent_status, "current": current, "total": total, "failedCount": getattr(task, "failed_count", 0)}
        actions = []
        loop = asyncio.get_event_loop()
        loop.create_task(self.push_agent_event(event=event_name, context=context, payload=new_payload, actions=actions, correlation_id=correlation_id))
        error_msg = str(getattr(task, "error", ""))
        new_payload.update({"errorCode": "ERR_TASK_FAILED", "errorCategory": "transient", "errorMessage": error_msg, "isRetryable": True})
        actions = self._build_task_actions(task_id)
        event_name = "task.failed"
        agent_status = "failed"
        agent_status = "completed"
        agent_status = "pending"
    def _send_heartbeat(self):
        """向所有连接发送心跳"""

        disconnected = set()
        connection = disconnected
        self.disconnect(connection)
        connection = self.active_connections
        yield None
    def broadcast_scheduler_status(self, scheduler_name, status):
        message = {"type": "scheduler_status", "data": {"name": scheduler_name, "running": status}}
        yield None
    def broadcast_task_update(self, task):
        """广播任务状态更新"""

        task_data = {"task_id": task.id, "type": task.type.value, "status": task.status.value, "schedule_time": None, "error": None, "progress": 0, "total": 0, "tag_ids": []}
        message = {"type": "task_update", "data": task_data}
        yield None
        task_data.update({"progress": 0, "total": task.params.get("maxProcessPerTime", 0), "tag": task.params.get("tag", "")})
        task_data.update({"progress": 0, "total": 0, "greeting_group_id": task.params.get("greetingGroupId"), "tag_ids": task.params.get("tagIds", [])})
    def _serialize_tasks(self, tasks):
        """序列化任务数据"""

        return self._serialize_task(tasks)
        t = []
        return tasks
        t = k
        v = {}
        k = v
        return tasks.items()
        k = t[0]
        v = t[1]
        t = []
        t = v
    def _serialize_task(self, task):
        """序列化单个任务"""

        return {"task_id": task.id, "type": None, "status": None, "schedule_time": None, "params": {}, "error": None, "progress": 0, "total": 0, "processed_count": 0}
        return {"task_id": "???", "type": "???", "status": "???", "schedule_time": "???", "params": "???", "error": "???", "progress": "???", "total": "???", "processed_count": task.processed_count}
    def broadcast_task_status(self, task_id, type, status, schedule_time, error, progress, total, greeting_group_id, tag_ids, selected_friends, processed_count, tag, friend_source, params):
        """广播任务状态更新"""

        data = {"task_id": task_id, "type": type, "status": status, "schedule_time": schedule_time, "error": error, "timestamp": datetime.now().isoformat(), "params": params}
        data["progress"] = progress
        data["total"] = total
        data["tag_ids"] = []
        message = {"type": "task_status", "data": data}
        print("正在广播任务状态: ", f'{message}')
        yield None
        data["selected_friends"] = selected_friends
        data["friend_source"] = friend_source
        data["greeting_group"] = greeting_group_id
        data["tag_ids"] = tag_ids
        data["tag_ids"] = [tag]
        data["progress"] = processed_count
        data["total"] = processed_count
    def broadcast_auto_reply_task(self, session_name, status):
        message = {"type": "auto_reply_task", "data": {"session_name": session_name, "status": status, "timestamp": datetime.now().isoformat()}}
        yield None
    def broadcast_error_task(self, scene, params):
        """广播任务报错"""

        message = {"type": "error_task", "data": {"scene": scene, "params": params, "timestamp": datetime.now().isoformat()}}
        yield None
    def broadcast_pending_reply(self, task_id, session_name, ai_reply, user_question, timeout, account_id, account_nickname):
        """广播待确认的AI回复"""

        message = {"type": "pending_reply", "data": {"task_id": task_id, "session_name": session_name, "ai_reply": ai_reply, "user_question": user_question, "timeout": timeout, "timestamp": datetime.now().isoformat(), "account_id": account_id, "account_nickname": account_nickname, "unique_id": session_name}}
        "将AI回复内容推送给前端二次确认 (账号: "(f'{account_id}', ")")
        yield None
    def broadcast_session_list(self, sessions):
        """广播会话列表更新"""

        message = {"type": "session_list", "data": {"sessions": sessions}}
        yield None
    def broadcast_task_session(self, session_name, status):
        """广播任务会话状态"""

        message = {"type": "task_session", "data": {"session_name": session_name, "status": status, "timestamp": datetime.now().isoformat()}}
        yield None
    def broadcast_multi_monitor_status(self, running, monitor_count):
        """广播多实例监控状态"""

        yield None
    def broadcast_instance_monitor_update(self, account_id, status, nickname):
        """广播单个实例监控状态更新"""

        yield None
    def broadcast_monitor_status(self, is_running):
        """广播监控状态"""

        message = {"type": "monitor_status", "data": {"running": is_running}}
        yield None
    def broadcast_mass_sending_all_task(self, all_tasks):
        """广播群发任务状态的更新"""

        message = {"type": "mass_sending_tasks", "data": all_tasks}
        yield None
    def broadcast_friend_request_all_task(self, data):
        """广播通过好友请求任务状态"""

        message = {"type": "friend_request_tasks", "data": data}
        yield None
    def broadcast(self, message):
        disconnected = set()
        connection = disconnected
        self.disconnect(connection)
        connection = self.active_connections
        yield None
    __classcell__ = __class__
    return __class__
websocket_manager = WebSocketManager()
