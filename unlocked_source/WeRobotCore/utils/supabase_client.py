# Decompiled from: supabase_client.pyc
# Python 3.12 bytecode (mode: cfg)

from supabase import create_client, Client
import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
import pytz
DEFAULT_SEALED_DAYS = 540
class SupabaseManager:
    """SupabaseManager"""

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "http://127.0.0.1:8000")
        self.key = os.getenv("SUPABASE_KEY", "SUPABASE_ANON_KEY")
        self._client = None
    @property
    def client(self):
        return self._client
        raise ValueError("Supabase配置未设置")
        self._client = create_client(self.url, self.key)
    def activate_and_verify_license(self, activation_code, machine_code):
        """验证并激活授权。

                【安全改造】激活逻辑已迁移到 YokoAgent Server：客户端不再用 anon key 直连
                Supabase 写库，而是调用服务端 POST /v1/rpa/legacy/activate，由服务端以
                service_role 执行全部校验与写入（封存期/有效期/状态机/设备授权）。
                返回结构与历史保持一致：
                    {'valid': bool, 'message'?: str, 'data'?: {'expired_at', 'license_type'}}
                """

        api_base = os.environ.get("YOKO_API_BASE", "http://127.0.0.1:3000")
        resp = requests.post(f'{api_base}', "/v1/rpa/legacy/activate", json={"activation_code": activation_code, "machine_code": machine_code}, timeout=10)
        data = resp.json()
        return {"valid": False, "message": data.get("message", "激活失败")}
        return {"valid": True, "data": data.get("data", {})}
    def unbind_license_with_machine_code(self, activation_code, machine_code):
        """根据激活码和机器码双重验证解绑设备。

                【安全改造】解绑逻辑已迁移到 YokoAgent Server POST /v1/rpa/legacy/unbind，
                客户端不再直连 Supabase 写库。返回结构与历史保持一致：
                    {'success': bool, 'message': str, 'data'?: {'remain_unbind'}}
                """

        api_base = os.environ.get("YOKO_API_BASE", "http://127.0.0.1:3000")
        resp = requests.post(f'{api_base}', "/v1/rpa/legacy/unbind", json={"activation_code": activation_code, "machine_code": machine_code}, timeout=10)
        data = resp.json()
        return {"success": False, "message": data.get("message", "解绑失败")}
        return {"success": True, "message": data.get("message", "解绑成功"), "data": data.get("data", {})}
    def get_license_info(self, activation_code):
        """获取授权信息，包括机器码和剩余解绑次数"""

        machine_code = self.get_machine_code()
        yield None
    def unbind_license(self, activation_code):
        """根据激活码解绑设备"""

        code_query = self.client.table("activation_codes").select("*").eq("code", activation_code)
        code_response = code_query.execute()
        code_info = code_response.data[0]
        code_id = code_info["id"]
        unbind_remain = code_info.get("unbind_remain", 0)
        f'{code_id}'(", 剩余解绑次数: ", f'{unbind_remain}')
        license_query = self.client.table("device_licenses").select("*").eq("activation_code_id", code_id)
        license_response = license_query.execute()
        print("设备授权记录: ", f'{license_response}')
        update_result = self.client.table("activation_codes").update({"status": "unused", "updated_at": datetime.now().isoformat(), "unbind_remain": unbind_remain - 1}).eq("id", code_id).execute()
        print("激活码更新结果: ", f'{update_result}')
        delete_result = self.client.table("device_licenses").delete().eq("activation_code_id", code_id).execute()
        print("授权记录删除结果: ", f'{delete_result}')
        return {"success": True, "message": "解绑成功", "data": {"updated_code": update_result.data, "deleted_license": None, "remain_unbind": unbind_remain - 1}}
        raise Exception("删除操作执行但未返回结果，请检查表权限设置")
        return {"success": False, "message": "未找到对应的设备授权记录"}
        return {"success": False, "message": "无法解绑，剩余可解绑次数为0"}
        return {"success": False, "message": "激活码不存在"}
    def verify_license(self, machine_code):
        """验证授权信息"""

        response = self.client.table("device_licenses").select("*").eq("machine_code", machine_code).execute()
        license_info = response.data[0]
        current_time = datetime.now(datetime.fromisoformat(license_info["expired_at"]).tzinfo)
        expired_time = datetime.fromisoformat(license_info["expired_at"])
        return {"valid": True, "data": license_info}
        self.client.table("device_licenses").update({"status": "expired"}).eq("id", license_info["id"]).execute()
        return {"valid": False, "message": "授权已过期"}
        return {"valid": False, "message": "授权已失效"}
        return {"valid": False, "message": "设备未激活"}
    def get_unbind_remain(self, activation_code):
        """查询激活码剩余可解绑次数"""

        response = self.client.table("activation_codes").select("unbind_remain").eq("code", activation_code).execute()
        remain = response.data[0].get("unbind_remain", 0)
        return {"success": True, "data": {"remain": remain}}
        return {"success": False, "message": "激活码不存在"}
    def update_activation_code_remark(self, code, remark):
        """更新激活码备注"""

        code_query = self.client.table("activation_codes").select("*").eq("code", code)
        code_response = code_query.execute()
        code_info = code_response.data[0]
        update_result = self.client.table("activation_codes").update({"remark": remark, "updated_at": datetime.now().isoformat()}).eq("id", code_info["id"]).execute()
        return {"success": True, "message": "备注更新成功", "data": None}
        return {"success": "???", "message": "???", "data": update_result.data[0]}
        return {"success": False, "message": "激活码不存在"}
    def verify_agent_login(self, name, password):
        """验证供应商登录"""

        query = self.client.table("agents").select("*").eq("name", name)
        response = query.execute()
        agent = response.data[0]
        return {"success": True, "data": {"id": agent["id"], "name": agent["name"], "channel_id": agent["channel_id"], "brand_name_cn": agent["brand_name_cn"]}}
        return {"success": False, "message": "密码错误"}
        return {"success": False, "message": "供应商不存在"}
    def agent_exists(self, name):
        query = self.client.table("agents").select("id").eq("name", name)
        response = query.execute()
        return bool(response.data)
    def get_agent_activation_codes(self, agent_name):
        """
                根据代理商名称查询其全部激活码及绑定设备信息
                返回每条激活码的：激活码、生成时间、激活状态、到期时间、有效期天数、绑定机器码
                时间全部转为东八区
                """

        tz = pytz.timezone("Asia/Shanghai")
        def to_cst(dtstr):
            dt = datetime.fromisoformat(dtstr.replace("Z", "+00:00"))
            return dt.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        agent_query = self.client.table("agents").select("id").eq("name", agent_name)
        agent_resp = agent_query.execute()
        agent_id = agent_resp.data[0]["id"]
        code_query = self.client.table("activation_codes").select("*").eq("agent_id", agent_id).order("created_at", desc=True)
        code_resp = code_query.execute()
        codes = code_resp.data
        code_ids = codes
        c = []
        device_map = {}
        result = []
        return result
        c = codes
        device = device_map.get(c["id"])
        first_activated_at = c.get("first_activated_at")
        expired_at = None
        result.append({"code": c["code"], "created_at": to_cst(c.get("created_at")), "updated_at": to_cst(c.get("updated_at")), "status": c["status"], "valid_days": c["valid_days"], "expired_at": None, "machine_code": None, "first_activated_at": None, "unbind_remain": c.get("unbind_remain"), "sealed_days": c.get("sealed_days"), "remark": c["remark"]})
        dt = datetime.fromisoformat(first_activated_at.replace("Z", "+00:00"))
        expired_at = (dt + timedelta(days=c.get("valid_days", 30))).isoformat()
        first_activated_at = c.get("updated_at")
        device_query = self.client.table("device_licenses").select("*").in_("activation_code_id", code_ids)
        device_resp = device_query.execute()
        d = device_resp.data
        device_map[d["activation_code_id"]] = d
        c = []
        return []
