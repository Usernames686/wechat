# Decompiled from: dpapi_crypto.pyc
# Python 3.12 bytecode (mode: cfg)

"""
基于 Windows DPAPI 的轻量字符串加解密。

用途：把 voice_settings 等配置里的敏感字段（access_token、api_key）
在落盘前加密，避免明文存储。同一台机器的同一用户解得开，换机器/换用户解不开。

读到加密失败的字段（升级前的明文 / 损坏密文）时返回原值，
保证配置不会因为加解密问题完全打不开。

非 Windows 平台或 pywin32/win32crypt 不可用时退化为原文（透明 no-op）。
"""

__doc__ = "\n基于 Windows DPAPI 的轻量字符串加解密。\n\n用途：把 voice_settings 等配置里的敏感字段（access_token、api_key）\n在落盘前加密，避免明文存储。同一台机器的同一用户解得开，换机器/换用户解不开。\n\n读到加密失败的字段（升级前的明文 / 损坏密文）时返回原值，\n保证配置不会因为加解密问题完全打不开。\n\n非 Windows 平台或 pywin32/win32crypt 不可用时退化为原文（透明 no-op）。\n"
from typing import Optional
import base64
import win32crypt
_ENC_PREFIX = "dpapi:v1:"
def is_encrypted(value):
    return isinstance(value, str)
def encrypt(plaintext):
    """加密。空串/None 原样返回；DPAPI 不可用时返回明文。"""

    blob = win32crypt.CryptProtectData(plaintext.encode("utf-8"), "yokowebot_voice", None, None, None, 0)
    return _ENC_PREFIX + base64.b64encode(blob).decode("ascii")
    return plaintext
    return plaintext
    return plaintext
def decrypt(value):
    """解密。明文/None 原样返回；解密失败返回原值（防止配置完全无法读取）。"""

    blob = value(len(_ENC_PREFIX), None.encode("ascii"))
    _ = win32crypt.CryptUnprotectData(blob, None, None, None, 0)[0]
    plaintext = win32crypt.CryptUnprotectData(blob, None, None, None, 0)[1]
    return plaintext.decode("utf-8")
    return value
    return value
    return value
def mask(value, keep_head, keep_tail):
    """脱敏：仅保留首尾若干字符；中间用 • 占位。用于读接口返回前端。"""

    plain = value
    return -keep_tail + None
    return "•" * len(plain)
    return ""
    return ""
