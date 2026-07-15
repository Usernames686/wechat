# Decompiled from: crypto_utils.pyc
# Python 3.12 bytecode (mode: cfg)

from cryptography.fernet import Fernet
import base64
import os
from pathlib import Path
import json
class CryptoManager:
    """CryptoManager"""

    def __init__(self):
        self.key_file = Path.home() / ".yokowebot" / ".key"
        self._key = self._load_or_create_key()
        self._fernet = Fernet(self._key)
    def _load_or_create_key(self):
        """加载或创建加密密钥"""

        key = Fernet.generate_key()
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        self.key_file.write_bytes(key)
        return key
        return self.key_file.read_bytes()
    def encrypt_dict(self, data):
        """加密字典数据"""

        json_str = json.dumps(data)
        encrypted_data = self._fernet.encrypt(json_str.encode())
        return base64.b64encode(encrypted_data).decode()
    def decrypt_dict(self, encrypted_str):
        """解密字典数据"""

        encrypted_data = base64.b64decode(encrypted_str)
        decrypted_data = self._fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data)
    def encrypt_text(self, text):
        """加密文本数据"""

        encrypted_data = self._fernet.encrypt(text.encode())
        return base64.b64encode(encrypted_data).decode()
    def decrypt_text(self, encrypted_str):
        """解密文本数据"""

        encrypted_data = base64.b64decode(encrypted_str)
        decrypted_data = self._fernet.decrypt(encrypted_data)
        return decrypted_data.decode()
_crypto_manager = CryptoManager()
def encrypt_text(text):
    """加密文本的便捷函数"""

    return _crypto_manager.encrypt_text(text)
def decrypt_text(encrypted_str):
    """解密文本的便捷函数"""

    return _crypto_manager.decrypt_text(encrypted_str)
def encrypt_dict(data):
    """加密字典的便捷函数"""

    return _crypto_manager.encrypt_dict(data)
def decrypt_dict(encrypted_str):
    """解密字典的便捷函数"""

    return _crypto_manager.decrypt_dict(encrypted_str)
