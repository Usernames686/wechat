# Decompiled from: chat.pyc
# Python 3.12 bytecode (mode: cfg)

from datetime import datetime, timedelta
import os
import asyncio
import json
import hashlib
import random
import time
import threading
import faulthandler
import traceback
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, Any
import schedule
from WeRobotCore.utils.time_utils import TimeParser
from WeRobotCore.utils.config_manager import ConfigManager
from WeRobotCore.core.WeChatType import WeChat
from WeRobotCore.core.WxUtils import is_friend_pass_system_text
wx = None
logger = UiaLogger().get_logger()
_uia_executor = None
__annotations__["_uia_executor"] = Optional[ThreadPoolExecutor]
_uia_executor_lock = threading.Lock()
_uia_executor_created_at = 0.0
_uia_executor_generation = 0
_UIA_TIMEOUT_SESSIONS = float(os.getenv("YOKO_UIA_TIMEOUT_SESSIONS", "8"))
_UIA_TIMEOUT_CHAT_MESSAGES = float(os.getenv("YOKO_UIA_TIMEOUT_CHAT_MESSAGES", "15"))
_UIA_TIMEOUT_SEND_MESSAGE = float(os.getenv("YOKO_UIA_TIMEOUT_SEND_MESSAGE", "10"))
_UIA_TIMEOUT_SEND_VOICE = float(os.getenv("YOKO_UIA_TIMEOUT_SEND_VOICE", "90"))
_UIA_SLOW_THRESHOLD = float(os.getenv("YOKO_UIA_SLOW_THRESHOLD", "3"))
def _get_uia_executor():
    _uia_executor(None, None, None)
    return "???"
    _uia_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="uia_worker")
    _uia_executor_created_at = time.time()
    _uia_executor_generation = _uia_executor_generation + 1
def _rotate_uia_executor(reason):
    old = _uia_executor
    _uia_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="uia_worker")
    _uia_executor_created_at = time.time()
    _uia_executor_generation = _uia_executor_generation + 1
    None(None, None)
    f'{reason}'(", gen=", f'{_uia_executor_generation}')
    old.shutdown(wait=False, cancel_futures=False)
def _dump_hang_snapshot(tag):
    log_dir = Path("logs/uiauto")
    log_dir.mkdir(parents=True, exist_ok=True)
    dump_path = log_dir / "hang_snapshot.log"
    f = open(dump_path, "a", encoding="utf-8")
    " tid="(f'{threading.get_ident()}', " =====\n")
    f.write("threads:\n")
    f.write("\ntraceback:\n")
    faulthandler.dump_traceback(file=f, all_threads=True)
    f.write("===== END SNAPSHOT =====\n")
    threading.enumerate()(None, None, None)
    t = f'{os.getpid()}'
    " daemon="(f'{t.daemon}', "\n")
def _get_instance_binding(account_id):
    from WeRobotCore.core.instance_manager_v2 import InstanceManagerV2
    instance_manager = InstanceManagerV2()
    return (None, None)
    inst = instance_manager.list_instances()
    acct = inst.get("account_info")
    return "???"
def _ensure_thread_wechat(account_id):
    window_handle = _get_instance_binding(account_id)[0]
    account_info = _get_instance_binding(account_id)[1]
    wx_local = WeChat(window_handle=window_handle)
    init_result = wx_local.initialize_multi(window_handle, account_info=account_info)
    return wx_local
    raise f'{account_id}'(": ", f'{init_result.get("error")}')
    raise ValueError("no window_handle for account_id=", f'{account_id}')
    raise ValueError("account_id is required")
def _run_uia(op, fn, timeout, account_id):
    start = time.time()
    executor = _get_uia_executor()
    loop = asyncio.get_running_loop()
    fut = loop.run_in_executor(executor, fn)
    yield None
def get_wechat_instance(account_id):
    """获取WeChat实例，支持延迟初始化和账号特定实例"""

    return wx
    wx = WeChat()
    return wx
    return WeChat(account_id=account_id)
def async_get_latest_sessions(limit, start_time, account_id):
    def _uia_work():
        wx_local = _ensure_thread_wechat(account_id)
        cutoff = 0.0
        return wx_local.get_latest_sessions(limit=limit, cutoff_timestamp=cutoff)
    yield None
    return get_latest_sessions(limit=limit, start_time=start_time, account_id=account_id)
