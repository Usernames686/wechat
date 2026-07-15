# Decompiled from: auto_follow_task.pyc
# Python 3.12 bytecode (mode: cfg)

"""
自动跟单任务 - Task System V2

实现对指定好友的自动跟进功能，通过Coze智能体生成个性化话术并发送消息。
"""

__doc__ = "\n自动跟单任务 - Task System V2\n\n实现对指定好友的自动跟进功能，通过Coze智能体生成个性化话术并发送消息。\n"
from datetime import datetime, timezone, timedelta
import asyncio
import random
import hashlib
from typing import Dict, Any, Optional
from WeRobotCore.task_system_v3.unified_manager_pattern import get_auto_reply_manager
MAX_FLAT_HISTORY_MESSAGES = 40
MAX_FLAT_HISTORY_CHARS = 12000
class AutoFollowTask(TimedBaseTask):
    """AutoFollowTask"""

    __doc__ = "自动跟单任务\n    \n    负责对指定好友发送智能体生成的跟进话术，\n    支持个性化消息生成和多种消息类型发送。\n    "
    def __init__(self, task_id, params, schedule_time, schedule_config, is_recurring):
        """初始化自动跟单任务

                Args:
                    task_id: 任务ID
                    params: 任务参数，包含：
                        - friend_wxid: 好友微信ID
                        - friend_name: 好友昵称
                        - account_id: 微信账号ID
                        - agent_id: Coze智能体ID
                        - follow_scenario: 跟单场景（如：新好友）
                    schedule_time: 调度时间
                    schedule_config: 调度配置
                    is_recurring: 是否为循环任务
                """

        required_params = ("friend_wxid", "friend_name", "account_id", "agent_id")
        super().__init__(task_id=task_id, task_type=TaskType.AUTO_FOLLOW, params=params, schedule_time=schedule_time, priority=TaskPriority.MEDIUM, schedule_config=schedule_config, is_recurring=is_recurring)
        self.task_logger = TaskLogger()
        self.config_manager = ConfigManager()
        self.message_processor = MessageProcessor()
        self.id = task_id
        self.error = None
        self.friend_wxid = params["friend_wxid"]
        self.friend_name = params["friend_name"]
        self.account_id = params["account_id"]
        self.agent_id = params["agent_id"]
        self.wechat = WeChat(self.account_id)
        self.follow_scenario = params.get("follow_scenario", "新好友")
        self.chat_type = params.get("chat_type", "single")
        self.metadata = params.get("metadata", {})
        self.follow_day = self._calculate_follow_day()
        "，第"(f'{self.follow_day}', "天跟进")
        param = f'{self.account_id}'
        raise ValueError("缺少必需参数: ", f'{param}')
    def execute(self):
        """执行跟单任务"""

        yield None
    def _send_follow_message(self, chat_messages):
        """发送跟进消息"""

        agent_info = self.config_manager.get_agent_by_id(self.agent_id)
        service_type = agent_info.get("platform", "coze").lower()
        print("不支持的智能体平台: ", f'{service_type}')
        return False
        config = {}
        ai_service = AIServiceFactory.create_service(service_type, config, agent_info)
        f'{service_type}'(", 智能体ID: ", f'{self.agent_id}')
        prompt = self._build_follow_prompt()
        flatten = service_type == "fireflow"
        context_messages = self._build_context_messages(chat_messages, prompt, flatten=flatten)
        "构建消息内容(携带上下文数: "(f'{len(context_messages)}', ")")
        session_id = self._generate_session_id()
        encrypted_account_id = None
        yield None
        config = self.config_manager.get_cached_config("dify_settings")
        print("未配置 Dify 设置")
        return False
        config = {}
        config = self.config_manager.get_cached_config("coze_settings")
        print("未配置 Coze 设置")
        return False
        print("未找到智能体信息: ", f'{self.agent_id}')
        return False
    def _calculate_follow_day(self):
        """计算当前跟进天数

                根据执行统计信息计算当前是第几天跟进：
                1. 优先使用执行次数(execution_count)来确定已跟进的天数，当前跟进天数 = 执行次数 + 1
                2. 如果无法获取执行次数，则使用next_execution_day作为备选
                3. 如果metadata为空或无法计算，则默认为第1天跟进
                """

        follow_day = 1
        execution_stats = self.metadata.get("execution_stats", {})
        execution_count = execution_stats.get("execution_count", 0)
        next_execution_day = execution_stats.get("next_execution_day", 1)
        return follow_day
        follow_day = next_execution_day
        print("使用next_execution_day计算当前跟进天数: ", f'{follow_day}')
        follow_day = execution_count + 1
        f'{execution_count}'(")计算当前跟进天数: ", f'{follow_day}')
        return follow_day
        print("执行统计信息为空，使用默认跟进天数: 1")
        return follow_day
        print("元数据为空，使用默认跟进天数: 1")
        return follow_day
    def _build_follow_prompt(self):
        """构建跟进提示词

                根据跟单场景和跟进天数生成不同的提示词，如果无法确定跟进天数，则使用兜底提示词
                """

        has_valid_follow_day = self.follow_day > 0
        base_prompt = "的跟单话术"
        print("无法确定跟进天数，使用兜底提示词")
        return base_prompt
        base_prompt = "天的跟单话术"
        return base_prompt
        base_prompt = "的运营话术"
        print("无法确定跟进天数，使用兜底提示词")
        return base_prompt
        base_prompt = "天的运营话术"
        return base_prompt
    def _build_message_content(self, content):
        """构建消息内容"""

        return {"role": "user", "content": content, "content_type": "text"}
    def _build_flat_context(self, chat_messages, prompt):
        """拍平上下文：把整段历史按时间顺序拼成一段纯文本，连同任务作为单条 user 消息发出。

                某些平台/模型对"历史字段(history)"是略读的——当结尾是我方消息、且历史里对方消息很短时，
                模型容易漏看对方发言而误判（典型：把已经回复/提过问的候选人当成失联，误发再触达话术）。
                把完整对话拍平进单条 query 可强制模型通读，经实测能消除这类漏读。是否启用由 agent 配置
                启用条件见 _send_follow_message（fireflow 平台）。我方(本账号)消息标[我方]，非我方标[对方]。
                顺序与 _build_context_messages 一致（保序：输入即时间正序 旧→新）。
                为防止模型输入 token 超限，按 MAX_FLAT_HISTORY_MESSAGES / MAX_FLAT_HISTORY_CHARS 截断，
                优先保留最近的消息（从新到旧累计，超限即停），并在开头标注省略。"""

        all_lines = []
        kept = []
        used_chars = 0
        kept.reverse()
        truncated = len(kept) < len(all_lines)
        convo = "（暂无任何聊天记录）"
        text = f'{prompt}'
        return [self._build_message_content(text)]
        convo = "\n".join(kept)
        convo = "（更早的聊天记录已省略）\n" + convo
        line = "\n\n【任务】"
        kept.append(line)
        used_chars = used_chars + len(line) + 1
        hist_msg = reversed(all_lines)
        hist_sender_name = hist_msg.get("sender", {}).get("name")
        hist_content = hist_msg.get("content", "")
        is_self = hist_msg.get("isSelf", False)
        f'{"[对方]"}'(" ", f'{hist_content}')
        hist_content = "）"
    def _build_context_messages(self, chat_messages, prompt, flatten):
        """构建完整的上下文消息

                设计说明：跟进进度的判定（如"对方是否已提交所需材料/资料"）完全交给跟单智能体
                从对话上下文中按【内容】去分析，代码不再注入"除本账号外是否有他人发过消息"这类
                基于 isSelf 的权威布尔事实。原因：真实群里除机器人外还可能有人工顾问/其他助理用各自
                账号发言，仅凭 isSelf 无法把"队友"和"候选人/客户"区分开；一刀切地把"有非我消息"当成
                "对方已回复/已推进"会造成误判（典型：顾问用私人手机发的空白资料模板被当成候选人已交
                资料，从而误判 SKIP）。正确做法是把完整对话原样交给智能体，由提示词规则按内容判断
                "上下文里是否出现了候选人实际填写的个人资料"（详见 Coze 提示词，不区分发送方）。

                flatten=True 时改用拍平格式（见 _build_flat_context），用于规避 fireflow 模型对历史短消息
                的弱注意力（由调用方按 platform==fireflow 决定）。"""

        context_messages = []
        context_messages.append(self._build_message_content(prompt))
        return context_messages
        hist_msg = reversed(chat_messages)
        hist_sender_name = hist_msg.get("sender", {}).get("name")
        hist_content = hist_msg.get("content", "")
        is_self = hist_msg.get("isSelf", False)
        context_messages.insert(0, {"role": "user", "content": hist_content, "content_type": "text"})
        context_messages.insert(0, {"role": "assistant", "content": hist_content, "type": "answer", "content_type": "text"})
        hist_content = "）"
        return self._build_flat_context(chat_messages, prompt)
    def _load_local_history_context(self, account_id, max_count):
        """读取本地保存的历史会话作为上下文（更长上下文）。

                - 单聊、群聊均启用：群跟单场景下目标常是"对方所在的准一对一群"，
                  同样需要跨多屏的历史来判断"是否已回复/已发资料"；群内多人噪声由跟单智能体提示词做语义去噪。
                  本地历史由自动回复 / 仅监控记录员落库，群会话也会被记录。
                - 返回结构与顺序与 UIA 一屏读取保持一致：嵌套 sender.name、按时间正序（旧→新），
                  可直接交给 _build_context_messages，无需再调整顺序（该方法对输入顺序是保序的）。
                - 读不到（会话改名/从未记录）返回空列表，由调用方回退到一屏读取。
                """

        from WeRobotCore.utils.chat_history import ChatHistoryManager
        chat_history = ChatHistoryManager(account_id)
        yield None
        return []
    def _generate_session_id(self):
        """生成会话ID"""

        _machine_code = LicenseManager().get_machine_code()
        session_str = f'{_machine_code}'
        session_id = hashlib.md5(session_str.encode("utf-8")).hexdigest()(None, 8, 16) & 2147483647
        return session_id
    def _send_parsed_message(self, reply):
        """解析并发送消息"""

        parsed_reply = self.message_processor.parse_message(reply)
        success = True
        return success
        component = parsed_reply.components
        yield None
        file_key = component.content
        local_path = self._resolve_local_file(file_key)
        yield None
        result = file.send_file(wx=self.wechat, user=self.friend_name, file=local_path)
        auto_reply_manager = get_auto_reply_manager()
        yield None
        f'{file_key}'(", error=", f'{result.get("error", "未知错误")}')
        success = False
        result = file.send_file(wx=self.wechat, user=self.friend_name, file=component.content)
        auto_reply_manager = get_auto_reply_manager()
        print("V3 自动回复管理器未初始化，跳过缓存")
        yield None
        print("发送文件失败: ", f'{result.get("error", "未知错误")}')
        success = False
        result = file.send_file(wx=self.wechat, user=self.friend_name, file=component.content)
        auto_reply_manager = get_auto_reply_manager()
        print("V3 自动回复管理器未初始化，跳过缓存")
        yield None
        print("发送图片失败: ", f'{result.get("error", "未知错误")}')
        success = False
        raw_message = component.content
        raw_message = component.content.encode("raw_unicode_escape").decode("unicode_escape")
        messages = split_text_message(raw_message, self.config_manager.get_auto_split_mode())
        msg = messages
        result = chat.send_message(user=self.friend_name, message=msg, account_id=self.account_id)
        auto_reply_manager = get_auto_reply_manager()
        yield None
        yield None
        print("发送消息失败: ", f'{result.get("error", "未知错误")}')
        success = False
    def _broadcast_task_status(self):
        """广播任务状态"""

        status_data = {"type": "auto_follow_status", "task_id": self.id, "friend_wxid": self.friend_wxid, "friend_name": self.friend_name, "status": self.status.value, "timestamp": datetime.now().isoformat()}
        yield None
    def _save_execution_log(self, success, error):
        """保存执行日志"""

        log_data = {"task_id": self.id, "friend_wxid": self.friend_wxid, "friend_name": self.friend_name, "account_id": self.account_id, "agent_id": self.agent_id, "follow_scenario": self.follow_scenario, "execution_time": datetime.now().isoformat(), "success": success, "generated_message": getattr(self, "generated_message", ""), "error": error}
        self.task_logger.log_auto_follow_execution(log_data)
    def _resolve_local_file(self, key):
        """根据文件库key查找本地文件路径，找不到返回None"""

        return FileLibraryManager().resolve_key(key)
    def _handle_missing_local_file(self, key):
        """文件库文件缺失时，通过WebSocket通知前端引导用户补充"""

        f'{key}'("'，会话=", f'{self.friend_name}')
        yield None
    __classcell__ = __class__
    return __class__
