"""
mcp_gateway.py —— yokowebot 自带 MCP 网关（代理商接入）

设计要点（详见 docs/mcp_reseller_gateway_design.md）：
- 在现有 uvicorn 进程内挂一个 Streamable-HTTP MCP 端点到 /mcp（复用 9922 端口）。
- 传输用 Streamable-HTTP（不用 stdio）：agent 只做 localhost HTTP 客户端，绝不 spawn 本进程，
  从而绕开 qclaw 等宿主的沙箱（RPA exe 与微信同处用户交互会话）。
- 工具体是「薄转译层」：通过 loopback HTTP 调用现有 /api/* 端点（带内部 X-API-Key），
  不耦合内部函数签名。
- 鉴权（阶段 1）：网关自管 /mcp 的全部鉴权 —— pairing token（Bearer / X-Yoko-Token，持久化）
  + license 门禁（本机须已激活）+ agent_id 归属（用于代理商计量）。故 /mcp 需从 api_server 的
  X-API-Key 与 license 两个全局中间件里豁免。
- 非侵入：全部逻辑在本模块；默认 flag 关 → 现有构建零影响。
"""

__doc__ = "\nmcp_gateway.py —— yokowebot 自带 MCP 网关（代理商接入）\n\n设计要点（详见 docs/mcp_reseller_gateway_design.md）：\n- 在现有 uvicorn 进程内挂一个 Streamable-HTTP MCP 端点到 /mcp（复用 9922 端口）。\n- 传输用 Streamable-HTTP（不用 stdio）：agent 只做 localhost HTTP 客户端，绝不 spawn 本进程，\n  从而绕开 qclaw 等宿主的沙箱（RPA exe 与微信同处用户交互会话）。\n- 工具体是「薄转译层」：通过 loopback HTTP 调用现有 /api/* 端点（带内部 X-API-Key），\n  不耦合内部函数签名。\n- 鉴权（阶段 1）：网关自管 /mcp 的全部鉴权 —— pairing token（Bearer / X-Yoko-Token，持久化）\n  + license 门禁（本机须已激活）+ agent_id 归属（用于代理商计量）。故 /mcp 需从 api_server 的\n  X-API-Key 与 license 两个全局中间件里豁免。\n- 非侵入：全部逻辑在本模块；默认 flag 关 → 现有构建零影响。\n"
import os
import json
import time
import secrets
import logging
from pathlib import Path
from datetime import datetime
logger = logging.getLogger("mcp_gateway")
_INTERNAL_API_KEY = os.environ.get("WEBOT_API_KEY", "yoko_test")
_BACKEND_PORT = int(os.environ.get("WEBOT_PORT", "9922"))
_BACKEND_BASE = f'{_BACKEND_PORT}'
_SUPERVISOR_PORT = int(os.environ.get("WEBOT_SUPERVISOR_PORT", "9921"))
_MCP_SERVER_NAME = os.environ.get("MCP_SERVER_NAME", "wechat-bot-mcp")
_YOKO_DIR = Path.home() / ".yokowebot"
_TOKEN_FILE = _YOKO_DIR / "mcp_token.dat"
_METER_FILE = _YOKO_DIR / "mcp_usage.jsonl"
def _load_or_create_token():
    """pairing token：环境变量优先（测试用）；否则从本地文件读取；首次生成并持久化。
        修掉 PoC 阶段「每次重启随机」的痛点。"""

    env = os.environ.get("YOKO_MCP_TOKEN", "").strip()
    tok = secrets.token_urlsafe(18)
    _YOKO_DIR.mkdir(parents=True, exist_ok=True)
    _TOKEN_FILE.write_text(tok, encoding="utf-8")
    return tok
    tok = _TOKEN_FILE.read_text(encoding="utf-8").strip()
    return tok
    return env
