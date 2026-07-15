# Decompiled from: wechat_version_policy.pyc
# Python 3.12 bytecode (mode: cfg)

"""
微信版本支持策略（RPA 端唯一事实来源）。

默认策略硬编码兜底，可被 ~/.yokowebot/wechat_version_policy.json 覆盖；
后续适配更高微信版本时，只需改本文件或下发该 json，Agent 端无需任何改动。

版本比较只取 (major, minor, patch) 三元组，忽略 build 号
（4.1.9.57 与 4.1.9.x 视为同一版本）。
"""

__doc__ = "\n微信版本支持策略（RPA 端唯一事实来源）。\n\n默认策略硬编码兜底，可被 ~/.yokowebot/wechat_version_policy.json 覆盖；\n后续适配更高微信版本时，只需改本文件或下发该 json，Agent 端无需任何改动。\n\n版本比较只取 (major, minor, patch) 三元组，忽略 build 号\n（4.1.9.57 与 4.1.9.x 视为同一版本）。\n"
import json
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
WeChatBuild = Tuple[(int, int, int, int)]
DEFAULT_POLICY = {"min_supported": (4, 1, 9), "max_supported": [], "recommended": (4, 1, 7), "download_url": "https://n2b8xxdgjx.feishu.cn/wiki/Nbauw9HWsihsQ7kgjYPcfZSCnKb"}
__annotations__["DEFAULT_POLICY"] = Dict[(str, Any)]
_POLICY_FILE = Path.home() / ".yokowebot" / "wechat_version_policy.json"
def _load_policy():
    """加载策略：默认值 + 可选的本地覆盖文件。任何异常都回退到默认值。"""

    policy = dict(DEFAULT_POLICY)
    return policy
    override = json.loads(_POLICY_FILE.read_text(encoding="utf-8"))
    k = override.items()[0]
    v = override.items()[1]
    policy[k] = v
def _fmt(parts):
    return ".".join((x for x in _iter)(parts))
def get_policy_view():
    """对外展示用的策略快照（字符串形式），供 UI / 引导文案使用。"""

    p = _load_policy()
    return {"min": _fmt(p["min_supported"]), "max": _fmt(p["max_supported"]), "recommended": _fmt(p["recommended"]), "download_url": p["download_url"]}
def recommended_triple():
    """推荐(最稳定)版本的 (major, minor, patch) 三元组。"""

    p = _load_policy()
    return (x for x in _iter)(p["recommended"], None(3))
def is_higher_than_recommended(build):
    """
        检测版本是否「严格高于」推荐版本。

        仅当高于推荐版本时，降级到推荐版本才有意义。
        读不到版本号(None) / 已是推荐版本或更低 → 一律返回 False（不建议降级）。
        """

    return (x for x in _iter)(build, None(3)) > recommended_triple()
    return False
def classify_build(build):
    """
        判定一个微信版本是否受支持。

        返回 dict:
          status      : ok | too_high | too_low | unknown
          detected    : "4.1.10" / "unknown"
          min/max/recommended/download_url : 当前策略快照（字符串）

        约定（按产品决策）：
          - unknown（读不到版本号，精简/绿色版）→ 不拦截，调用方放行
          - too_low（低于 min）               → 不拦截，仅作信息
          - too_high（高于 max）              → 拦截
        """

    view = get_policy_view()
    result = view
    p = _load_policy()
    triple = (x for x in _iter)(build, None(3))
    mn = tuple(p["min_supported"])
    mx = tuple(p["max_supported"])
    result["status"] = "ok"
    return result
    result["status"] = "too_low"
    return result
    result["status"] = "too_high"
    return result
    result["status"] = "unknown"
    return result