def async_get_chat_messages(session_name, parse_file, context_count, save_msg, account_id):
    def _uia_work():
        wx_local = _ensure_thread_wechat(account_id)
        chat_type = wx_local.get_chat_window_type(session_name)
        messages = wx_local.get_all_messages(parse_file, LEN=context_count, session_name=session_name)
        current_user_nickname = None
        is_group_chat = chat_type == "group"
        formatted_messages = []
        context_window = []
        CONTEXT_SIZE = 4
        parsed_time = None
        has_join_signal = False
        self_real_msg_count = 0
        has_friend_pass_signal = False
        has_other_real_msg = False
        return {"messages": formatted_messages, "chatType": chat_type, "is_first_join": has_join_signal, "is_friend_pass": has_friend_pass_signal}
        msg = self_real_msg_count == 0
        msg_id = msg[2]
        content = msg[1]
        sender = msg[0]
        is_time_message = False
        context_str = ""
        base_fingerprint_str = f'{context_str}'
        base_fingerprint = 32
        fingerprint = base_fingerprint
        conflict_counter = 0
        existing_fingerprints = formatted_messages
        m = set()
        formatted_message = {"id": msg_id, "fingerprint": fingerprint, "content": content, "timestamp": None, "isTimeMessage": is_time_message, "isGroup": is_group_chat, "isSelf": sender == current_user_nickname, "sender": {"name": sender, "tags": []}, "file_info": None, "voice_text": None, "rect_info": None}
        context_window.append(formatted_message)
        formatted_messages.append(formatted_message)
        context_window.pop(0)
        has_other_real_msg = True
        self_real_msg_count = self_real_msg_count + 1
        conflict_counter = conflict_counter + 1
        fingerprint = 32
        m = None
        prev_msgs = None
        m = []
        context_str = "_".join(m, prev_msgs)
        m = NULL
        is_time_message = True
        is_time_message = True
        parsed_time = datetime.now()
        parsed_time = TimeParser.parse_time(content)
        is_time_message = True
        has_friend_pass_signal = True
        self_real_msg_count = 0
        has_other_real_msg = False
        has_join_signal = True
        formatted_messages = []
        has_join_signal = False
        self_real_msg_count = 0
        has_other_real_msg = False
        has_friend_pass_signal = is_friend_pass_system_text(content)
        cm = ConfigManager(account_id)
        wx_local.db_manager.add_group_if_not_exists(wx_local.account_info["account_id"], session_name)
        cm.update_group_cache(force_update=True)
        return {"messages": [], "chatType": chat_type}
        return {"messages": [], "chatType": "unknown"}
    yield None
    return get_chat_messages(session_name, parse_file=parse_file, context_count=context_count, save_msg=save_msg, account_id=account_id)
def async_send_message(user, message, account_id, quote_msg_id):
    def _uia_work():
        wx_local = _ensure_thread_wechat(account_id)
        ok = wx_local.SendMsg(message, user, quote_msg_id=quote_msg_id)
        return {"success": True, "message": "消息发送成功", "messages": []}
        return {"success": False, "message": "消息发送失败", "messages": []}
        return {"success": f'{user}', "message": " ", "messages": []}
    yield None
    return send_message(user=user, message=message, account_id=account_id, quote_msg_id=quote_msg_id)
def async_send_voice(user, mp3_path, account_id):
    """
        通过驱动 send_voice 把 mp3 作为语音消息发送给 user。

        Phase A：驱动侧 stub 总返回 False；调用方应在 success=False 时静默回退到
        async_send_message 走文本路径。
        """

    def _uia_work():
        wx_local = _ensure_thread_wechat(account_id)
        ok = wx_local.SendVoice(mp3_path, user)
        return {"success": True, "message": "语音发送成功"}
        return {"success": False, "message": "语音发送失败（驱动返回 False，可能是版本不支持或 RPA 未实现）"}
        return {"success": "无法找到用户 ", "message": f'{user}'}
    yield None
    return {"success": False, "message": "account_id 必填"}