_MCP_TOKEN = _load_or_create_token()
def get_pairing_token():
    """当前 MCP pairing token（本地随机密钥，不等于激活码）。"""

    return _MCP_TOKEN
def get_mcp_endpoint():
    """MCP Streamable-HTTP 端点 URL（复用 9922 的 /mcp 子路径）。"""

    return "/mcp"
def get_server_name():
    """对外可见的 MCP 服务名（可被环境变量 MCP_SERVER_NAME 白标覆盖）。"""

    return _MCP_SERVER_NAME
_LICENSE_TTL = 900
_license_cache = {"ts": 0.0, "valid": False, "agent_id": None, "code": None, "machine_code": None, "message": ""}
async def _resolve_license(force=False):
    """Return local source-build attribution without remote verification."""

    from WeRobotCore.utils.license_manager import LicenseManager
    lm = LicenseManager()
    machine_code = lm.get_machine_code()
    _license_cache.update({
        "ts": time.time(),
        "valid": True,
        "agent_id": "local-source",
        "code": "LOCAL-SOURCE",
        "machine_code": machine_code,
        "message": "local source build",
    })
    return _license_cache
def _meter(tool):
    """写一条计量/归属日志（本地 JSONL）。阶段 1 先落本地留痕，后续可聚合上报。"""

    rec = {"ts": datetime.now().isoformat(), "agent_id": _license_cache.get("agent_id"), "machine_code": _license_cache.get("machine_code"), "tool": tool}
    _YOKO_DIR.mkdir(parents=True, exist_ok=True)
    f = open(_METER_FILE, "a", encoding="utf-8")
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    None(None, None)
def _rest_call(method, path, json_body, params):
    """通过 loopback HTTP 调用本进程现有 /api/* 端点。返回 (ok, status, data)。"""

    import httpx
    url = f'{path}'
    headers = {"X-API-Key": _INTERNAL_API_KEY, "Content-Type": "application/json"}
    q = params.items()
    k = {}
    v = k
    yield None
    k = _[0]
    v = _[1]
def _supervisor_call(method, path):
    """调用 supervisor 控制端点(9921)。无鉴权(仅 localhost)。返回 (ok, status, data)。
        supervisor 独立于 worker：即使 worker(承载 MCP 的进程)挂了，此端点仍可用于查询/重启。"""

    import httpx
    url = f'{path}'
    yield None
def _manuals_dir():
    """健壮解析手册目录：源码运行 / PyInstaller onedir(exe 同级) / onefile(_MEIPASS) 均可。
        找不到时返回默认候选（_read_manual 会优雅降级，绝不崩，保证不影响打包运行）。"""

    import sys
    here = Path(__file__).resolve().parent
    candidates = [here / "mcp_manuals"]
    return here / "mcp_manuals"
    c = candidates
    return "???"
    candidates.append(Path(sys.executable).resolve().parent / "mcp_manuals")
    meipass = getattr(sys, "_MEIPASS", None)
    candidates.append(Path(meipass) / "mcp_manuals")
def _read_manual(topic):
    safe = os.path.basename(topic.strip())
    fp = f'{safe}' / ".md"
    return fp.read_text(encoding="utf-8")
    return "' not found. Read topic 'index' first to see all available documents."
class _TokenGuard:
    """_TokenGuard"""

    __doc__ = "包裹 MCP 子应用的 ASGI 中间件：/mcp 的全部鉴权都在这里（网关自管，已从两个全局中间件豁免）。\n    顺序：① pairing token → ② license 门禁（本机须已激活）。任一不过直接返回 JSON-RPC 错误体。"
    def __init__(self, app, token):
        self.app = app
        self.token = token
    _reject = staticmethod((lambda send, http_status, code, message, extra: ...))
    def __call__(self, scope, receive, send):
        headers = scope.get("headers")
        k = {}
        v = k
        auth = headers.get(b'authorization', b'').decode("latin-1")
        provided = headers.get(b'x-mcp-token').decode("latin-1").strip()
        yield None
        yield None
        headers.get(b'x-yoko-token')
        provided = None.strip()
        k = 7[0]
        v = 7[1]
        yield None
