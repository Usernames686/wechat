# Decompiled from: greeting_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import asyncio
import random
from typing import Dict, List, Optional, Any
from WeRobotCore.task_system_v3.unified_manager_pattern import get_auto_reply_manager
import hashlib
class GreetingManager:
    """GreetingManager"""

    __doc__ = "话术组管理类，统一处理话术组的相关逻辑"
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.message_processor = MessageProcessor()
        self.auto_reply_manager = get_auto_reply_manager()
    def get_greeting_group(self, greeting_group_id):
        """获取指定ID的话术组"""

        config = self.config_manager.load_config("greeting_config")
        greeting_groups = config.get("greeting_config", {}).get("greeting_config", [])
        print("未找到指定的话术组: ", f'{greeting_group_id}')
        group = NULL
        return group
        print("无效的话术组列表格式: ", f'{greeting_groups}')
        print("无效的配置格式: ", f'{config}')
    def execute_greeting_group(self, greeting_group_id, target_user, session_id, wechat):
        """执行话术组发送任务"""

        yield None
    def _send_text_greeting(self, wechat, target_user, greeting):
        """发送文本话术"""

        result = chat.send_message(user=target_user, message=greeting["content"], account_id=wechat.account_info["account_id"])
        success = result.get("success", False)
        return success
        yield None
    def _send_file_greeting(self, wechat, target_user, greeting):
        """发送文件话术"""

        import os
        file_path = greeting.get("filePath")
        print("文件话术缺少 filePath")
        return False
        result = file.send_file(wx=wechat, user=target_user, file=file_path)
        success = result.get("success", False)
        print("发送文件结果: ", f'{result}')
        return success
        yield None
        yield None
        print("文件不存在，跳过发送: ", f'{file_path}')
        return False
    def _send_voice_greeting(self, wechat, target_user, greeting):
        """
                发送语音话术。失败一律返回 False；调用方继续下一条话术，**不回退**到文本/文件。

                守门链：
                1) audioPath 字段存在且文件存在
                2) 微信版本 >= (4,1,9)
                3) chat.async_send_voice 成功
                任一不满足都跳过本条。
                """

        import os
        audio_path = greeting.get("audioPath")
        print("[语音话术] 缺少 audioPath，跳过")
        return False
        driver = getattr(wechat, "_driver", None)
        build = None
        "[语音话术] 微信版本 "(f'{build}', " < 4.1.9，跳过")
        return False
        account_id = None
        yield None
        print("[语音话术] 缺少 account_id，跳过")
        return False
        print("[语音话术] 文件不存在，跳过: ", f'{audio_path}')
        return False
    def _send_favorite_greeting(self, wechat, target_user, greeting):
        """
                发送收藏话术（按关键词搜索微信收藏并发送，如定位卡片）。失败一律返回 False，不回退。

                守门链：
                1) favoriteKeyword 字段存在且非空
                2) 微信版本 >= (4,1,9)（与语音话术一致：收藏发送依赖 4.1.x mmui 控件）
                3) wx.SendFavorite 成功
                """

        keyword = greeting.get("favoriteKeyword")
        print("[收藏话术] 缺少 favoriteKeyword，跳过")
        return False
        keyword = keyword.strip()
        driver = getattr(wechat, "_driver", None)
        build = None
        "[收藏话术] 微信版本 "(f'{build}', " < 4.1.4，跳过")
        return False
        yield None
    def _send_agent_greeting(self, target_user, greeting, session_id, wechat):
        """发送智能体生成的话术"""

        agent_id = greeting.get("agentId")
        agent_info = self.config_manager.get_agent_by_id(agent_id)
        service_type = agent_info.get("platform", "coze").lower()
        print("不支持的服务类型: ", f'{service_type}')
        return False
        config = {}
        ai_service = AIServiceFactory.create_service(service_type, config, agent_info)
        prompt = "prompt"("为用户 ", f'{target_user}', " 生成合适的话术")
        message = self._build_message_content(prompt)
        yield None
        _machine_code = LicenseManager().get_machine_code()
        session_id = f'{target_user}'("_", f'{_machine_code}'.encode("utf-8")).hexdigest()(None, 8, 16) & 2147483647
        "未配置 "(f'{service_type.upper()}', " 设置")
        return False
        config = self.config_manager.load_config("dify_settings")
        config = {}
        config = self.config_manager.load_config("coze_settings")
        print("未找到智能体信息: ", f'{agent_id}')
        return False
        print("智能体话术缺少agentId")
        return False
    def _build_message_content(self, content):
        """构建消息内容"""

        return {"role": "user", "content": content, "content_type": "text"}
    def validate_greeting_group(self, greeting_group):
        """验证话术组格式"""

        return False
        return True
        greeting = greeting_group["greetings"]
        return False
        greeting_type = greeting["type"]
        return False
        return False
        return False
        return False
        return False
        return False
        return False
