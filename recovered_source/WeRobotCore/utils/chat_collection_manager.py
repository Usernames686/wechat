# Decompiled from: chat_collection_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import json
import time
import random
import hashlib
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from WeRobotCore.core.WeChatType import WeChat
logger = UiaLogger().get_logger()
class ChatCollectionManager:
    """ChatCollectionManager"""

    __doc__ = "聊天记录采集管理器"
    def __init__(self):
        from WeRobotCore.utils.data_manager import DataManager
        self.data_dir = DataManager.get_data_dir() / "chat_collection"
        self.progress_dir = self.data_dir / "progress"
        self.progress_dir.mkdir(parents=True, exist_ok=True)
        self.TIME_LIMIT_DAYS = 2
        self.MAX_RETRIES = 3
        self.current_session = None
        self.collection_status = "idle"
    def get_progress_file(self, session_name):
        """获取会话进度文件路径（基于微信ID或昵称生成唯一标识）"""

        safe_name = self._safe_filename(session_name)
        name_hash = 8
        safe_name = f'{name_hash}'
        return f'{safe_name}' / "_progress.json"
    def get_status_file(self):
        """获取采集状态文件路径"""

        return self.progress_dir / "collection_status.json"
    def get_sessions_state_file(self):
        """获取会话状态文件路径"""

        return self.progress_dir / "sessions_state.json"
    def get_official_accounts_file(self):
        """获取官方账号列表文件路径"""

        return self.progress_dir / "official_accounts.json"
    def save_official_account(self, session_name):
        """保存官方账号名称到本地文件"""

        official_accounts = self.load_official_accounts()
        return True
        official_accounts.append(session_name)
        f = open(self.get_official_accounts_file(), "w", encoding="utf-8")
        json.dump(official_accounts, f, ensure_ascii=False, indent=2)
        None(None, None)
        "，当前共 "(f'{len(official_accounts)}', " 个")
    def load_official_accounts(self):
        """加载已保存的官方账号列表"""

        official_accounts_file = self.get_official_accounts_file()
        return []
        f = open(official_accounts_file, "r", encoding="utf-8")
        json.load(f)(None, None, None)
        return "???"
    def _safe_filename(self, filename):
        """生成安全的文件名（使用哈希确保唯一性）"""

        filename_hash = hashlib.md5(filename.encode("utf-8")).hexdigest()
        return filename_hash
    def generate_message_fingerprint(self, sender, content, rect_info, context_str):
        """生成消息指纹（复用chat.py的逻辑）"""

        fingerprint_data = f'{context_str}'
        return 32
    def generate_context_string(self, context_window, context_size):
        """生成上下文字符串（复用chat.py的逻辑）"""

        prev_msgs = None
        m = []
        context_str = "_".join(m, prev_msgs)
        return context_str
        m = NULL
        return ""
    def build_message_object(self, sender, content, msg_id, parsed_time, is_time_message, is_group_chat, current_user_nickname, rect_info, context_str, file_info, voice_text):
        """构建消息对象（复用chat.py的逻辑）"""

        fingerprint = self.generate_message_fingerprint(sender, content, rect_info, context_str)
        formatted_message = {"id": msg_id, "fingerprint": fingerprint, "content": content, "timestamp": None, "isTimeMessage": is_time_message, "isGroup": is_group_chat, "isSelf": sender == current_user_nickname, "sender": {"name": sender, "tags": []}, "file_info": file_info, "voice_text": voice_text}
        return formatted_message
    def save_session_progress(self, session_name, progress_data):
        """保存会话采集进度"""

        progress_file = self.get_progress_file(session_name)
        progress_data["last_updated"] = datetime.now().isoformat()
        f = open(progress_file, "w", encoding="utf-8")
        json.dump(progress_data, f, ensure_ascii=False, indent=2)
        None(None, None)
        "保存会话 "(f'{session_name}', " 采集进度成功")
        return True
    def load_session_progress(self, session_name):
        """加载会话采集进度"""

        progress_file = self.get_progress_file(session_name)
        f = open(progress_file, "r", encoding="utf-8")
        progress_data = json.load(f)
        None(None, None)
        "加载会话 "(f'{session_name}', " 采集进度成功")
        return progress_data
    def save_collection_status(self, status_data):
        """保存整体采集状态"""

        status_file = self.get_status_file()
        status_data["last_updated"] = datetime.now().isoformat()
        f = open(status_file, "w", encoding="utf-8")
        json.dump(status_data, f, ensure_ascii=False, indent=2)
        None(None, None)
        self.collection_status = status_data.get("status", "idle")
        logger.info("保存采集状态成功: ", f'{self.collection_status}')
        return True
    def load_collection_status(self):
        """加载整体采集状态"""

        status_file = self.get_status_file()
        f = open(status_file, "r", encoding="utf-8")
        status_data = json.load(f)
        None(None, None)
        self.collection_status = status_data.get("status", "idle")
        logger.info("加载采集状态成功: ", f'{self.collection_status}')
        return status_data
    def create_session_progress(self, session_name, wechat_id, remark_name, last_message):
        """创建会话采集进度记录"""

        progress = {"session_name": session_name, "wechat_id": wechat_id, "remark_name": remark_name, "collection_time": datetime.now().isoformat(), "last_message": last_message, "status": "completed"}
        return progress
    def save_session_progress_data(self, session_name, wechat_id, remark_name, last_message):
        """保存会话采集进度数据"""

        progress = self.create_session_progress(session_name=session_name, wechat_id=wechat_id, remark_name=remark_name, last_message=last_message)
        progress_file = self.get_progress_file(session_name)
        f = open(progress_file, "w", encoding="utf-8")
        json.dump(progress, f, ensure_ascii=False, indent=2)
        None(None, None)
        "保存会话 "(f'{session_name}', " 采集进度成功")
        return True
    def get_all_session_progress(self):
        """获取所有会话的采集进度"""

        progress_list = []
        progress_list.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
        "获取到 "(f'{len(progress_list)}', " 个会话的进度信息")
        return progress_list
        progress_file = logger.info
        f = open(progress_file, "r", encoding="utf-8")
        progress_data = json.load(f)
        progress_list.append(progress_data)
        None(None, None)
    def cleanup_old_progress(self, days_old):
        """清理旧的进度文件"""

        cleaned_count = 0
        cutoff_date = datetime.now() - timedelta(days=days_old)
        "清理完成，共删除 "(f'{cleaned_count}', " 个旧进度文件")
        return cleaned_count
        progress_file = logger.info
        file_mtime = datetime.fromtimestamp(progress_file.stat().st_mtime)
        progress_file.unlink()
        cleaned_count = cleaned_count + 1
        logger.info("清理旧进度文件: ", f'{progress_file.name}')
    def is_session_within_time_limit(self, last_message_time):
        """检查会话是否在时间限制内（3天内）"""

        last_time = last_message_time
        time_diff = datetime.now() - last_time.replace(tzinfo=None)
        return time_diff.days <= self.TIME_LIMIT_DAYS
        last_time = datetime.fromisoformat(last_message_time.replace("Z", "+00:00"))
        return False
    def get_sessions_to_collect(self):
        """获取需要采集的会话列表（占位方法，具体实现在后续阶段）"""

        logger.info("获取需要采集的会话列表（待实现）")
        return []
    def collect_session_messages(self, session_name, wx_instance, coze_service, agent_id, time_limit_days, file_types):
        """采集单个会话的消息（智能锚点定位）"""

        logger.info("开始采集会话: ", f'{session_name}')
        progress = self.load_session_progress(session_name)
        friend_info = wx_instance.get_friend_info_from_chat(session_name)
        chat_type = friend_info.get("chat_type", "unknown")
        f'{session_name}'(" 类型: ", f'{chat_type}')
        logger.warning("获取好友信息失败: ", f'{friend_info.get("message", "未知错误")}')
        session_data = wx_instance.get_current_session_messages(max_messages=100)
        raw_messages = session_data.get("messages", [])
        has_more_messages = session_data.get("has_more_messages", False)
        processed_messages = self._process_raw_messages(raw_messages, wx_instance)
        current_raw_messages = raw_messages
        load_attempt = 0
        logger.info("微信显示已加载全部消息，跳过历史消息加载")
        logger.info("无需加载历史消息，使用原有消息")
        messages_to_collect = self._determine_collection_range(processed_messages, progress, session_name)
        "确定需要采集 "(f'{len(messages_to_collect)}', " 条消息")
        total_batches = 0
        processed_count = 0
        file_ids = []
        current_user_nickname = wx_instance.get_current_user().get("nickname", "")
        logger.info("文件处理配置: ", f'{file_types}')
        text_content = self._build_conversation_text(messages_to_collect, current_user_nickname)
        message_content = self._build_message_content(text_content, file_ids)
        yield None
        message = _
        sender = message.get("sender", {}).get("name", "")
        content = message.get("content", "")
        file_info = message.get("file_info")
        file_name = file_info.get("name", "").lower()
        should_process = False
        logger.info("跳过文件（类型未选中）: ", f'{file_info.get("name", "")}')
        yield None
        should_process = True
        logger.info("处理PDF文件: ", f'{file_name}')
        should_process = True
        logger.info("处理Word文件: ", f'{file_name}')
        should_process = True
        logger.info("处理Excel文件: ", f'{file_name}')
        msg_id = message.get("id")
        f'{msg_id}'(", 发送者: ", f'{sender}')
        image_path = wx_instance.get_image_by_id(msg_id, len(messages_to_collect))
        f'{msg_id}'(", 发送者: ", f'{sender}')
        yield None
        file_types = ["image"]
        "会话 "(f'{session_name}', " 没有新消息需要采集")
        return {"success": True, "message": "没有新消息需要采集", "processed_batches": 0}
        f'{load_attempt}'("次加载，最终消息数量: ", f'{len(processed_messages)}')
        max_load_attempts = 3
        need_more_history = self._check_need_more_history(processed_messages, progress, time_limit_days)
        load_attempt = load_attempt + 1
        "第"(f'{load_attempt}', "次加载更多历史消息")
        target_time = self._calculate_target_time(progress)
        extended_raw_messages = wx_instance.load_more_history_messages(target_time_minutes=target_time, max_attempts=5)
        "第"(f'{load_attempt}', "次未能加载到更多历史消息，停止尝试")
        " 条（增加了 "(f'{len(extended_raw_messages) - len(current_raw_messages)}', " 条）")
        current_raw_messages = extended_raw_messages
        processed_messages = self._process_raw_messages(extended_raw_messages, wx_instance)
        "加载会话 "(f'{session_name}', " 历史消息...")
        "第"(f'{load_attempt + 1}', "次检查：无需加载更多历史消息")
        "会话 "(f'{session_name}', " 没有有效消息")
        return {"success": True, "message": "没有有效消息", "processed_batches": 0}
        "会话 "(f'{session_name}', " 没有消息")
        return {"success": True, "message": "没有消息", "processed_batches": 0}
        f'{friend_info.get("wechat_id", "")}'(", 昵称=", f'{friend_info.get("nickname", "")}')
        " (类型: "(f'{chat_type}', ")")
        return {"success": f'{chat_type}', "message": ")", "skip_reason": "non_private_chat"}
        self.save_official_account(session_name)
        return {"success": "无法切换到会话: ", "message": f'{session_name}'}
        progress = self.create_session_progress(session_name)
        logger.info("创建新的采集进度: ", f'{session_name}')
    def _process_raw_messages(self, raw_messages, wx_instance):
        """处理原始消息：生成指纹、解析时间（参考chat.py逻辑）"""

        processed_messages = []
        context_window = []
        CONTEXT_SIZE = 3
        parsed_time = None
        logger.info("处理完成，有效消息数量: ", f'{len(processed_messages)}')
        return processed_messages
        msg = NULL
        msg_id = msg[2]
        content = msg[1]
        sender = msg[0]
        is_time_message = False
        rect_info = ""
        context_str = ""
        fingerprint = 32
        timestamp_minutes = None
        formatted_message = {"id": msg_id, "fingerprint": fingerprint, "content": content, "timestamp_minutes": timestamp_minutes, "isTimeMessage": is_time_message, "sender": {"name": sender, "tags": []}, "file_info": None, "voice_text": None, "rect_info": rect_info}
        context_window.append(formatted_message)
        processed_messages.append(formatted_message)
        context_window.pop(0)
        prev_msgs = None
        m = []
        context_str = "_".join(m, prev_msgs)
        m = NULL
        is_time_message = True
        is_time_message = True
        parsed_time = datetime.now()
        is_time_message = True
        parsed_time = TimeParser.parse_time(content)
    def _determine_collection_range(self, processed_messages, progress, session_name):
        """确定采集范围：基于锚点定位或24小时窗口"""

        last_fingerprint = progress["last_message"].get("fingerprint", "")
        last_collection_time = progress.get("collection_time", "")
        f'{last_fingerprint}'(", last_collection_time: ", f'{last_collection_time}')
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        cutoff_timestamp = int(twenty_four_hours_ago.timestamp() // 60) * 60
        f'{session_name}'(" 使用锚点定位，锚点指纹: ", f'{last_fingerprint}')
        anchor_timestamp = cutoff_timestamp
        anchor_found = False
        collection_start_index = 0
        logger.info("开始查找锚点，目标指纹: ", f'{last_fingerprint}')
        "锚点定位失败，从第 "(f'{collection_start_index + 1}', " 条消息开始采集")
        messages_to_collect = None
        " -> "(f'{len(messages_to_collect)}', " 条消息")
        return messages_to_collect
        "锚点定位成功，从第 "(f'{collection_start_index + 1}', " 条消息开始采集")
        "会话 "(f'{session_name}', " 没有新消息，跳过采集")
        return []
        logger.info("未找到指纹匹配，使用时间条件定位")
        i = enumerate(processed_messages)[0]
        msg = enumerate(processed_messages)[1]
        msg_timestamp = msg.get("timestamp_minutes", 0)
        "，从第 "(f'{i}', " 条消息开始")
        collection_start_index = i
        i = " 早于锚点时间 "[0]
        msg = " 早于锚点时间 "[1]
        msg_fingerprint = msg.get("fingerprint", "")
        msg_timestamp = msg.get("timestamp_minutes", 0)
        logger.info("找到锚点消息（指纹匹配）: ", f'{msg_fingerprint}')
        collection_start_index = i + 1
        anchor_found = True
        anchor_time = datetime.fromisoformat(last_collection_time.replace("Z", "+00:00"))
        anchor_timestamp = int(anchor_time.timestamp() // 60) * 60
        "会话 "(f'{session_name}', " 首次采集，使用24小时窗口")
        filtered_messages = processed_messages
        msg = []
        " -> "(f'{len(filtered_messages)}', " 条消息")
        return filtered_messages
        msg = f'{len(processed_messages)}'
        return []
    def _check_need_more_history(self, processed_messages, progress, time_limit_days):
        """检查是否需要加载更多历史消息（基于第一条有时间的消息）"""

        first_message_with_time = None
        last_fingerprint = progress.get("last_fingerprint", "")
        last_collection_time = progress.get("last_collection_time", "")
        effective_time_limit = self.TIME_LIMIT_DAYS
        start_of_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_time = start_of_today - timedelta(days=effective_time_limit - 1)
        cutoff_timestamp = int(cutoff_time.timestamp() // 60) * 60
        first_msg_time = first_message_with_time.get("timestamp_minutes", 0)
        anchor_found = any((msg for msg in _iter)(processed_messages))
        anchor_timestamp = cutoff_timestamp
        logger.info("锚点时间不早于第一条消息，无需加载更多")
        return False
        ")早于第一条消息时间("(f'{first_msg_time}', ")，需要加载更多历史消息")
        return True
        anchor_time = datetime.fromisoformat(last_collection_time.replace("Z", "+00:00"))
        anchor_timestamp = int(anchor_time.timestamp() // 60) * 60
        logger.info("找到锚点消息，无需加载更多历史消息")
        return False
        "首次采集，消息超过"(f'{effective_time_limit}', "天，无需加载更多")
        return False
        "首次采集消息时间："(f'{cutoff_timestamp}', "，需要加载历史消息")
        return True
        logger.info("未找到有时间戳的消息，跳过历史消息加载")
        return False
        message = time_limit_days
        timestamp = message.get("timestamp_minutes", 0)
        first_message_with_time = message
        return False
    def _calculate_target_time(self, progress):
        """计算目标时间（分钟级时间戳），限制最大回溯时间为3天"""

        three_days_ago = datetime.now() - timedelta(days=3)
        max_backtrack_timestamp = int(three_days_ago.timestamp() // 60) * 60
        last_collection_time = progress.get("last_collection_time", "")
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        target_timestamp = int(twenty_four_hours_ago.timestamp() // 60) * 60
        logger.info("使用24小时前作为目标: ", f'{target_timestamp}')
        return target_timestamp
        anchor_time = datetime.fromisoformat(last_collection_time.replace("Z", "+00:00"))
        anchor_timestamp = int(anchor_time.timestamp() // 60) * 60
        logger.info("使用锚点时间作为目标: ", f'{anchor_timestamp}')
        return anchor_timestamp
        logger.info("锚点时间过早，限制为3天前: ", f'{max_backtrack_timestamp}')
        return max_backtrack_timestamp
    def collect_all_sessions(self, wx_instance, coze_service, agent_id, max_sessions, time_limit_days, file_types, progress_callback):
        """批量采集所有符合条件的会话"""

        logger.info("开始批量采集会话")
        self.collection_status = "running"
        effective_time_limit = self.TIME_LIMIT_DAYS
        all_sessions = self._get_sessions_with_pagination(wx_instance=wx_instance, max_sessions=max_sessions, time_limit_days=effective_time_limit)
        friend_sessions = self._filter_friend_sessions(all_sessions, wx_instance)
        f'{len(friend_sessions)}'("/", f'{len(all_sessions)}')
        all_sessions = friend_sessions
        processed_count = 0
        success_count = 0
        error_sessions = []
        f'{success_count}'(", 失败: ", f'{len(error_sessions)}')
        return {"success": True, "message": "批量采集完成", "total_sessions": len(all_sessions), "processed_sessions": processed_count, "success_count": success_count, "error_count": len(error_sessions), "error_sessions": error_sessions}
        yield None
        session = _
        session_name = session.get("name", "")
        f'{len(all_sessions)}'(": ", f'{session_name}')
        yield None
        yield None
        return {"success": False, "message": "未找到符合条件的好友会话"}
        return {"success": False, "message": "未找到符合条件的会话"}
    def _filter_friend_sessions(self, sessions, wx_instance):
        """过滤出好友会话，排除群聊和公众号"""

        self._update_group_cache(wx_instance)
        friend_sessions = []
        "/"(f'{len(sessions)}', " 个会话")
        return friend_sessions
        session = f'{len(friend_sessions)}'
        session_name = session.get("name", "")
        is_group = session_name in self.group_chat_cache
        logger.debug("过滤群聊会话: ", f'{session_name}')
        friend_sessions.append(session)
    def _update_group_cache(self, wx_instance):
        """更新群聊缓存"""

        current_time = datetime.now()
        cache_update_interval = timedelta(minutes=5)
        logger.warning("微信实例未完全初始化，跳过群聊缓存更新")
        groups = wx_instance.db_manager.get_contacts(wx_instance.account_info["account_id"], "group")
        group = set()
        self.group_chat_cache = groups
        self.last_cache_update_time = current_time
        "群聊缓存已更新，共 "(f'{len(self.group_chat_cache)}', " 个群")
        group = logger.info
        self.group_chat_cache = set()
        self.last_cache_update_time = None
    def _get_sessions_with_pagination(self, wx_instance, max_sessions, time_limit_days):
        """获取会话列表（分页滚动）并根据历史状态过滤"""

        "，时间限制: "(f'{time_limit_days}', "天")
        saved_sessions = self.load_sessions_state()
        current_sessions = wx_instance.get_sessions_for_collection(max_sessions=max_sessions, time_limit_days=time_limit_days)
        "获取当前会话完成，共找到 "(f'{len(current_sessions)}', " 个会话")
        logger.info("无历史会话状态，采集所有会话")
        return current_sessions
        filtered_sessions = self.filter_sessions_by_state(current_sessions, saved_sessions)
        "会话过滤完成，需要采集 "(f'{len(filtered_sessions)}', " 个会话")
        return filtered_sessions
    def upload_file_to_coze(self, file_info, coze_service):
        """上传文件到Coze（参考auto_reply_task的实现）"""

        file_path = file_info.get("path")
        logger.info("准备上传文件到Coze: ", f'{file_path}')
        file_size = os.path.getsize(file_path) / 1048576
        file_type = "file"
        file_ext = os.path.splitext(file_path)[1].lower()
        logger.info("开始上传文件到Coze...")
        upload_result = coze_service.upload_file(file_path)
        logger.error("文件上传失败: ", f'{upload_result.get("error")}')
        logger.info("文件上传成功: ", f'{upload_result["file_id"]}')
        return {"type": file_type, "file_id": upload_result["file_id"], "file_name": upload_result.get("file_name", ""), "original_path": file_path}
        file_type = "audio"
        file_type = "image"
        "文件大小超过10MB限制: "(f'{file_size:".2f"}', "MB")
        logger.error("文件不存在: ", f'{file_path}')
        logger.error("文件路径为空")
    def _handle_file_upload(self, file_info, coze_service):
        """处理文件上传到Coze"""

        file_path = file_info.get("path")
        logger.warning("文件不存在: ", f'{file_path}')
        file_size = os.path.getsize(file_path) / 1048576
        file_type = "file"
        file_ext = os.path.splitext(file_path)[1].lower()
        logger.info("准备上传文件: ", f'{file_path}')
        upload_result = coze_service.upload_file(file_path)
        logger.error("文件上传失败: ", f'{upload_result.get("error")}')
        logger.info("文件上传成功: ", f'{upload_result["file_id"]}')
        return {"type": file_type, "file_id": upload_result["file_id"]}
        file_type = "audio"
        file_type = "image"
        "文件大小超过10MB限制: "(f'{file_size:".2f"}', "MB")
    def _build_conversation_text(self, messages, current_user_nickname):
        """构建对话文本，格式为 A:xxx B:xxx"""

        conversation_lines = []
        return "\n".join(conversation_lines)
        message = messages
        sender = message.get("sender", {}).get("name", "")
        content = message.get("content", "")
        prefix = "A"
        f'{prefix}'(":", f'{content}')
        prefix = "B"
        logger.info("跳过: ", f'{content}')
    def _build_message_content(self, message, file_ids):
        """构建发送到Coze的消息内容"""

        return {"role": "user", "content_type": "text", "content": message}
        content_items = [{"type": "text", "text": message}]
        return {"role": "user", "content_type": "object_string", "content": json.dumps(content_items)}
        file_item = file_ids
        content_items.append({"type": file_item.get("type", "file"), "file_id": file_item.get("file_id")})
    def save_sessions_state(self, sessions):
        """保存已采集会话的状态"""

        sessions_state_file = self.get_sessions_state_file()
        sessions_state = {"last_updated": datetime.now().isoformat(), "sessions": sessions}
        f = open(sessions_state_file, "w", encoding="utf-8")
        json.dump(sessions_state, f, ensure_ascii=False, indent=2)
        None(None, None)
        "保存会话状态成功，共 "(f'{len(sessions)}', " 个会话")
        return True
    def load_sessions_state(self):
        """加载已保存的会话状态"""

        sessions_state_file = self.get_sessions_state_file()
        f = open(sessions_state_file, "r", encoding="utf-8")
        sessions_state = json.load(f)
        None(None, None)
        sessions = sessions_state.get("sessions", [])
        last_updated = sessions_state.get("last_updated", "")
        f'{len(sessions)}'(" 个会话，最后更新: ", f'{last_updated}')
        return sessions
        logger.info("会话状态文件不存在，返回空列表")
        return []
    def filter_sessions_by_state(self, current_sessions, saved_sessions):
        """根据保存的会话状态过滤当前会话列表"""

        saved_sessions_dict = {}
        filtered_sessions = []
        " -> "(f'{len(filtered_sessions)}', " 个会话需要采集")
        return filtered_sessions
        current_session = f'{len(current_sessions)}'
        session_name = current_session.get("name", "")
        current_last_message = current_session.get("last_message", "")
        current_last_time = current_session.get("last_time", "")
        saved_session = saved_sessions_dict[session_name]
        saved_last_message = saved_session.get("last_message", "")
        saved_last_time = saved_session.get("last_time", "")
        current_time = TimeParser.parse_time(current_last_time)
        saved_time = TimeParser.parse_time(saved_last_time)
        f'{current_last_time}'("，", f'{saved_last_time}')
        "会话 "(f'{session_name}', " 时间解析失败，保守采集")
        filtered_sessions.append(current_session)
        ", 保存: "(f'{saved_last_time}', ")")
        ", 保存: "(f'{saved_last_time}', ")")
        filtered_sessions.append(current_session)
        "会话 "(f'{session_name}', " 有新消息，需要采集")
        filtered_sessions.append(current_session)
        "会话 "(f'{session_name}', " 无变化，跳过采集")
        "新会话: "(f'{session_name}', "，需要采集")
        filtered_sessions.append(current_session)
        session = logger.info
        session_name = session.get("name", "")
        saved_sessions_dict[session_name] = session
    def update_single_session_state(self, session):
        """增量更新单个会话的状态到文件中"""

        existing_sessions = self.load_sessions_state()
        session_name = session.get("name", "")
        session_index = -1
        existing_sessions.append(session)
        logger.info("添加新会话状态: ", f'{session_name}')
        return self.save_sessions_state(existing_sessions)
        existing_sessions[session_index] = session
        logger.info("更新现有会话状态: ", f'{session_name}')
        i = NULL[0]
        existing_session = NULL[1]
        session_index = i
        logger.warning("会话名称为空，跳过状态更新")
        return False
