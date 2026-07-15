# Decompiled from: auto_reply_task.pyc
# Python 3.12 bytecode (mode: cfg)

from email import message
import os
import re
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import qrcode
import json
class AutoReplyTask(BaseTask):
    """AutoReplyTask"""

    _image_path_cache = {}
    __annotations__["_image_path_cache"] = Dict[(str, str)]
    _IMAGE_CACHE_MAX = 200
    def __init__(self, task_id, params, account_id, schedule_time):
        super().__init__(task_id=task_id, task_type=TaskType.AUTO_REPLY, params=params, schedule_time=schedule_time, priority=TaskPriority.HIGH)
        self.account_id = account_id
        self.wechat = WeChat()
        print("🔧 [任务执行] 使用默认实例（未指定账号）- 任务: ", f'{self.id}')
        self.message_processor = MessageProcessor()
        self.config_manager = ConfigManager(account_id)
        self.task_logger = TaskLogger()
        self.logger = UiaLogger(logger_name="AutoReplyTask").get_logger()
        self.message_num = params.get("message_num", 1)
        self.file_info = None
        self.pending_messages = []
        self.max_concurrent_requests = 5
        self._coze_semaphore = asyncio.Semaphore(1)
        self.license_manager = LicenseManager()
        self.require_confirmation = params.get("require_confirmation", False)
        self.confirmation_timeout = params.get("confirmation_timeout", 30)
        self.auto_send_on_timeout = params.get("auto_send_on_timeout", True)
        self.confirmation_event = asyncio.Event()
        self.confirmed_content = None
        self.confirmation_action = None
        self.wechat = WeChat(account_id=account_id)
        f'{self.account_id}'(", 任务: ", f'{self.id}')
    def process_messages(self, messages, agent_config):
        """处理消息列表，返回需要发送到Coze的消息"""

        processed_messages = []
        is_group = self.params.get("is_group", False)
        user_name = self.params.get("user_name")
        rect_sender_cache = {}
        return self.max_concurrent_requests
        msg = None
        content = msg.get("content", "")
        sender = msg.get("sender", {}).get("name", "")
        self.logger.info("过滤系统消息和自己的消息: ", f'{content}')
        self.logger.info("好友通过标志消息，交由事件处理，跳过回复: ", f'{content}')
        processed_messages.append({"content": content, "sender": sender, "is_greeting": False, "fingerprint": msg.get("fingerprint", ""), "id": msg.get("id")})
        file_info = msg.get("file_info")
        processed_messages.append({"content": content, "file_info": file_info, "sender": sender, "is_greeting": False, "fingerprint": msg.get("fingerprint", ""), "id": msg.get("id")})
        print("检测到图片消息: ", f'{self.config_manager.is_image_recognition_enabled()}')
        fingerprint = msg.get("fingerprint", "")
        image_path = None
        processed_messages.append({"content": content, "image_path": image_path, "sender": sender, "is_greeting": False, "fingerprint": fingerprint, "id": msg.get("id")})
        image_path = self.wechat.get_image_by_id(msg.get("id"))
        AutoReplyTask._cache_image_path(fingerprint, image_path)
        voice_text = msg.get("voice_text", "")
        content = content.replace(",未播放", "")
        content = voice_text
        self.logger.info("消息不满足策略条件: ", f'{content}')
        msg_rect = msg.get("rect_info")
        rect_key = None
        resolved_sender = self.wechat.get_group_msg_sender(msg.get("id"))
        sender = resolved_sender
        colleague_names_str = self.config_manager.get_colleague_names_to_ignore()
        colleague_list = colleague_names_str.split("//")
        name = []
        "忽略来自群聊的同事 '"(f'{sender}', "' 消息")
        name = self.logger.info
        rect_sender_cache[rect_key] = resolved_sender
        resolved_sender = rect_sender_cache[rect_key]
    def _build_file_info_from_content(self, content):
        """从 "[文件] 文件名.ext" 预览文本中兜底提取文件信息。"""

        file_name = None.strip()
        ext_match = re.search("\\.([a-z0-9]+)$", file_name, re.IGNORECASE)
        return {"name": file_name, "size": None, "type": None}
        return {"name": content, "size": len("[文件]"), "type": ext_match.group(1).lower()}
    @classmethod
    def _cache_image_path(cls, fingerprint, path):
        cls._image_path_cache[fingerprint] = path
        remove_keys = cls._IMAGE_CACHE_MAX // 2
        k = remove_keys
        del cls._image_path_cache[k]
    def _should_process_file(self, file_info):
        """检查文件是否需要处理"""

        strategy = self.config_manager.get_file_recognition_config()
        file_enable = strategy.get("enabled", False)
        file_type_mapping = {"pdf": ["doc", "docx"], "word": ["xls", "xlsx"], "excel": [], "text": ("txt", "md", "csv", "json", "xml")}
        file_type = file_info.get("type")
        self.logger.info("无效的文件类型: ", f'{file_type}')
        return False
        allowed_types = strategy.get("fileTypes", [])
        return any((config_type for config_type in _iter)(allowed_types))
        return True
        return False
        return False
    def process_coze_requests(self, messages, session_name, session_id, is_group, agent_config):
        """并发处理Coze/Dify请求，支持消息合并"""

        account_id = None
        agent_result = agent_config
        agent_id = agent_result
        user_exists_in_db = True
        ai_chat_service = self._get_ai_service(agent_id)
        chat_history_settings = self.config_manager.load_config("chat_history_settings").get("chat_history_settings", {})
        message_merge_config = chat_history_settings.get("messageMerge", {})
        merge_mode = message_merge_config.get("mode", "none")
        friend_tags = ""
        yield None
        yield None
        friend_tags = self._get_friend_tags(session_name)
        from WeRobotCore.api.friend import read_and_save_friend_info
        result = read_and_save_friend_info(session_name, account_id)
        f'{session_name}'(" 好友信息失败: ", f'{result.get("message", "未知错误")}')
        "已为新用户 "(f'{session_name}', " 读取并保存好友信息")
        return [{"success": False, "error": "消息列表为空"}]
        self.logger.info("未找到有效的 agentId")
        return [{"success": False, "error": "未找到有效的 agentId"}]
        agent_id = agent_result.get("agent_id")
        user_exists_in_db = agent_result.get("user_exists_in_db", True)
        agent_config = self.config_manager.get_agent_id_by_tags(account_id, session_name, is_group)
    def _process_individual_messages(self, agent_id, messages, session_name, session_id, is_group, ai_chat_service, friend_tags):
        """处理单独的消息（原有逻辑）"""

        def process_single_message(message):
            yield None
        "开始处理并回复 "(f'{len(messages)}', " 个消息...")
        tasks = messages
        msg = []
        yield None
        msg = _
    def _process_merged_messages(self, agent_id, messages, session_name, session_id, ai_chat_service, friend_tags):
        """处理合并的消息"""

        yield None
    def _should_extract_friend_tags(self):
        """检查是否需要提取好友标签"""

        config_manager = ConfigManager()
        api_config = config_manager.load_config("external_api_settings")
        return False
        customer_id = api_config["identifier"]
        customer_config_manager = CustomerAPIConfig()
        customer_config = customer_config_manager.get_customer_config(customer_id)
        return False
        custom_features = customer_config.get("custom_features", {})
        auto_reply_config = custom_features.get("auto_reply", {})
        return auto_reply_config.get("extract_friend_tags", False)
    def _get_friend_tags(self, session_name):
        """获取好友标签并拼接成字符串"""

        account_id = None
        db_manager = WeChatDBManager()
        user_tags_result = db_manager.get_contact_tags(account_id, session_name)
        return ""
        tag_str = ""
        return tag_str
        tag_str = user_tags_result[0][1]
        return tag_str
        return ""
    def increment_message_num(self):
        """增加消息计数"""

        self.message_num += 1
        self.params["message_num"] = self.message_num
    def _handle_file_upload(self, file_info, ai_service, user_id):
        """处理文件上传到Coze"""

        file_path = file_info.get("path")
        self.logger.info("文件的绝对路径：", f'{file_path}')
        file_size = os.path.getsize(file_path) / 1048576
        file_type = "file"
        file_ext = os.path.splitext(file_path)[1].lower()
        self.logger.info("准备上传文件....")
        import asyncio
        upload_result = ai_service.upload_file(file_path, user_id)
        print("文件上传失败: ", f'{upload_result.get("error")}')
        self.logger.info("文件上传成功: ", f'{upload_result["file_id"]}')
        return {"type": file_type, "file_id": upload_result["file_id"]}
        yield None
        file_type = "audio"
        file_type = "image"
        "文件大小超过10MB限制: "(f'{file_size:".2f"}', "MB")
        base_name = os.path.splitext(file_info["name"])[0]
        ext = os.path.splitext(file_info["name"])[1]
        pattern = re.compile(re.escape(base_name) + "\\(\\d+\\)" + re.escape(ext) + "$", re.IGNORECASE)
        matched_files = []
        self.logger.warning("文件不存在: ", f'{file_path}')
        matched_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        file_path = matched_files[0]
        self.logger.info("因微信文件同名自动加后缀，匹配到真实文件: ", f'{file_path}')
        f = os.listdir(file_dir)
        matched_files.append(os.path.join(file_dir, f))
        base_path = self.config_manager.get_file_recognition_config().get("filePath")
        current_month = datetime.now().strftime("%Y-%m")
        version = detect_version()
        file_dir = os.path.join(base_path, "FileStorage", "File", current_month)
        file_path = os.path.join(file_dir, file_info["name"])
        file_dir = os.path.join(base_path, "msg", "file", current_month)
        self.logger.info("未配置文件路径")
    def _build_message_content(self, message, file_ids):
        """构建发送到Coze的消息内容"""

        return {"role": "user", "content_type": "text", "content": message}
        return {"role": "object_string", "content_type": NULL, "content": json.dumps([{"type": "text", "text": message}], file_ids)}
    def _build_context_messages(self, session_id, session_name, fingerprint, sender_name, actual_message, file_ids, is_group):
        """构建上下文消息列表"""

        all_messages = self.params.get("all_messages")
        context_messages = []
        context_messages.append(self._build_message_content(actual_message, file_ids))
        return context_messages
        from WeRobotCore.utils.chat_history import ChatHistoryManager
        chat_history_manager = ChatHistoryManager(self.account_id)
        context_count = self.config_manager.get_context_count()
        yield None
    def _get_coze_service(self):
        """获取 Coze 服务实例"""

        config = self.config_manager.get_cached_config("coze_settings")
        raise ValueError("未配置 Coze Token")
        return CozeService(config["coze_settings"]["token"])
    def _get_ai_service(self, agent_id):
        """获取智能体服务实例"""

        config_manager = ConfigManager()
        agent_info = config_manager.get_agent_by_id(agent_id)
        service_type = agent_info.get("platform", "coze").lower()
        raise ValueError("不支持的智能体平台: ", f'{service_type}')
        config = {}
        return AIServiceFactory.create_service(service_type, config, agent_info)
        config = self.config_manager.get_cached_config("dify_settings")
        raise ValueError("未配置 Dify 设置")
        config = {}
        config = self.config_manager.get_cached_config("coze_settings")
        raise ValueError("未配置 Coze 设置")
        raise ValueError("未找到智能体信息: ", f'{agent_id}')
    def execute(self):
        session_id = self.params.get("session_id")
        messages = self.params.get("messages", [])
        user_name = self.params.get("user_name")
        session_name = self.params.get("session_name")
        is_group = self.params.get("is_group", False)
        account_id = None
        yield None
    def _update_last_reply_cache(self, session_id, content):
        """更新最后回复消息缓存"""

        scheduler = self._get_scheduler()
        scheduler.update_message_mapping(session_id=session_id, reply_message=content, account_id=self.account_id)
        scheduler.update_last_reply_cache(session_id=session_id, content=content, account_id=self.account_id)
    def _get_scheduler(self):
        """获取调度器实例（适配V3缓存系统）"""

        return get_v3_adapter_instance()
    def _check_reply_strategy(self, message, is_group, user_name, strategy):
        """检查是否满足回复策略"""

        chat_type = strategy.get("chatType", "all")
        keywords = strategy.get("keywords", [])
        return True
        return False
        return False
        return False
    def _check_need_transfer(self, reply):
        """检查是否需要转人工

                Args:
                    reply: 回复内容

                Returns:
                    tuple: (need_transfer, notify_wechat) 是否需要转人工和通知的微信号
                """

        chat_history_settings = self.config_manager.get_cached_config("chat_history_settings")
        transfer_config = chat_history_settings.get("chat_history_settings", {}).get("transferConfig", {})
        transfer_phrases = transfer_config.get("phrases", [])
        notify_wechat = transfer_config.get("notifyWechat", "")
        need_transfer = False
        return (need_transfer, notify_wechat)
        auto_reply_manager = get_auto_reply_manager()
        return (need_transfer, notify_wechat)
        session_name = self.params.get("session_name")
        account_id = getattr(self, "account_id", None)
        auto_reply_manager.suspend_session(account_id, session_name)
        "会话 "(f'{session_name}', " 已因转人工被挂起")
        phrase = self.logger.info
        need_transfer = True
    def _handle_transfer_to_human(self, session_name, user_qustion, reply, notify_wechat):
        """处理转人工通知

                Args:
                    session_name: 会话名称
                    user_qustion: 用户问题
                    reply: 回复内容
                    notify_wechat: 通知的微信号
                """

        notifier = FeishuNotifier()
        question_content = str(user_qustion.get("content", ""))
        short_question = 20
        transfer_message = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        loop = asyncio.get_event_loop()
        yield None
        self.logger.warning("未配置飞书，跳过飞书转人工通知")
        self.logger.info("准备发送转人工通知给微信好友: ", f'{notify_wechat}')
        question_content = str(user_qustion.get("content", ""))
        notify_message = f'{question_content}'
        yield None
    def _wait_for_confirmation(self, ai_reply, user_question, session_name):
        """等待前端确认回复内容"""

        self.status = TaskStatus.PENDING_CONFIRMATION
        yield None
    def confirm_reply(self, action, final_content):
        """确认回复（由API调用）"""

        print("确认回复")
        self.confirmation_action = action
        self.confirmed_content = final_content
        self.confirmation_event.set()
    def _resolve_local_file(self, key):
        """根据文件库key查找本地文件路径，找不到返回None"""

        return FileLibraryManager().resolve_key(key)
    def _handle_missing_local_file(self, key, session_name):
        """文件库文件缺失时，通过WebSocket通知前端引导用户补充"""

        f'{key}'("'，会话=", f'{session_name}')
        yield None
    def _handle_missing_rhetoric_group(self, group_name, session_name):
        """话术组缺失或发送失败时，通过WebSocket通知前端引导用户检查配置"""

        f'{group_name}'("'，会话=", f'{session_name}')
        yield None
    __classcell__ = __class__
    return __class__
