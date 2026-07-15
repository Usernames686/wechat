# Decompiled from: __init__.pyc
# Python 3.12 bytecode (mode: cfg)

"""
语音服务模块：声音复刻 + TTS 合成。

入口：voice_service.get_voice_service() 返回当前配置 provider 的实例。
扩展：新增 provider 实现 VoiceProvider 接口并在 voice_service.PROVIDER_REGISTRY 注册。
"""

__doc__ = "\n语音服务模块：声音复刻 + TTS 合成。\n\n入口：voice_service.get_voice_service() 返回当前配置 provider 的实例。\n扩展：新增 provider 实现 VoiceProvider 接口并在 voice_service.PROVIDER_REGISTRY 注册。\n"
__all__ = ("get_voice_service", "reload_voice_service", "VoiceProvider", "VoiceInfo", "CloneJob", "CloneStatus", "SynthResult", "HealthCheckResult", "voice_library", "voice_greetings_store", "preview_store")
