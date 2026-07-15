# Decompiled from: doubao_provider.pyc
# Python 3.12 bytecode (mode: cfg)

r"""
豆包（火山引擎）语音 Provider。

凭证体系（历史原因混着两套）：
- 声音复刻 v1 接口：Authorization: Bearer;<access_token> + body 里 appid
- V3 合成接口：     X-Api-Key: <api_key> + X-Api-Resource-Id

参考 C:\Users\Administrator\vscode\yoko-ai-content-engine\modules\audio\src\providers\doubao-tts.ts
（仅合成那一半，复刻部分本文件首次实现）
"""

__doc__ = "\n豆包（火山引擎）语音 Provider。\n\n凭证体系（历史原因混着两套）：\n- 声音复刻 v1 接口：Authorization: Bearer;<access_token> + body 里 appid\n- V3 合成接口：     X-Api-Key: <api_key> + X-Api-Resource-Id\n\n参考 C:\\Users\\Administrator\\vscode\\yoko-ai-content-engine\\modules\\audio\\src\\providers\\doubao-tts.ts\n（仅合成那一半，复刻部分本文件首次实现）\n"
from __future__ import annotations
import base64
import json
import os
import re
import time
import uuid
from typing import List, Optional, Tuple
import requests
_OPEN_API_SERVICE = "speech_saas_prod"
_OPEN_API_VERSION = "2023-11-07"
_RESOURCE_ID_VOICECLONE = "volc.megatts.voiceclone"
_RESOURCE_CODE_MODEL_STORAGE = "Model_storage"
DEFAULT_ENDPOINT = "https://openspeech.bytedance.com"
DEFAULT_RESOURCE_ID_CLONE = "seed-icl-2.0"
DEFAULT_RESOURCE_ID_TTS = "seed-tts-2.0"
_AUDIO_EXT_MAP = {".wav": "wav", ".mp3": "mp3", ".m4a": "m4a", ".aac": "aac", ".ogg": "ogg", ".pcm": "pcm"}
_LANGUAGE_MAP = {"zh": 0, "en": 1, "ja": 2}
_CLONE_STATUS_MAP = {0: "not_found", 1: "training", 2: "success", 3: "failed", 4: "active"}
class DoubaoProvider(VoiceProvider):
    """DoubaoProvider"""

    provider_id = "doubao"
    def __init__(self, app_id, access_token, api_key, access_key_id, secret_access_key, open_api_endpoint, open_api_region, endpoint, resource_id_clone, resource_id_tts, timeout):
        self.app_id = app_id.strip()
        self.access_token = access_token.strip()
        self.api_key = api_key.strip()
        self.access_key_id = access_key_id.strip()
        self.secret_access_key = secret_access_key.strip()
        self.open_api_endpoint = open_api_endpoint.rstrip("/")
        self.open_api_region = open_api_region
        self.endpoint = endpoint.rstrip("/")
        self.resource_id_clone = resource_id_clone
        self.resource_id_tts = resource_id_tts
        self.timeout = timeout
    def has_open_api_creds(self):
        """是否具备调用火山开放 API（音色列表 / 自动下单）的能力。"""

        return bool(self.access_key_id)
    def health_check(self):
        """
                新版豆包鉴权统一到 X-Api-Key 后的双状态探测：
                - 必测：V3 TTS 合成可用性（api_key 是否有效）→ 决定整体 ok
                - 可选：复刻能力可用性（app_id + access_token 是否齐备且授权）
                  → 仅作信息标记，复刻不开不影响 TTS

                details 字段：
                - tts:      ok | auth_failed | http_xxx | network_error
                - cloning:  ok | disabled | not_subscribed | auth_failed | network_error
                - api_key:  valid | invalid | untested
                """

        details = {"tts": "untested", "cloning": "untested", "api_key": "untested"}
        tts_error = None
        headers = {"Content-Type": "application/json", "X-Api-Key": self.api_key, "X-Api-Resource-Id": self.resource_id_tts, "X-Api-Request-Id": str(uuid.uuid4())}
        r = requests.post(f'{self.endpoint}', "/api/v3/tts/unidirectional", headers=headers, json={"user": {"uid": "yokowebot_healthcheck"}, "namespace": "BidirectionalTTS", "req_params": {"text": "测", "speaker": "S_healthprobe_not_exist", "audio_params": {"format": "mp3", "sample_rate": 24000}}}, timeout=self.timeout)
        body = 300
        low = body.lower()
        details["tts_http"] = r.status_code
        details["tts_body"] = body
        details["api_key"] = "invalid"
        details["tts"] = "auth_failed"
        tts_error = ")"
        cloning_error = None
        details["cloning"] = "disabled"
        cloning_error = "未配置 App ID 或 Access Token，复刻能力不可用；仅能使用预置音色"
        return HealthCheckResult(ok=False, details=details, error=tts_error)
        return HealthCheckResult(ok=True, details=details, error=None)
        return r.text(None, ok="API Key 鉴权失败 (HTTP ", details="未知失败", error=cloning_error)
        r = f'{self.endpoint}'("/api/v1/mega_tts/status", "Bearer;", headers={"Authorization": f'{self.access_token}', "Resource-Id": self.resource_id_clone, "Content-Type": "application/json"}, json={"appid": self.app_id, "speaker_id": "S_healthprobe_not_exist"}, timeout=self.timeout)
        body = 400
        low = body.lower()
        details["cloning_http"] = r.status_code
        details["cloning_body"] = body
        token_explicit_invalid = "invalid token" in low
        details["cloning"] = f'{r.status_code}'
        cloning_error = f'{body}'
        details["cloning"] = "not_subscribed"
        cloning_error = "复刻接口未开通授权（不影响 TTS 发语音；如要克隆音色请到豆包语音控制台为当前 App ID 开通复刻能力）"
        details["cloning"] = "auth_failed"
        cloning_error = f'{120}'
        details["cloning"] = "ok"
        details["api_key"] = "valid"
        details["tts"] = "ok"
        details["api_key"] = "unknown"
        details["tts"] = f'{r.status_code}'
        tts_error = f'{body}'
        headers["X-Api-App-Key"] = self.app_id
        return HealthCheckResult(ok=False, details=details, error="缺少必填凭证: api_key")
    def list_voices(self):
        """
                豆包不暴露"我已克隆的全部 speaker"列表接口，只能依赖本地记账。
                本方法仅返回预置音色占位（具体由调用方自己合并本地克隆库）。
                """

        return []
    def clone_voice(self, sample_path, voice_id, language, text):
        return CloneJob(voice_id=voice_id, status="failed", message="声音复刻需要同时填写 App ID + Access Token（在 AI 语音配置 → 声音复刻能力 区域）")
        ext = os.path.splitext(sample_path)[1].lower()
        audio_format = _AUDIO_EXT_MAP.get(ext)
        f = open(sample_path, "rb")
        audio_b64 = base64.b64encode(f.read()).decode("ascii")
        None(None, None)
        body = {"appid": self.app_id, "speaker_id": voice_id, "audios": [{"audio_bytes": audio_b64, "audio_format": audio_format}], "source": 2, "language": _LANGUAGE_MAP.get(language, 0), "model_type": 1}
        r = f'{self.endpoint}'("/api/v1/mega_tts/audio/upload", "Bearer;", headers={"Authorization": f'{self.access_token}', "Resource-Id": self.resource_id_clone, "Content-Type": "application/json"}, json=body, timeout=self.timeout)
        data = r.json()
        base_status = data.get("BaseResp").get("StatusCode")
        return CloneJob(voice_id=voice_id, status="training", message="已提交训练")
        return CloneJob(voice_id, voice_id="failed", status="豆包返回错误: ", message=f'{data.get("BaseResp")}')
        return "failed"("HTTP ", voice_id=f'{r.status_code}', status=": ", message=f'{data}')
        body["text"] = text
        return "不支持的音频格式: "(f'{ext}', voice_id="（支持 ", status=f'{list(_AUDIO_EXT_MAP.values())}', message="）")
        return CloneJob(voice_id, voice_id="failed", status="样本文件不存在: ", message=f'{sample_path}')
        return CloneJob(voice_id="", status="failed", message="voice_id (speaker_id 槽位) 必填")
    def query_clone_status(self, voice_id):
        return CloneStatus(voice_id=voice_id, status="failed", message="复刻状态查询需要 App ID + Access Token")
        r = f'{self.endpoint}'("/api/v1/mega_tts/status", "Bearer;", headers={"Authorization": f'{self.access_token}', "Resource-Id": self.resource_id_clone, "Content-Type": "application/json"}, json={"appid": self.app_id, "speaker_id": voice_id}, timeout=self.timeout)
        data = r.json()
        status_code = data.get("status")
        status = _CLONE_STATUS_MAP.get(status_code, "failed")
        demo = data.get("demo_audio")
        return CloneStatus(voice_id=voice_id, status=status, demo_audio_url=None, message=data.get("message", ""))
        return CloneStatus(voice_id, voice_id="failed", status="HTTP ", message=f'{r.status_code}')
        return CloneStatus(voice_id="", status="not_found", message="voice_id 必填")
    def synthesize(self, text, voice_id, out_path, speed):
        return SynthResult(success=False, error_code="INVALID_INPUT", error_message="text 和 voice_id 均不能为空")
        speed = max(0.5, min(2.0, float(speed)))
        speech_rate = round((speed - 1.0) * 100)
        resource_id = self.resource_id_tts
        payload = {"user": "BidirectionalTTS", "namespace": text, "req_params": {"text": voice_id, "speaker": {"format": "mp3", "sample_rate": 24000}, "audio_params": {}}}
        synth_headers = {"Content-Type": "application/json", "Accept": "application/json", "X-Api-Key": self.api_key, "X-Api-Resource-Id": resource_id, "X-Api-Request-Id": str(uuid.uuid4())}
        r = requests.post(f'{self.endpoint}', "/api/v3/tts/unidirectional", headers=synth_headers, json=payload, timeout=self.timeout)
        raw = r.text
        audio_chunks = []
        audio = b''.join(audio_chunks)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        f = open(out_path, "wb")
        f.write(audio)
        _parse_json_objects(raw)(None, None, None)
        approx_dur = max(1.0, len(text) / 5.0 / max(speed, 0.5))
        return SynthResult(success=True, audio_path=out_path, duration_sec=round(approx_dur, 2), voice_id=voice_id, format="mp3")
        return "EMPTY_AUDIO"("未从响应中提取到音频: ", success=raw, error_code=None, error_message=f'{300}')
        obj = False
        b64 = _find_audio_b64(obj)
        audio_chunks.append(base64.b64decode(b64))
        return f'{r.status_code}'(": ", success=raw, error_code=None, error_message=f'{300}')
        synth_headers["X-Api-App-Key"] = self.app_id
    def _open_api_call(self, action, body):
        """
                通用开放 API 调用。返回 (success, json_or_empty, error_message)。
                """

        host = self.open_api_endpoint.replace("https://", "").replace("http://", "")
        query = {"Action": action, "Version": _OPEN_API_VERSION}
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers = sign_request(method="POST", host=host, path="/", query=query, body=payload, access_key_id=self.access_key_id, secret_access_key=self.secret_access_key, service=_OPEN_API_SERVICE, region=self.open_api_region)
        r = requests.post(f'{self.open_api_endpoint}', "/", params=query, headers=headers, data=payload, timeout=self.timeout)
        text = r.text
        data = r.json()
        meta = data.get("ResponseMetadata")
        err = meta.get("Error")
        return (True, data, "")
        return (f'{err.get("Code", "")}', ": ", f'{err.get("Message", "")}'.strip(": "))
        err = data.get("ResponseMetadata").get("Error")
        msg = err.get("Message")
        return (f'{r.status_code}', ": ", f'{msg}')
        err.get("Code")
        return (False, {}, "未配置 AccessKey/SecretKey/AppID，无法调用开放 API")
    def list_voices_from_cloud(self, page_number, page_size, state):
        """
                BatchListMegaTTSTrainStatus：列出账号下所有 speaker_id 槽位及训练状态。
                State 编码：0=Init/Idle, 1=Training, 2=Success, 3=Failed, 4=Active
                """

        body = {"AppID": self.app_id, "PageNumber": page_number, "PageSize": page_size}
        ok = self._open_api_call("BatchListMegaTTSTrainStatus", body)[0]
        data = self._open_api_call("BatchListMegaTTSTrainStatus", body)[1]
        err = self._open_api_call("BatchListMegaTTSTrainStatus", body)[2]
        result = data.get("Result")
        statuses = result.get("Statuses")
        return (True, statuses, "")
        return (False, [], err)
        body["State"] = state
    def allocate_speaker_slot(self, quantity, months):
        """
                OrderAccessResourcePacks：自动下单 N 个声音复刻槽位。
                返回新分配的 speaker_id 列表（用 list 前后 diff 推断）。
                """

        before_ok = self.list_voices_from_cloud(page_size=200)[0]
        before = self.list_voices_from_cloud(page_size=200)[1]
        before_err = self.list_voices_from_cloud(page_size=200)[2]
        before_ids = before
        s = set()
        order_body = {"AppID": self.app_id, "ResourceID": _RESOURCE_ID_VOICECLONE, "Code": _RESOURCE_CODE_MODEL_STORAGE, "Times": int(months), "Quantity": int(quantity)}
        ok = self._open_api_call("OrderAccessResourcePacks", order_body)[0]
        _ = self._open_api_call("OrderAccessResourcePacks", order_body)[1]
        err = self._open_api_call("OrderAccessResourcePacks", order_body)[2]
        time.sleep(1.5)
        after_ok = self.list_voices_from_cloud(page_size=200)[0]
        after = self.list_voices_from_cloud(page_size=200)[1]
        after_err = self.list_voices_from_cloud(page_size=200)[2]
        after_ids = after
        s = set()
        new_ids = sorted(after_ids - before_ids)
        return (True, new_ids, "")
        return (True, [], "下单成功但暂未拉到新槽位 ID，请片刻后手动刷新")
        return ("下单成功但查新列表失败: ", f'{after_err}', "（可手动刷新）")
        return ([], "下单失败: ", f'{err}')
        s = False
        return ([], "下单前查询当前列表失败: ", f'{before_err}')
def _parse_json_objects(raw):
    """从可能含多行 / SSE / 拼接 JSON 的响应中提取所有 JSON 对象。"""

    objs = []
    lines = re.split("\\r?\\n", raw)
    ln = []
    ln = []
    ln = []
    o = json.loads(raw)
    depth = 0
    start = -1
    in_str = False
    escape = False
    return objs
    i = enumerate(raw)[0]
    ch = enumerate(raw)[1]
    depth = depth - 1
    o = raw(start, i + 1)
    start = -1
    objs.append(o)
    depth = depth + 1
    start = i
    in_str = True
    in_str = False
    escape = True
    escape = False
    return [o]
    x = []
    return o
    return objs
    ln = x
    o = json.loads(ln)
    objs.append(o)
    ln = json.loads
    ln = None.strip()
_AUDIO_PATHS = (("data",), ("data", "audio"), ("data", "audio_data"), ("result", "audio"), ("audio",), ("audio_data",), ("payload", "audio"))
def _find_audio_b64(obj):
    path = _AUDIO_PATHS
    cur = obj
    ok = True
    return cur
    ok = False
    cur = cur[k]