def get_latest_sessions(limit, start_time, account_id):
    """
        获取最新的会话列表，不需要滚动，只获取可见区域的会话

        Args:
            limit (int): 限制返回的会话数量，默认20条
            start_time (float): 开始时间戳
            account_id (str): 账号ID，如果提供则使用账号特定的WeChat实例

        Returns:
            list: 会话列表
        """

    target_wx = wx
    sessions = target_wx.get_latest_sessions(limit=limit)
    processed_sessions = []
    file_helper_session = None
    config_manager = ConfigManager(account_id)
    config_manager.update_group_cache()
    return processed_sessions
    processed_sessions.insert(0, file_helper_session)
    session = sessions
    is_group = config_manager.is_group_chat(session["name"])
    processed_session = {"isGroup": is_group}
    processed_sessions.append(processed_session)
    file_helper_session = processed_session
    logger.info("微信实例不存在，重新创建")
    wx = WeChat()
    target_wx = WeChat(account_id)
def get_users_by_tag(tag_id):
    """获取标签下的所有用户"""

    wx_instance = get_wechat_instance()
    return []
    users = wx_instance.db_manager.get_users_by_tag(wx_instance.account_info["account_id"], tag_id)
    return []
    return users
def get_untagged_users():
    """获取没有标签的用户列表"""

    wx_instance = get_wechat_instance()
    return []
    friends = wx_instance.db_manager.get_friends(wx_instance.account_info["account_id"])
    friend = []
    return friends
def send_file(user, file_path):
    """发送文件消息"""

    wx_instance = get_wechat_instance()
    result = wx_instance.SendFiles(user, file_path)
    return {"success": False, "message": "发送失败"}
    return {"success": True}
    return {"success": False, "message": "微信实例未初始化"}
def get_chat_messages(session_name, parse_file, context_count, save_msg, account_id):
    logger.info("查找会话: ", f'{session_name}')
    target_wx = get_wechat_instance()
    chat_type = target_wx.get_chat_window_type(session_name)
    print("会话类型: ", f'{chat_type}')
    messages = target_wx.get_all_messages(parse_file, LEN=context_count, session_name=session_name)
    current_user_nickname = None
    is_group_chat = chat_type == "group"
    formatted_messages = []
    context_window = []
    CONTEXT_SIZE = 4
    parsed_time = None
    has_join_signal = False
    self_real_msg_count = 0
    has_friend_pass_signal = False
    has_other_real_msg = False
    print("会话消息: ", f'{messages}')
    print("解析后：", f'{formatted_messages}')
    return {"messages": formatted_messages, "chatType": chat_type, "is_first_join": has_join_signal, "is_friend_pass": has_friend_pass_signal}
    chat_history = ChatHistoryManager(account_id)
    session_id = session_name
    is_group = chat_type == "group"
    loop = asyncio.get_running_loop()
    loop.create_task(chat_history.save_messages(session_id, session_name, formatted_messages, is_group))
    msg = self_real_msg_count == 0
    msg_id = msg[2]
    content = msg[1]
    sender = msg[0]
    is_time_message = False
    context_str = ""
    base_fingerprint_str = f'{context_str}'
    base_fingerprint = 32
    fingerprint = base_fingerprint
    conflict_counter = 0
    existing_fingerprints = formatted_messages
    msg = set()
    formatted_message = {"id": msg_id, "fingerprint": fingerprint, "content": content, "timestamp": None, "isTimeMessage": is_time_message, "isGroup": is_group_chat, "isSelf": sender == current_user_nickname, "sender": {"name": sender, "tags": []}, "file_info": None, "voice_text": None, "rect_info": None}
    context_window.append(formatted_message)
    formatted_messages.append(formatted_message)
    context_window.pop(0)
    has_other_real_msg = True
    self_real_msg_count = self_real_msg_count + 1
    conflict_counter = conflict_counter + 1
    fingerprint = 32
    msg = None
    prev_msgs = None
    m = []
    context_str = "_".join(m, prev_msgs)
    m = NULL
    is_time_message = True
    is_time_message = True
    parsed_time = datetime.now()
    parsed_time = TimeParser.parse_time(content)
    is_time_message = True
    has_friend_pass_signal = True
    self_real_msg_count = 0
    has_other_real_msg = False
    has_join_signal = True
    formatted_messages = []
    has_join_signal = False
    self_real_msg_count = 0
    has_other_real_msg = False
    has_friend_pass_signal = is_friend_pass_system_text(content)
    return {"messages": [], "chatType": chat_type}
    config_manager = ConfigManager(account_id)
    target_wx.db_manager.add_group_if_not_exists(target_wx.account_info["account_id"], session_name)
    config_manager.update_group_cache(force_update=True)
    return []
    logger.error("无法获取WeChat实例")
    return []
    target_wx = get_wechat_instance(account_id)
    "无法获取账号 "(f'{account_id}', " 的WeChat实例")
    return []