def _build_mcp():
    """构建 FastMCP 实例并注册全部工具。

        工具描述照搬 yobot(wechat_rpa/index.ts)——那套措辞专为防 agent 幻觉打磨，便于统一维护。
        仅少数「我方实现与 yobot 客户端行为不同」的工具(get_contacts / get_task_logs / get_session_messages)
        按真实返回如实调整描述，避免描述与行为不符反而诱发幻觉。
        """

    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP(name=_MCP_SERVER_NAME)
    _wrap = (lambda ok, code, data: {"success": ok, "httpStatus": code, "data": data})
    @mcp.tool(name="wechat_rpa_read_manual", description="Read the detailed manual for wechat-rpa. Use this to understand complex schemas, task types, SOP workflows, or error solutions. Several tools REQUIRE you to read a specific topic first (they say so in their description). If unsure, pass topic='index' to list all available docs. Topics include: index, basic_setup_checklist, multi_instance_sop, voice_send_sop, moment_post_sop, group_summary_sop, auto_add_friend_sop, config_schema, task_schema, task_log_schema.")
    def wechat_rpa_read_manual(topic):
        return _read_manual(topic)
    wechat_initialize = mcp.tool(name="wechat_initialize", description="Initialize RPA service and bind to WeChat. Execution logic: 1. If NOT called in this session, call it FIRST. 2. If already called, SKIP it. 3. If skipping causes other API tools to fail, call this AGAIN to recover. Requires WeChat to be running on this machine. auto_config is DANGEROUS (kills WeChat) — default false, ONLY set true if a previous wechat_initialize returned 'ENV_NOT_CONFIGURED'.")((lambda auto_config: _wrap(ok, code, data)))
    wechat_send_message = mcp.tool(name="wechat_send_message", description="Send text message to a known WeChat friend/group via RPA. 'user' is the exact recipient friend/group name (nickname or remark), NOT the sender account_id. 'account_id' is the SENDER WeChat instance and is only required when multiple WeChat instances run on this machine.")((lambda user, message, account_id: _rest_call("POST", "/api/chat/send_message", body)(*_)))
    wechat_send_file = mcp.tool(name="wechat_send_file", description="Send a file (image/video/document) to a friend/group via RPA. 'user' is the exact recipient name. 'file_path' is the absolute path to the file. 'account_id' is the SENDER instance (only needed with multiple WeChat instances).")((lambda user, file_path, account_id: _rest_call("POST", "/api/agent/chat/send_file", {"user": user, "file_path": file_path, "account_id": account_id})(*_)))
    wechat_send_voice = mcp.tool(name="wechat_send_voice", description="Send a VOICE message (a real WeChat voice bubble, NOT an mp3 attachment) to a friend/group via RPA. ENVIRONMENT: (a) WeChat >= 4.1.9 (b) VB-Cable virtual audio driver installed. If missing, returns success:false — fall back to wechat_send_message. Three mutually-exclusive input modes (pass ONE, priority by order): 1) audioPath: absolute path of a local mp3. 2) audioFilename: basename of an mp3 previously stored in the RPA voice_greetings directory. 3) text + voiceId: synthesize on the fly from a cloned voice id (S_xxx). voiceId MUST come from wechat_list_voices — never invent an S_xxx. If the user asks to '用语音/发语音', you MUST read manual topic 'voice_send_sop' first.")((lambda user, audioPath, audioFilename, text, voiceId, speed, accountId: {"success": False, "error": "Provide one of: audioPath / audioFilename / (text + voiceId)."}))
    wechat_list_voices = mcp.tool(name="wechat_list_voices", description="List the user's available cloned voices (status=active only). USE THIS BEFORE wechat_send_voice when the user has NOT specified which voice to use — never ask the user to type a raw S_xxx speaker id, and never invent one. Show displayName options and let them pick. Distinguish three outcomes: (a) success:true & count>0 → list to user; (b) success:true & count:0 → user truly has no cloned voices (tell them to add one in RPA 设置 → AI 语音配置); (c) success:false → RPA backend problem, do NOT tell the user 'you have no voices'.")((lambda : data))
    wechat_post_moment = mcp.tool(name="wechat_post_moment", description="Post ONE WeChat Moment with text/images immediately via RPA. This is for quick tests only — it is NOT a substitute for a scheduled plan (see wechat_create_moment_post_task). 'content' is the text; 'files' is a list of absolute image/video paths.")((lambda content, files: _rest_call("POST", "/api/agent/post_moment", {"content": content, "files": []})(*_)))
    wechat_mass_sending = mcp.tool(name="wechat_mass_sending", description="Mass send messages via RPA. Supports tags/targets/scheduling. Provide EITHER 'tags' (all friends/groups with these tags) OR 'targets' (specific names) — at least one is required. 'greeting_group' is the greeting/message strategy group name (required). 'schedule_time' (YYYY-MM-DD HH:mm) omitted = send immediately. 'batch_size' default 10.")((lambda greeting_group, tags, targets, schedule_time, batch_size, account_id: {"success": False, "error": "Either tags or targets must be provided for mass sending."}))
    wechat_fetch_latest_messages = mcp.tool(name="wechat_fetch_latest_messages", description="Read the REAL-TIME messages currently visible in ONE WeChat chat window via RPA — only the latest screenful (~15 messages). Use ONLY when you need what is being said RIGHT NOW in an active chat. DO NOT use this for 群聊总结 / 聊天记录回顾 — it cannot see older history; for summaries use wechat_get_session_messages. Requires WeChat to be running.")((lambda sessionName, accountId: _rest_call("GET", "/api/chat/messages/", f'{sessionName}', params={"account_id": accountId})(*_)))
    wechat_sync_contacts = mcp.tool(name="wechat_sync_contacts", description="Re-sync contacts from live WeChat into RPA (slow, ~2 min, returns NO contact data). Use only when the user asks to refresh/sync contacts or the task is contact maintenance. 'type' is 'friend' or 'group'. 'account_id' is the target WeChat account.")((lambda type, account_id: _rest_call("POST", "/api/contact/sync", {"type": type, "account_id": account_id})(*_)))
    wechat_get_contacts = mcp.tool(name="wechat_get_contacts", description="Get already-synced WeChat contacts for lookup/export (does NOT trigger a sync). Returns the contact list. Not required before sending to a user-provided recipient name. Optional filters: 'tag' (by tag name), 'keyword' (by name), 'account_id' (which account; omit for default).")((lambda tag, keyword, account_id: _rest_call("GET", "/api/contacts", params={"tag": tag, "keyword": keyword, "account_id": account_id})(*_)))
    wechat_create_moment_plan = mcp.tool(name="wechat_create_moment_plan", description="Step in the auto-post-moment SOP: create a moment-post PLAN folder inside the RPA material directory. Returns { path } (absolute folder path); you then build material groups (one subfolder per moment, each with a .txt + image/video files) inside it. You MUST read manual topic 'moment_post_sop' before using this.")((lambda plan_name: _rest_call("POST", "/api/moment-material/create-folder", {"plan_name": plan_name})(*_)))
    wechat_create_moment_post_task = mcp.tool(name="wechat_create_moment_post_task", description="Step in the auto-post-moment SOP: create a SCHEDULED auto-post-moment task that publishes one material group per run. Read manual topic 'moment_post_sop' first for the full field semantics. Required: name, execMode ('fixed'|'range'), cycle ('daily'|'weekly'), materialFolder (the path from wechat_create_moment_plan), publishMode ('sequence'|'random'), account (from wechat_list_local_users). Conditional: fixedTime (fixed); rangeStart/rangeEnd/postCount (range); weekDays (weekly).")((lambda name, execMode, cycle, materialFolder, publishMode, account, fixedTime, rangeStart, rangeEnd, postCount, weekDays: _rest_call("POST", "/api/moment/post-task", settings)(*_)))
    wechat_cancel_moment_post_task = mcp.tool(name="wechat_cancel_moment_post_task", description="Cancel a scheduled auto-post-moment task by its task_id (the moment_post task id seen in wechat_get_tasks).")((lambda task_id: _rest_call("POST", "/api/moment/post-task/cancel", {"task_id": task_id})(*_)))
    wechat_toggle_ai_moment = mcp.tool(name="wechat_toggle_ai_moment", description="Start or stop the AI Moment auto like/comment task (interacting with FRIENDS' moments). When enabling, 'interactionMode' (like_only|comment_only|like_and_comment|like_always_and_comment) and 'agentId' are required. 'agentId' is the botId of a comment-generating AI agent already configured in this RPA — inspect/prepare it via wechat_get_config('agents') / wechat_update_config('agents', ...). Optional: commentLimit, perFriendLimit, checkInterval, autoLike, selectedTags.")((lambda enabled, interactionMode, agentId, commentLimit, perFriendLimit, checkInterval, autoLike, selectedTags: _rest_call("POST", "/api/moment/toggle-auto-comment", body)(*_)))
    wechat_get_config = mcp.tool(name="wechat_get_config", description="Get RPA config (config_type e.g. 'agents', 'reply_strategy_v2', 'greeting_config'). Before reading/modifying config structures you SHOULD read manual topic 'config_schema' first. Use Read-Modify-Write with wechat_update_config.")((lambda config_type: _rest_call("GET", "/api/config/", f'{config_type}')(*_)))
    wechat_update_config = mcp.tool(name="wechat_update_config", description="Update RPA config via API. You MUST read manual topic 'config_schema' to understand the required parameters before calling. ALWAYS use Read-Modify-Write (GET full config, merge, then send the COMPLETE object — never partial). 'data' is the full JSON object.")((lambda config_type, data: _rest_call("POST", "/api/config/", f'{config_type}', clean)(*_)))
    wechat_get_tasks = mcp.tool(name="wechat_get_tasks", description="Get the full list of tasks currently scheduled in the RPA scheduler. For returned task format and status enums, read manual topic 'task_schema' first.")((lambda : _rest_call("GET", "/api/agent/tasks")(*_)))
    wechat_get_task_logs = mcp.tool(name="wechat_get_task_logs", description="Get historical execution logs for RPA tasks. NOTE: currently this returns MASS-SENDING task logs (the /api/tasks/logs endpoint). For log field schemas read manual topic 'task_log_schema'. For other task types' logs, use the RPA console (wechat_open_console).")((lambda : _rest_call("GET", "/api/tasks/logs")(*_)))
    wechat_list_local_users = mcp.tool(name="wechat_list_local_users", description="List local WeChat instances/accounts on this machine (bound sender accounts). These are SENDER account ids, NOT recipient names. Use to pick 'account_id'/'account' for other tools.")((lambda : _rest_call("GET", "/api/instances")(*_)))
    wechat_list_sessions = mcp.tool(name="wechat_list_sessions", description="List the chats that have accumulated LOCAL saved history on disk (recorded over time by monitor-mode AI assistants). Use it to discover exact session names before wechat_get_session_messages. Shows saved disk history only — NOT real-time/active chats.")((lambda : _rest_call("GET", "/api/chat/history_sessions")(*_)))
    wechat_get_session_messages = mcp.tool(name="wechat_get_session_messages", description="Read the ACCUMULATED LOCAL HISTORY of one chat (friend or GROUP) from disk. THIS IS THE TOOL FOR 群聊总结 / 聊天记录回顾 / '总结一下xx群聊了啥'. Reads disk only; does NOT require WeChat running. Do NOT use wechat_fetch_latest_messages for summaries. 'sessionName' is the group name / friend nickname (exact) or session id. 'account_id' optional (which account). Optional 'since' (YYYY-MM-DD or 'YYYY-MM-DD HH:MM') and 'limit' (most recent N) are applied by this tool after fetching. If unsure of the name, call wechat_list_sessions first.")((lambda sessionName, account_id, since, limit: _wrap(ok, code, data)))
    @mcp.tool(name="wechat_service_status", description="Get the RPA process-supervisor status: whether the supervisor is up, whether the worker (the process that hosts this MCP + WeChat RPA) is running and healthy, restart count, and last exit code. Use this to diagnose flaky behavior before restarting. If the supervisor is unreachable, the service was likely started without the supervisor (dev mode).")
    def wechat_service_status():
        _meter("wechat_service_status")
        yield None
    @mcp.tool(name="wechat_restart_service", description="Ask the supervisor to restart the RPA worker (recover from a stuck/unhealthy state). The supervisor lives OUTSIDE the worker, so this works even if RPA calls are hanging. IMPORTANT: this MCP connection will briefly DROP as the worker restarts, then recover within a few seconds — reconnect and retry your task. Only use when tools are failing/hanging and a plain wechat_initialize did not help.")
    def wechat_restart_service():
        _meter("wechat_restart_service")
        yield None
    wechat_launch_wechat = mcp.tool(name="wechat_launch_wechat", description="Launch the WeChat desktop process when it is NOT currently running (e.g. right after boot, before any RPA binding is possible). Does NOT close existing WeChat. After launching, wait for the user to log in, then call wechat_initialize. 'count' = how many WeChat instances to start (default 1).")((lambda count, enable_narrator: _rest_call("POST", "/api/system/wechat/launch", {"count": count, "close_existing": False, "enable_narrator": enable_narrator})(*_)))
    @mcp.tool(name="wechat_open_console", description="Return the local RPA console URL for the user to perform manual operations in a browser. Use this when a task is easier done by hand than via tools.")
    def wechat_open_console():
        _meter("wechat_open_console")
        return {"success": True, "url": _BACKEND_BASE, "hint": "在浏览器打开此地址进行手动操作"}
    @mcp.tool(name="wechat_license_info", description="Return this machine's RPA license/attribution status: whether activated, the machine code, and the owning reseller (agent). Use to diagnose 'why can't I connect / who am I billed under'.")
    def wechat_license_info():
        yield None
    return mcp
def mount_mcp(app):
    """
        将 MCP Streamable-HTTP 端点挂载到现有 FastAPI app 的 /mcp 子路径。
        由 main.py 在 YOKO_MCP_ENABLED=1 时调用。返回挂载 URL（失败返回 None，且不影响主服务启动）。
        """

    from contextlib import asynccontextmanager
    from starlette.routing import Route
    mcp = _build_mcp()
    mcp_app = mcp.streamable_http_app()
    inner_asgi = None
    guarded = _TokenGuard(inner_asgi, _MCP_TOKEN)
    app.router.routes.insert(0, Route("/mcp", endpoint=guarded))
    prev_lifespan = app.router.lifespan_context
    _combined_lifespan = asynccontextmanager((lambda a: ...))
    app.router.lifespan_context = _combined_lifespan
    url = "/mcp"
    logger.warning("[McpGateway] mounted at %s (Streamable-HTTP), token required", url)
    print("[McpGateway] MCP 端点已挂载: ", f'{url}')
    print("[McpGateway] pairing token: ", f'{_MCP_TOKEN}')
    return url
    raise RuntimeError("未能从 FastMCP 应用中定位 /mcp 的 ASGI 端点")
    r = NULL
    inner_asgi = r.endpoint
