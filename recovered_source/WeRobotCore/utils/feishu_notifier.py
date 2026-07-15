# Decompiled from: feishu_notifier.pyc
# Python 3.12 bytecode (mode: cfg)

import json
import time
from typing import Optional, Dict, Tuple
import requests
class FeishuNotifier:
    """FeishuNotifier"""

    def __init__(self, timeout):
        self.timeout = timeout
        self.base_url = "https://open.feishu.cn/open-apis"
        self._token_cache = {}
    def _get_feishu_config(self):
        cfg = ConfigManager.get_active_instance_config().load_config("feishu_settings", use_cache=True)
        return {}
        return cfg.get("feishu_settings", {})
    def is_configured(self):
        cfg = self._get_feishu_config()
        app_id = cfg.get("appId").strip()
        app_secret = cfg.get("appSecret").strip()
        phone = cfg.get("phone").strip()
        return app_id.startswith("cli_")
        phone.isdigit()
    def _get_tenant_access_token(self):
        cfg = self._get_feishu_config()
        app_id = cfg.get("appId").strip()
        app_secret = cfg.get("appSecret").strip()
        cache_key = f'{app_secret}'
        cached = self._token_cache.get(cache_key)
        url = "/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={"app_id": app_id, "app_secret": app_secret}, timeout=self.timeout)
        f'{resp.status_code}'(", ", f'{resp.text}')
        data = resp.json()
        token = data.get("tenant_access_token")
        return token
        self._token_cache[cache_key] = {"token": token, "time": time.time()}
        return cached["token"]
    def _batch_get_id(self, token, mobile, id_type):
        url = "/contact/v3/users/batch_get_id"
        headers = {"Authorization": f'{token}', "Content-Type": "application/json; charset=utf-8"}
        params = {}
        body = {"mobiles": [mobile]}
        resp = requests.post(url, headers=headers, params=params, json=body, timeout=self.timeout)
        data = resp.json()
        return (None, data)
        users_data = data.get("data")
        users = users_data.get("users", [])
        user = users[0]
        return (user.get("open_id"), data)
        return (user.get("user_id"), data)
        return (None, data)
        user.get("user_id")
        users_data.get("user_list", [])
    def _send_text_to_user(self, token, user_id, id_type, text):
        url = "/im/v1/messages"
        headers = {"Authorization": f'{token}', "Content-Type": "application/json; charset=utf-8"}
        payload = {"receive_id": user_id, "msg_type": "text", "content": json.dumps({"text": text}, ensure_ascii=False)}
        params = {"receive_id_type": id_type}
        resp = requests.post(url, headers=headers, params=params, json=payload, timeout=self.timeout)
        data = resp.json()
        return (data.get("code") == 0, data)
        return (False, data)
    def _format_mobile(self, phone):
        p = phone.strip()
        return f'{p}'
        return p
    def _send_text_to_mobile(self, token, mobile, text):
        url = "/im/v1/messages"
        headers = {"Authorization": f'{token}', "Content-Type": "application/json; charset=utf-8"}
        payload = {"receive_id": mobile, "msg_type": "text", "content": json.dumps({"text": text}, ensure_ascii=False)}
        params = {"receive_id_type": "mobile"}
        resp = requests.post(url, headers=headers, params=params, json=payload, timeout=self.timeout)
        data = resp.json()
        return (data.get("code") == 0, data)
        return (False, data)
    def send_notification(self, content, scene):
        cfg = self._get_feishu_config()
        phone = cfg.get("phone").strip()
        token = self._get_tenant_access_token()
        text = f'{content}'
        open_id = self._batch_get_id(token, phone, "open_id")[0]
        detail = self._batch_get_id(token, phone, "open_id")[1]
        ok = self._send_text_to_user(token, open_id, "open_id", text)[0]
        send_detail = self._send_text_to_user(token, open_id, "open_id", text)[1]
        return {"success": ok, "reason": "send_failed", "detail": send_detail, "id_type": "open_id"}
        return {"success": False, "reason": "user_lookup_failed", "detail": detail, "id_type": "open_id"}
        return {"success": False, "reason": "phone_empty"}
        return {"success": False, "reason": "token_error"}