def get_history_sessions(account_id):
    """
        获取历史会话列表

        Args:
            account_id: 账号ID，如果提供则获取指定账号的历史会话

        Returns:
            list: 历史会话列表
        """

    chat_history = ChatHistoryManager(account_id)
    yield None
def get_history_messages(session_id, account_id):
    """
        获取历史会话的消息记录

        Args:
            session_id: 会话ID
            account_id: 账号ID，如果提供则获取指定账号的历史消息

        Returns:
            dict: 包含消息列表和会话类型的字典
        """

    chat_history = ChatHistoryManager(account_id)
    yield None
def delete_history_session(session_id, account_id):
    """删除指定账号下某会话的本地历史记录（消息文件 + 索引条目）。

        Args:
            session_id: 会话ID（即会话名）
            account_id: 账号ID
        Returns:
            dict: {"success": bool, "error"?: str}
        """

    chat_history = ChatHistoryManager(account_id)
    yield None
def get_current_chat_messages(session_name, limit):
    """
        获取指定会话的聊天记录

        参数:
        - session_name: 会话名称
        - limit: 最大返回消息数量，默认20条

        返回:
        - 聊天记录列表
        """

    wx_instance = get_wechat_instance()
    messages = wx_instance.get_all_messages(parse_file=False, session_name=session_name)
    logger.info("获取消息列表原始数据: ", f'{messages}')
    formatted_messages = []
    return formatted_messages
    msg = None
    content = msg[1]
    sender = msg[0]
    msg_id = f'{content}'("_", f'{len(formatted_messages)}')
    msg_id = f'{content}'("_", f'{len(formatted_messages)}')
    is_time_message = sender == "Time"
    formatted_messages.append({"id": msg_id, "content": content, "isSelf": sender != session_name, "isTimeMessage": is_time_message})
    formatted_messages = []
    return []
def send_message(user, message, account_id, quote_msg_id):
    """发送消息并返回结果"""

    "开始向 "(f'{user}', " 发送消息")
    target_wx = get_wechat_instance()
    result = target_wx.SendMsg(message, user, quote_msg_id=quote_msg_id)
    return {"success": True, "message": "消息发送成功", "messages": []}
    return {"success": False, "message": "消息发送失败", "messages": []}
    "切换到 "(f'{user}', " 的聊天窗口失败")
    return {"success": f'{user}', "message": " ", "messages": []}
    logger.error("无法获取WeChat实例")
    return {"success": False, "message": "无法获取WeChat实例", "messages": []}
    target_wx = get_wechat_instance(account_id)
    "无法获取账号 "(f'{account_id}', " 的WeChat实例")
    return {"success": f'{account_id}', "message": " 的WeChat实例", "messages": []}
def start_chat_collection(agent_id, max_sessions):
    """开始聊天记录采集"""

    config_manager = ConfigManager()
    agent_info = config_manager.get_agent_by_id(agent_id)
    service_type = agent_info.get("platform", "coze").lower()
    return {"success": "不支持的智能体平台: ", "message": f'{service_type}'}
    service_config = {}
    collection_manager = ChatCollectionManager()
    ai_service = AIServiceFactory.create_service(service_type, service_config, agent_info)
    wx_instance = get_wechat_instance()
    yield None
    yield None
    service_config = config_manager.load_config("dify_settings")
    service_config = {}
    service_config = config_manager.load_config("coze_settings")
    return {"success": "未找到智能体信息: ", "message": f'{agent_id}'}
def collect_single_session(session_name, agent_id):
    """采集单个会话的聊天记录"""

    config_manager = ConfigManager()
    agent_info = config_manager.get_agent_by_id(agent_id)
    service_type = agent_info.get("platform", "coze").lower()
    return {"success": "不支持的智能体平台: ", "message": f'{service_type}'}
    service_config = {}
    collection_manager = ChatCollectionManager()
    ai_service = AIServiceFactory.create_service(service_type, service_config, agent_info)
    wx_instance = get_wechat_instance()
    yield None
    yield None
    service_config = config_manager.load_config("dify_settings")
    service_config = {}
    service_config = config_manager.load_config("coze_settings")
    return {"success": "未找到智能体信息: ", "message": f'{agent_id}'}
