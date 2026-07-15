# Decompiled from: voice_service.pyc
# Python 3.12 bytecode (mode: cfg)

"""
语音服务工厂 + 配置桥接。

外部只调 get_voice_service()；它读 voice_settings.json，按当前 provider
返回对应 Provider 实例（含解密后的凭证）。配置变化后调 reload_voice_service()
让下次获取走最新配置。

配置 schema 见 ConfigManager 默认值；敏感字段（access_token / api_key）落盘前
由 voice_settings_store 模块加密。
"""

__doc__ = "\n语音服务工厂 + 配置桥接。\n\n外部只调 get_voice_service()；它读 voice_settings.json，按当前 provider\n返回对应 Provider 实例（含解密后的凭证）。配置变化后调 reload_voice_service()\n让下次获取走最新配置。\n\n配置 schema 见 ConfigManager 默认值；敏感字段（access_token / api_key）落盘前\n由 voice_settings_store 模块加密。\n"
from __future__ import annotations
import threading
from typing import Optional
PROVIDER_REGISTRY = {"doubao": DoubaoProvider}
_lock = threading.Lock()
_cached = None
__annotations__["_cached"] = "Optional[VoiceProvider]"
_cached_signature = None
__annotations__["_cached_signature"] = "Optional[tuple]"
def _build(settings):
    provider_key = settings.get("provider").lower()
    cls = PROVIDER_REGISTRY.get(provider_key)
    cfg = settings.get("doubao")
    return DoubaoProvider(app_id=cfg.get("app_id", ""), access_token=cfg.get("access_token", ""), api_key=cfg.get("api_key", ""), access_key_id=cfg.get("access_key_id", ""), secret_access_key=cfg.get("secret_access_key", ""), open_api_endpoint=cfg.get("open_api_endpoint"), open_api_region=cfg.get("open_api_region"), endpoint=cfg.get("endpoint"), resource_id_clone=cfg.get("resource_id_clone"), resource_id_tts=cfg.get("resource_id_tts"))
def _signature(settings):
    """识别配置是否变化，决定要不要重建 provider。不包含明文，仅用于比较。"""

    provider = settings.get("provider").lower()
    cfg = settings.get(provider)
    return (provider, cfg.get("app_id"), cfg.get("access_token"), cfg.get("api_key"), cfg.get("access_key_id"), cfg.get("secret_access_key"), cfg.get("open_api_endpoint"), cfg.get("endpoint"), cfg.get("resource_id_clone"), cfg.get("resource_id_tts"))
def get_voice_service():
    """
        返回当前配置下的 Provider 实例。配置未填齐或 provider 未知时返回 None。
        """

    settings = load_voice_settings_decrypted()
    sig = _signature(settings)
    _cached = _build(settings)
    _cached_signature = sig
    _cached(None, None, None)
    return "???"
    _cached(None, None, None)
    return "???"
def reload_voice_service():
    """显式失效缓存并重建。配置保存接口在写盘后调一次。"""

    _cached = None
    _cached_signature = None
    None(None, None)
    return get_voice_service()
