# Decompiled from: volc_signer.pyc
# Python 3.12 bytecode (mode: cfg)

"""
火山引擎 (Volcano Engine) Open API V4 风格签名实现。

参考：火山引擎签名规范（与 AWS Signature V4 兼容的变体）
  - 算法：HMAC-SHA256
  - Authorization header 形如：
      HMAC-SHA256 Credential=<AK>/<date>/<region>/<service>/request,
                  SignedHeaders=content-type;host;x-content-sha256;x-date,
                  Signature=<hex>

只覆盖本项目用得到的 POST + Action 查询参数 + JSON body 这一种调用形态。
未来需要 GET / 其它姿势再扩展。

外部入口：sign_request() 返回应该附到请求上的 headers。
"""

__doc__ = "\n火山引擎 (Volcano Engine) Open API V4 风格签名实现。\n\n参考：火山引擎签名规范（与 AWS Signature V4 兼容的变体）\n  - 算法：HMAC-SHA256\n  - Authorization header 形如：\n      HMAC-SHA256 Credential=<AK>/<date>/<region>/<service>/request,\n                  SignedHeaders=content-type;host;x-content-sha256;x-date,\n                  Signature=<hex>\n\n只覆盖本项目用得到的 POST + Action 查询参数 + JSON body 这一种调用形态。\n未来需要 GET / 其它姿势再扩展。\n\n外部入口：sign_request() 返回应该附到请求上的 headers。\n"
from __future__ import annotations
import datetime
import hashlib
import hmac
from typing import Dict, Mapping, Optional
from urllib.parse import quote
_ALGORITHM = "HMAC-SHA256"
_REQUEST_SUFFIX = "request"
def _sha256_hex(payload):
    return hashlib.sha256(payload).hexdigest()
def _hmac_sha256(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
def _canonical_query(query):
    """key 升序 + URL 编码后 join。"""

    items = sorted(query.items(), key=lambda kv: kv[0])
    parts = []
    return "&".join(parts)
    k = items[0]
    v = items[1]
    ek = quote(str(k), safe="-_.~")
    ev = quote(str(v), safe="-_.~")
    f'{ek}'("=", f'{ev}')
    return ""
def _canonical_headers(headers):
    """
        canonical_headers 形如：
          content-type:application/json

          host:open.volcengineapi.com

          x-content-sha256:<hex>

          x-date:20231107T120000Z

        """

    items = sorted((_item for _item in _iter)(headers.items()), key=lambda kv: kv[0])
    return "\n".join((_item for _item in _iter)(items)) + "\n"
def _signed_headers(headers):
    return ";".join(sorted((k for k in _iter)(headers.keys())))
def _derive_signing_key(secret_key, date, region, service):
    k_date = _hmac_sha256(secret_key.encode("utf-8"), date)
    k_region = _hmac_sha256(k_date, region)
    k_service = _hmac_sha256(k_region, service)
    k_signing = _hmac_sha256(k_service, _REQUEST_SUFFIX)
    return k_signing
def sign_request():
    """
        为请求计算签名，返回应该附上的 HTTP headers（含 Authorization）。

        用法：把返回的 dict 整个 merge 进 requests 的 headers 即可。
        """

    x_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_only = now.strftime("%Y%m%d")
    x_content_sha256 = _sha256_hex(body)
    base_headers = {"Content-Type": content_type, "Host": host, "X-Content-Sha256": x_content_sha256, "X-Date": x_date}
    canonical_request = "\n".join([method.upper(), path, _canonical_query(query), _canonical_headers(base_headers), _signed_headers(base_headers), x_content_sha256])
    credential_scope = f'{_REQUEST_SUFFIX}'
    string_to_sign = "\n".join([_ALGORITHM, x_date, credential_scope, _sha256_hex(canonical_request.encode("utf-8"))])
    signing_key = _derive_signing_key(secret_access_key, date_only, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    authorization = f'{signature}'
    return {"Content-Type": content_type, "Host": host, "X-Content-Sha256": x_content_sha256, "X-Date": x_date, "Authorization": authorization}
    now = datetime.datetime.now(datetime.timezone.utc)
