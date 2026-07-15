# Decompiled from: provider_base.pyc
# Python 3.12 bytecode (mode: cfg)

"""
语音服务 Provider 抽象层。

约定：每个 provider（豆包 / 未来 YokoAgent 等）实现 VoiceProvider 接口。
上层调用 voice_service 不感知具体 provider，便于切换/扩展。
"""

__doc__ = "\n语音服务 Provider 抽象层。\n\n约定：每个 provider（豆包 / 未来 YokoAgent 等）实现 VoiceProvider 接口。\n上层调用 voice_service 不感知具体 provider，便于切换/扩展。\n"
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
class HealthCheckResult:
    """HealthCheckResult"""

    __annotations__["ok"] = bool
    details = field(default_factory=dict)
    __annotations__["details"] = dict
    error = None
    __annotations__["error"] = Optional[str]
class VoiceInfo:
    """VoiceInfo"""

    __annotations__["voice_id"] = str
    __annotations__["name"] = str
    __annotations__["source"] = str
    language = "zh"
    __annotations__["language"] = str
    gender = "neutral"
    __annotations__["gender"] = str
    extra = field(default_factory=dict)
    __annotations__["extra"] = dict
class CloneJob:
    """CloneJob"""

    __doc__ = "提交复刻样本后的返回值。"
    __annotations__["voice_id"] = str
    __annotations__["status"] = str
    message = ""
    __annotations__["message"] = str
class CloneStatus:
    """CloneStatus"""

    __annotations__["voice_id"] = str
    __annotations__["status"] = str
    demo_audio_url = None
    __annotations__["demo_audio_url"] = Optional[str]
    message = ""
    __annotations__["message"] = str
class SynthResult:
    """SynthResult"""

    __annotations__["success"] = bool
    audio_path = None
    __annotations__["audio_path"] = Optional[str]
    duration_sec = 0.0
    __annotations__["duration_sec"] = float
    voice_id = None
    __annotations__["voice_id"] = Optional[str]
    format = "mp3"
    __annotations__["format"] = str
    error_code = None
    __annotations__["error_code"] = Optional[str]
    error_message = None
    __annotations__["error_message"] = Optional[str]
class VoiceProvider(ABC):
    """VoiceProvider"""

    __doc__ = "语音 Provider 抽象基类。"
    provider_id = ""
    __annotations__["provider_id"] = str
    @abstractmethod
    def health_check(self):
        """检查凭证是否有效。前端"测试连接"按钮调用。"""
    list_voices = abstractmethod((lambda self: ...))
    @CloneJob
    def clone_voice(self, sample_path, voice_id, language, text):
        """
                提交复刻样本启动训练。

                sample_path: 本地音频文件路径（wav/mp3/m4a 等，5-15s 最佳）
                voice_id:    控制台预占的 speaker_id（豆包形如 S_xxx）
                language:    'zh' | 'en' | 'ja'
                text:        样本对应的文本，用于 WER 校验（可选）
                """
    @abstractmethod
    def query_clone_status(self, voice_id):
        """查询复刻训练状态。"""
    @str
    def synthesize(self, text, voice_id, out_path, speed):
        """文本 → 音频文件，写入 out_path。"""
