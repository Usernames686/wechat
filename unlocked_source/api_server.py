from math import log
import sys
import os
import warnings
sys.coinit_flags = 2
warnings.filterwarnings("ignore", message="Apply externally defined coinit_flags", category=UserWarning)
from WeRobotCore.utils.data_manager import DataManager
DataManager()
import time
import asyncio
import logging
import traceback
from fastapi import FastAPI, Security, HTTPException, Request, File, UploadFile, WebSocket, Query, Body, Form
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pathlib import Path
from fastapi import status
from WeRobotCore.utils.license_manager import LicenseManager
from WeRobotCore.api.file import save_uploaded_file, list_moment_plans, list_moment_groups, select_moment_folder_and_groups, open_folder
from WeRobotCore.utils.file_library_manager import FileLibraryManager
from pydantic import BaseModel, Field, ConfigDict
import uvicorn
import uuid
from typing import Dict, Optional, List, Union
from WeRobotCore.api import chat, file, friend, guide, settings_backup
from WeRobotCore.core.WeChatType import WeChat
from datetime import datetime, timezone, timedelta
from WeRobotCore.utils.config_manager import ConfigManager
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()
from WeRobotCore.task_system_v2.websocket_manager import websocket_manager
from WeRobotCore.core.instance_manager_v2 import InstanceManagerV2
from WeRobotCore.core.instance_manager_v3 import InstanceManagerV3
from WeRobotCore.task_system_v2.multi_chat_monitor import multi_chat_monitor
from WeRobotCore.task_system_v3.unified_manager_pattern import get_mass_sending_manager, get_auto_reply_manager, get_moment_comment_manager, get_moment_post_manager, get_friend_request_manager, get_add_friend_manager, get_auto_follow_manager, get_sync_contacts_manager, get_scheduler
logging.info("V3 任务系统组件导入成功")
from WeRobotCore.utils.logger import task_logger
from WeRobotCore.utils.excel_parser import parse_friend_list
from WeRobotCore.core.uia_error import WeChatUIAError
from WeRobotCore.utils.supabase_client import SupabaseManager
from WeRobotCore.utils.version_manager import VersionManager
from WeRobotCore.api.customer_api import customer
from WeRobotCore.api.agent_api import AgentAPI
import shutil
import tempfile
frontend_path = None
env_frontend_path = os.environ.get("WEBOT_FRONTEND_PATH")
application_path = os.path.dirname(os.path.abspath(__file__))
builtin_path = Path(application_path) / "webot" / "dist"
app = FastAPI(title="WeRobotCore API")
print("注意: 当前无UI界面，仅API模式")
def get_config_manager():
    """动态获取ConfigManager实例，支持多实例切换"""

    return ConfigManager.get_active_instance_config()
license_manager = LicenseManager()
agent_api = AgentAPI()
def get_multi_chat_monitor():
    """获取MultiChatMonitor实例，统一管理所有监控器"""

    return multi_chat_monitor
@app.get("/api/health")
def health_check():
    """
        服务健康检查端点
        供生命周期管理器验证服务身份
        """

    from WeRobotCore import __version__
    return {"status": "ok", "service": "yokobot", "pid": os.getpid(), "version": __version__, "timestamp": datetime.now().isoformat()}
@Request
def open_browser(request):
    """在系统默认浏览器打开一个 http(s) 链接（用于"下载安装器"引导——webview 内 window.open 不可靠）。
        仅允许 http/https，本机单用户场景。"""

    yield None
@app.get("/api/system/install-channel")
def get_install_channel():
    """上报本客户端安装渠道：'installer'（安装器装）或 'zip'（解压包）。
        供前端在欢迎页给 zip 用户显示"迁移到安装器"提示，以及升级逻辑分支（installer 走 installer_url）。
        渠道由 main.py 的 _detect_install_channel() 写入环境变量。"""

    return {"status": "ok", "channel": os.environ.get("WEBOT_INSTALL_CHANNEL", "zip")}
@int
def diagnostics_log(tail):
    """诊断日志：返回客户端日志文件尾部，供用户出错时一键复制发给技术支持。
        日志由 main.py 的 _setup_client_file_log() 写到 ~/.webot/logs/client.log。"""

    log_path = os.path.join(os.path.expanduser("~"), ".webot", "logs", "client.log")
    f = open(log_path, "r", encoding="utf-8", errors="replace")
    lines = f.readlines()
    None(None, None)
    tail = max(1, min(int(tail), 5000))
    content = lines(-tail, None)
    return {"status": "ok", "path": log_path, "lines": len(lines), "content": content}
    return {"status": "empty", "path": log_path, "content": "", "message": "暂无日志文件"}
diagnostics_log_open = app.post("/api/diagnostics/log/open")((lambda : {"status": "ok", "path": log_dir}))
@app.get("/")
def root():
    """提供前端入口页面"""

    return JSONResponse(status_code=200, content={"message": "WeRobotCore API Service is running", "mode": "Web-Enabled", "version": "1.0.0"})
    index_path = os.path.join(frontend_path, "index.html")
    return FileResponse(index_path)
@app.get("/config.json")
def get_config_json():
    """提供前端配置文件"""

    return JSONResponse(status_code=404, content={"error": "Config not found"})
    config_path = os.path.join(frontend_path, "config.json")
    return FileResponse(config_path)
@app.get("/api/agent/backend_status")
def get_backend_status():
    """获取后端全量运行状态信息"""

    yield None
class AgentReplySubmitRequest(BaseModel):
    """AgentReplySubmitRequest"""

    __annotations__["taskId"] = str
    __annotations__["action"] = str
    reply = None
    __annotations__["reply"] = Optional[str]
    reason = None
    __annotations__["reason"] = Optional[str]
log_dir = os.path.join(application_path, "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, "webot_error.log"), level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console_handler)
logging.info("程序开始启动...")
logging.info("Python 路径: ", f'{sys.executable}')
logging.info("当前工作目录: ", f'{os.getcwd()}')
wx = None
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
def is_uia_disconnected_error(error):
    """检查是否是 UIA 断开连接错误"""

    return isinstance(error, tuple)
    isinstance(error, Exception)
    return True
API_KEY = os.environ.get("WEBOT_API_KEY", "yoko_test")
@Request
def api_key_check_middleware(request, call_next):
    whitelist_prefixes = ("/docs", "/redoc", "/openapi.json", "/api/license", "/api/version", "/api/debug/instances", "/api/tasks/stats/today", "/api/guide/status", "/api/voice/preview/file/", "/api/voice/greeting/file/", "/api/health", "/api/diagnostics", "/api/system/install-channel", "/api/system/open-browser", "/mcp", "/js", "/css", "/img", "/icon", "/favicon.ico", "/config.json", "/ws")
    path = request.url.path
    yield None
    client_api_key = request.headers.get("X-API-Key")
    yield None
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"success": False, "message": "请携带可验证的X-API-Key", "code": "INVALID_API_KEY"})
    prefix = _
    yield None
    yield None
import requests
from cachetools import TTLCache
yoko_auth_cache = TTLCache(maxsize=100, ttl=900)
yoko_auth_fail_cache = TTLCache(maxsize=100, ttl=60)
def get_yoko_token():
    """
        获取 YokoAgent 凭证，提供鲁棒的降级读取策略
        """

    token = os.environ.get("YOKO_RPA_TOKEN")
    home_dir = str(Path.home())
    auth_file = os.path.join(home_dir, ".yokoagent", "auth.json")
    f = open(auth_file, "r", encoding="utf-8")
    data = json.load(f)
    data.get("token")(None, None, None)
    return "???"
    return token
def get_channel_id():
    """获取渠道ID，优先从命令行参数获取，其次从环境变量获取"""

    return os.environ.get("YOKO_CHANNEL_ID")
    idx = sys.argv.index("--channel-id")
    return sys.argv[idx + 1]
def verify_yoko_token(machine_code):
    token = get_yoko_token()
    cache_key = f'{machine_code}'
    api_base = os.environ.get("YOKO_API_BASE", "http://127.0.0.1:3000")
    headers = {"Bearer ": f'{token}'}
    channel_id = get_channel_id()
    resp = requests.post(f'{api_base}', "/v1/rpa/auth/verify", json={"machine_code": machine_code}, headers=headers, timeout=5)
    data = resp.json()
    f'{resp.status_code}'(", data: ", f'{data}')
    result = {"valid": "SERVER_ERROR", "error": "Server returned abnormal status: ", "message": f'{resp.status_code}'}
    yoko_auth_fail_cache[cache_key] = result
    return result
    result = {"valid": False, "error": data.get("error_code"), "message": data.get("message", "License validation failed")}
    yoko_auth_fail_cache[cache_key] = result
    return result
    del yoko_auth_cache[cache_key]
    result = {"valid": True, "expires_at": data["data"]["expires_at"]}
    yoko_auth_cache[cache_key] = result
    return result
    headers["X-Channel-ID"] = channel_id
    logging.info("RPA API Base: ", f'{api_base}')
    return yoko_auth_fail_cache[cache_key]
    return yoko_auth_cache[cache_key]
    return {"valid": False, "error": "NO_TOKEN"}
@app.middleware("http")
async def license_check_middleware(request, call_next):
    request.state.auth_type = "local_source"
    return await call_next(request)
@Request
def catch_exceptions_middleware(request, call_next):
    yield None
@Request
def add_cors_headers(request, call_next):
    yield None
EXTERNAL_API_WHITELIST = {"/api/test/external"}
@Request
def access_control(request, call_next):
    client_host = request.client.host
    is_local = client_host in ("127.0.0.1", "localhost")
    path = request.url.path
    path = request.url.path
    return JSONResponse(status_code=403, content={"error": "此接口仅允许本地访问"})
    yield None
    yield None
api_key_header = APIKeyHeader(name="X-API-Key")
def get_api_key(api_key):
    return api_key
    raise HTTPException(status_code=403, detail="无效的 API Key")
class MessageRequest(BaseModel):
    """MessageRequest"""

    model_config = ConfigDict(populate_by_name=True)
    __annotations__["user"] = str
    __annotations__["message"] = str
    quote_msg_id = None
    __annotations__["quote_msg_id"] = Optional[str]
    account_id = Field(None, alias="accountId")
    __annotations__["account_id"] = Optional[str]
class FileRequest(BaseModel):
    """FileRequest"""

    __annotations__["user"] = str
    __annotations__["file_path"] = str
class FilesRequest(BaseModel):
    """FilesRequest"""

    __annotations__["user"] = str
    __annotations__["file_path"] = Union[(str, List[str])]
class FriendRequest(BaseModel):
    """FriendRequest"""

    __annotations__["msg"] = str
    __annotations__["num_notes"] = Dict[(str, str)]
class KeywordsChatRequest(BaseModel):
    """KeywordsChatRequest"""

    __annotations__["user"] = str
    __annotations__["keywords"] = Dict[(str, str)]
class Agent(BaseModel):
    """Agent"""

    __annotations__["id"] = str
    __annotations__["name"] = str
    __annotations__["botId"] = str
    platform = "coze"
    __annotations__["platform"] = str
    apiUrl = None
    __annotations__["apiUrl"] = Optional[str]
    apiToken = None
    __annotations__["apiToken"] = Optional[str]
class AgentsConfig(BaseModel):
    """AgentsConfig"""

    __annotations__["agents"] = List[Agent]
class CozeTokenRequest(BaseModel):
    """CozeTokenRequest"""

    __annotations__["token"] = str
class LicenseRequest(BaseModel):
    """LicenseRequest"""

    __annotations__["machine_code"] = str
class ActivationRequest(BaseModel):
    """ActivationRequest"""

    __annotations__["activation_code"] = str
    __annotations__["machine_code"] = str
class GreetingConfig(BaseModel):
    """GreetingConfig"""

    __annotations__["name"] = str
    __annotations__["greetings"] = List[Dict[(str, Any)]]
class GreetingConfigRequest(BaseModel):
    """GreetingConfigRequest"""

    __annotations__["greeting_config"] = List[GreetingConfig]
class MassSendingRequest(BaseModel):
    """MassSendingRequest"""

    __annotations__["tagIds"] = List[str]
    __annotations__["selectedFriends"] = List[str]
    __annotations__["greetingGroupId"] = str
    __annotations__["timeType"] = str
    __annotations__["contentType"] = str
    __annotations__["agentId"] = str
    account_id = None
    __annotations__["account_id"] = Optional[str]
    dayOffset = 0
    __annotations__["dayOffset"] = Optional[int]
    time = None
    __annotations__["time"] = Optional[datetime]
    sendInterval = "10-30"
    __annotations__["sendInterval"] = Optional[str]
    autoGrouping = False
    __annotations__["autoGrouping"] = Optional[bool]
    batchSize = 10
    __annotations__["batchSize"] = Optional[int]
class TestAgentRequest(BaseModel):
    """TestAgentRequest"""

    __annotations__["agent_id"] = str
    __annotations__["platform"] = str
class AgentPostMomentRequest(BaseModel):
    """AgentPostMomentRequest"""

    material_folder = ""
    __annotations__["material_folder"] = str
    content = ""
    __annotations__["content"] = str
    files = None
    __annotations__["files"] = Optional[List[str]]
class AgentMassSendingRequest(BaseModel):
    """AgentMassSendingRequest"""

    tags = None
    __annotations__["tags"] = Optional[List[str]]
    targets = None
    __annotations__["targets"] = Optional[List[str]]
    __annotations__["greeting_group"] = str
    schedule_time = None
    __annotations__["schedule_time"] = Optional[str]
    batch_size = 10
    __annotations__["batch_size"] = int
    account_id = None
    __annotations__["account_id"] = Optional[str]
class ChatCollectionRequest(BaseModel):
    """ChatCollectionRequest"""

    __annotations__["agent_id"] = str
    max_sessions = 50
    __annotations__["max_sessions"] = Optional[int]
    time_limit_days = 2
    __annotations__["time_limit_days"] = Optional[int]
    file_types = ["image"]
    __annotations__["file_types"] = Optional[List[str]]
    session_name = None
    __annotations__["session_name"] = Optional[str]
    __annotations__["timeType"] = str
    time = None
    __annotations__["time"] = Optional[datetime]
    is_recurring = False
    __annotations__["is_recurring"] = Optional[bool]
    schedule_config = None
    __annotations__["schedule_config"] = Optional[Dict]
class InviteToGroupRequest(BaseModel):
    """InviteToGroupRequest"""

    __annotations__["friends"] = List[str]
    __annotations__["targetGroup"] = str
    __annotations__["account_id"] = str
class FriendRequestSettings(BaseModel):
    """FriendRequestSettings"""

    __annotations__["enabled"] = bool
    maxFriendsPerDay = 100
    __annotations__["maxFriendsPerDay"] = int
    checkInterval = 10
    __annotations__["checkInterval"] = int
    maxProcessPerTime = 5
    __annotations__["maxProcessPerTime"] = int
    targetGroup = None
    __annotations__["targetGroup"] = str
    tag = None
    __annotations__["tag"] = Optional[str]
    greetingGroupId = None
    __annotations__["greetingGroupId"] = Optional[str]
    multiCycleEnabled = False
    __annotations__["multiCycleEnabled"] = Optional[bool]
    accountIds = []
    __annotations__["accountIds"] = Optional[List[str]]
class AddFriendSettings(BaseModel):
    """AddFriendSettings"""

    __annotations__["enabled"] = bool
    maxFriendsPerDay = None
    __annotations__["maxFriendsPerDay"] = Optional[int]
    interval = None
    __annotations__["interval"] = Optional[int]
    batchSize = None
    __annotations__["batchSize"] = Optional[int]
    verifyMessage = None
    __annotations__["verifyMessage"] = Optional[str]
    multiCycleEnabled = False
    __annotations__["multiCycleEnabled"] = Optional[bool]
    accountIds = []
    __annotations__["accountIds"] = Optional[List[str]]
class AutoFollowRequest(BaseModel):
    """AutoFollowRequest"""

    __annotations__["account_id"] = str
    __annotations__["friend_wxid"] = str
    __annotations__["friend_nickname"] = str
    __annotations__["agent_id"] = str
    __annotations__["follow_scenario"] = str
    follow_days = 7
    __annotations__["follow_days"] = int
    follow_frequency = 1
    __annotations__["follow_frequency"] = Union[(str, int)]
    time_range_start = "09:00"
    __annotations__["time_range_start"] = str
    time_range_end = "18:00"
    __annotations__["time_range_end"] = str
    chat_type = "single"
    __annotations__["chat_type"] = str
class BatchAutoFollowRequest(BaseModel):
    """BatchAutoFollowRequest"""

    __annotations__["account_id"] = str
    __annotations__["friends"] = List[Dict[(str, str)]]
    __annotations__["agent_id"] = str
    __annotations__["follow_scenario"] = str
    follow_days = 7
    __annotations__["follow_days"] = int
    follow_frequency = 1
    __annotations__["follow_frequency"] = Union[(str, int)]
    time_range_start = "09:00"
    __annotations__["time_range_start"] = str
    time_range_end = "18:00"
    __annotations__["time_range_end"] = str
    first_run_next_day = False
    __annotations__["first_run_next_day"] = bool
class BatchCancelAutoFollowRequest(BaseModel):
    """BatchCancelAutoFollowRequest"""

    __annotations__["task_ids"] = List[str]
class BatchUpdateAutoFollowAgentRequest(BaseModel):
    """BatchUpdateAutoFollowAgentRequest"""

    __annotations__["task_ids"] = List[str]
    __annotations__["agent_id"] = str
class SyncContactsRequest(BaseModel):
    """SyncContactsRequest"""

    __annotations__["sync_items"] = List[str]
    sync_frequency = 5
    __annotations__["sync_frequency"] = int
    time_range_start = "02:00"
    __annotations__["time_range_start"] = str
    time_range_end = "04:00"
    __annotations__["time_range_end"] = str
    enabled = True
    __annotations__["enabled"] = bool
class UnbindRequest(BaseModel):
    """UnbindRequest"""

    __annotations__["activation_code"] = str
class UpdateRemarkRequest(BaseModel):
    """UpdateRemarkRequest"""

    __annotations__["code"] = str
    __annotations__["remark"] = str
class VersionCheckRequest(BaseModel):
    """VersionCheckRequest"""

    __annotations__["current_version"] = str
    __annotations__["agent_id"] = str
def safe_cleanup_temp_files(path):
    """安全清理临时文件"""

    shutil.rmtree(path, ignore_errors=True)
instance_manager_v2 = InstanceManagerV2()
@app.get("/api/agent/instances_status")
def get_agent_instances_status():
    """
        获取所有微信实例的状态，供Agent判断是否启动
        返回格式：
        [
            {
                "_initialized": bool,
                "account_info": { "nickname": str, "account_id": str }
            },
            ...
        ]
        """

    instances = instance_manager_v2.list_instances()
    result = []
    return result
    inst = instances
    initialized = inst.get("initialized", False)
    account_info = inst.get("account_info")
    safe_account_info = {"nickname": account_info.get("nickname"), "account_id": account_info.get("account_id")}
    result.append({"_initialized": initialized, "account_info": safe_account_info})
def initialize_scheduler_if_needed():
    """在用户登录后初始化调度器（如果尚未初始化）"""

    scheduler = get_scheduler()
    status = scheduler.get_status()
    from WeRobotCore.task_system_v3.permission_manager import PermissionManager
    permission_manager = PermissionManager()
    logging.info("开始初始化调度器...")
    yield None
    logging.info("调度器已处于运行状态: ", f'{status.state.value}')
    _scheduler_initialized = True
    return True
class MultiInstanceRequest(BaseModel):
    """MultiInstanceRequest"""

    timestamp = None
    __annotations__["timestamp"] = Optional[int]
class InstanceInfo(BaseModel):
    """InstanceInfo"""

    __annotations__["instance_id"] = str
    __annotations__["window_handle"] = int
    __annotations__["api_port"] = int
    nickname = None
    __annotations__["nickname"] = Optional[str]
    account_id = None
    __annotations__["account_id"] = Optional[str]
class FailedInstanceInfo(BaseModel):
    """FailedInstanceInfo"""

    __annotations__["instance_index"] = int
    __annotations__["window_handle"] = int
    __annotations__["reason"] = str
    __annotations__["description"] = str
class InitSummary(BaseModel):
    """InitSummary"""

    __annotations__["total"] = int
    __annotations__["success"] = int
    __annotations__["failed"] = int
class MultiInstanceResponse(BaseModel):
    """MultiInstanceResponse"""

    __annotations__["success"] = bool
    __annotations__["message"] = str
    instances = []
    __annotations__["instances"] = List[InstanceInfo]
    code = None
    __annotations__["code"] = Optional[str]
    error_detail = None
    __annotations__["error_detail"] = Optional[str]
    init_summary = None
    __annotations__["init_summary"] = Optional[InitSummary]
    failed_instances = None
    __annotations__["failed_instances"] = Optional[List[FailedInstanceInfo]]
    need_auto_config = None
    __annotations__["need_auto_config"] = Optional[bool]
    next_action = None
    __annotations__["next_action"] = Optional[dict]
def _ctrl_alt_w_wake():
    """模拟微信全局热键 Ctrl+Alt+W 唤出主窗口（用于把托盘里的微信弹出，避免直接 ShowWindow 白屏）。"""

    import ctypes
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    KEYEVENTF_KEYUP = 2
    VK_CONTROL = (17, 18, 87)[0]
    VK_MENU = (17, 18, 87)[1]
    VK_W = (17, 18, 87)[2]
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_MENU, 0, 0, 0)
    user32.keybd_event(VK_W, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_W, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
def _wake_wechat_window(hwnd):
    """把指定微信窗口唤起到前台。安全：仅对【隐藏/最小化】的窗口发 Ctrl+Alt+W，
        不会把已经显示的微信反而切掉（Ctrl+Alt+W 是 toggle）。供 initialize 时"按需拉前台"用。"""

    import win32gui
    import win32con
    hidden = win32gui.IsIconic(hwnd)
    _ctrl_alt_w_wake()
    time.sleep(0.5)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.SetForegroundWindow(hwnd)
@Security(get_api_key)
def initialize_multiple_wechat(request, api_key):
    """初始化所有微信实例并获取用户信息"""

    os.environ.pop("WEBOT_DEFER_WECHAT_ACTIVATION", None)
    from WeRobotCore.core.uia_logger import UiaLogger
    logger = UiaLogger(logger_name="api_server").get_logger()
    existing_instances = instance_manager_v2.list_instances()
    from WeRobotCore.core.version_detector import detect_wechat_build
    from WeRobotCore.core import wechat_version_policy
    from WeRobotCore.core import init_failure_record
    from WeRobotCore.utils.qt_accessibility import is_qt_accessibility_user_env_enabled
    env_already_configured = is_qt_accessibility_user_env_enabled()
    classifications = []
    detected_builds = []
    too_high = classifications
    c = []
    usable = classifications
    c = []
    instance_infos = []
    failed_infos = []
    failed_key_versions = {}
    failed_builds = []
    max_retries = 3
    env_error_detected = False
    env_error_message = None
    failed_account_keys = list(failed_key_versions.keys())
    "TOOL [实例初始化] 成功初始化 "(f'{len(instance_infos)}', " 个实例")
    active_instance = instance_manager_v2.get_active_instance()
    yield None
    window_handle = active_instance["window_handle"]
    wx = WeChat(window_handle=window_handle)
    wx.initialize_multi(window_handle, active_instance.get("account_info"))
    raise HTTPException(status_code=500, detail="未能成功初始化任何微信实例，请确保微信已登录")
    f = []
    env_resp = {"success": "ENV_NOT_CONFIGURED", "code": "设备环境未配置，请执行自动配置", "message": env_error_message, "error_detail": {"total": len(existing_instances), "success": 0, "failed": len(failed_infos)}, "init_summary": f, "failed_instances": failed_infos, "need_auto_config": True, "next_action": {"action": "auto_config", "endpoint": "POST /api/system/wechat41/auto_config", "required": True, "hint": "所有实例初始化失败，必须执行自动配置后重新登录微信"}}
    any_higher_than_recommended = any((b for b in _iter)(failed_builds))
    return env_resp
    view = wechat_version_policy.get_policy_view()
    env_resp["downgrade_suggestion"] = {"show": " 版本后重试。", "message": view["recommended"], "recommended_version": view["download_url"], "download_url": "下载微信 ", "download_label": f'{view["recommended"]}'}
    f = f'{view["recommended"]}'
    k = failed_key_versions.items()[0]
    ver = failed_key_versions.items()[1]
    init_failure_record.record_failure(k, ver)
    i = f.model_dump()[0]
    instance = f.model_dump()[1]
    f'{i + 1}'(" 个实例，窗口句柄: ", f'{instance["window_handle"]}')
    instance_success = False
    fail_reason = "INIT_FAILED"
    fail_desc = "初始化失败，请确保微信已登录"
    account_key = init_failure_record.resolve_account_key(instance)
    detected_ver = "unknown"
    failed_infos.append(FailedInstanceInfo(instance_index=i + 1, window_handle=instance["window_handle"], reason=fail_reason, description=fail_desc))
    failed_key_versions[account_key] = detected_ver
    failed_builds.append(None)
    retry = classifications[i]["detected"]
    window_handle = instance["window_handle"]
    wx_instance = WeChat(window_handle=window_handle)
    result = wx_instance.initialize_multi(window_handle, account_info=instance.get("account_info"))
    f'{instance["window_handle"]}'("，失败原因:", f'{result["error"]}')
    time.sleep(2)
    env_error_detected = True
    env_error_message = result.get("error")
    fail_reason = "ENV_NOT_CONFIGURED"
    fail_desc = "该微信账号首次在本设备托管，需执行一次自动配置"
    account_id = result["account_id"]
    nickname = result["nickname"]
    WeChat.update_account_handle_mapping(account_id, window_handle)
    instance_manager_v2.update_instance_account_info(instance["instance_id"], {"nickname": nickname, "account_id": account_id})
    instance_infos.append({"instance_id": instance["instance_id"], "window_handle": instance["window_handle"], "api_port": instance["api_port"], "nickname": nickname, "account_id": account_id})
    instance_success = True
    init_failure_record.record_success(account_id)
    c = too_high[0]
    " ~ "(f'{c["max"]}', "）")
    return {"success": f'{c["max"]}', "code": "，当前版本 ", "message": f'{c["detected"]}', "version_info": "。", "guidance": {"title": "下载受支持版本（推荐 ", "reason": f'{c["recommended"]}', "fix_steps": ["，最稳定）", "安装后重新登录微信，再启动 BOT 服务"], "download_url": c["download_url"], "download_label": "下载受支持的微信版本"}}
    c = " ~ "
    instance = c
    build = detect_wechat_build(instance.get("window_handle"))
    detected_builds.append(build)
    classifications.append(wechat_version_policy.classify_build(build))
    raise HTTPException(status_code=400, detail="未检测到任何微信实例，请确保微信已启动")
    _inst = f'{c["min"]}'
    _hwnd = _inst.get("window_handle")
    _wake_wechat_window(_hwnd)
from pydantic import BaseModel
class AutoConfigWechat41Request(BaseModel):
    """AutoConfigWechat41Request"""

    force_narrator = True
    __annotations__["force_narrator"] = bool
@Security(get_api_key)
def auto_config_wechat41(request, api_key):
    import os
    import asyncio
    import subprocess
    from silent_narrator import SilentNarrator
    force_narrator = True
    narrator_activated = False
    print("[AutoConfig] [INFO] 用户指定强制使用真实讲述人模式，跳过静默模式")
    ps_script = "\n        $ErrorActionPreference = 'Stop'\n        Write-Output '[Step 1/3] 正在关闭微信进程'\n        try { Stop-Process -Name WeChat -Force -ErrorAction SilentlyContinue } catch {}\n        try { Stop-Process -Name Weixin -Force -ErrorAction SilentlyContinue } catch {}\n        Start-Sleep -Seconds 2\n        Write-Output '[Step 1/3] 完成'\n\n        $current = (Get-ItemProperty -Path 'HKCU:\\Environment' -Name 'QT_ACCESSIBILITY' -ErrorAction SilentlyContinue).QT_ACCESSIBILITY\n        if ($current -eq '1') {\n          Write-Output '[Step 2/3] 已存在 QT_ACCESSIBILITY=1，跳过设置'\n        } else {\n          Write-Output '[Step 2/3] 正在设置环境变量 QT_ACCESSIBILITY=1'\n          try { \n            Set-ItemProperty -Path 'HKCU:\\Environment' -Name 'QT_ACCESSIBILITY' -Value '1'\n          } catch { throw \"设置环境变量失败: $($_.Exception.Message)\" }\n        }\n        \n        # 确保当前 PowerShell 进程也被修改，这样 Start-Process 启动微信时才能正确继承该变量！\n        $env:QT_ACCESSIBILITY = '1'\n        Write-Output '[Step 2/3] 完成'\n\n        __FALLBACK_NARRATOR__\n\n        Write-Output '[Step 3/3] 正在查找微信安装路径并启动'\n        $wechat = $null\n        $env_path = '__WECHAT_EXEC_PATH__'\n        if ($env_path -ne '' -and (Test-Path $env_path)) {\n          $wechat = $env_path\n          Write-Output \"使用预设微信路径: $wechat\"\n        }\n        if (-not $wechat) {\n          $candidates = @(\n            \"$env:ProgramFiles\\Tencent\\Weixin\\Weixin.exe\",\n            \"$env:ProgramFiles(x86)\\Tencent\\Weixin\\Weixin.exe\",\n            \"$env:LOCALAPPDATA\\Tencent\\Weixin\\Weixin.exe\"\n          )\n          foreach ($c in $candidates) { if (Test-Path $c) { $wechat = $c; break } }\n        }\n        if (-not $wechat) {\n          $roots = @(\"$env:ProgramFiles\\Tencent\", \"$env:ProgramFiles(x86)\\Tencent\", \"$env:LOCALAPPDATA\\Tencent\")\n          foreach ($root in $roots) {\n            try {\n              $found = Get-ChildItem -Path $root -Filter 'Weixin.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1\n              if ($found) { $wechat = $found.FullName; break }\n            } catch {}\n          }\n        }\n        if (-not $wechat) {\n          Write-Output '[Step 3/3] 未找到微信路径，跳过启动'\n        } else {\n          Write-Output ('已找到微信路径: ' + $wechat)\n          Start-Process -FilePath $wechat\n          Write-Output '[Step 3/3] 完成'\n        }\n        Write-Output 'OK'\n        "
    fallback_str = ""
    ps_script = ps_script.replace("__FALLBACK_NARRATOR__", fallback_str)
    wechat_exec_path = os.environ.get("WECHAT_EXEC_PATH", "")
    ps_script = ps_script.replace("__WECHAT_EXEC_PATH__", wechat_exec_path.replace("'", "''"))
    yield None
    fallback_str = "\n        $nvdaRunning = ($null -ne (Get-Process -Name nvda -ErrorAction SilentlyContinue))\n        $narratorExists = Test-Path 'C:\\Windows\\System32\\Narrator.exe'\n\n        if ($narratorExists) {\n            Write-Output '[Fallback] 正在启动讲述人...'\n            Start-Process -FilePath 'C:\\Windows\\System32\\Narrator.exe'\n            Start-Sleep -Seconds 8\n            Write-Output '[Fallback] 讲述人已启动'\n        } elseif ($nvdaRunning) {\n            Write-Output '[Fallback] 检测到 NVDA 正在运行，使用 NVDA 模式'\n        } else {\n            Write-Output '__NO_SCREEN_READER__'\n            exit 1\n        }\n        "
    narrator_activated = SilentNarrator.activate()
    print("[AutoConfig] [WARN] 静默讲述人激活失败，将在 PowerShell 步骤中启动真实 Narrator")
    print("[AutoConfig] OK! 静默讲述人已激活（无需启动 Narrator.exe）")
@Security(get_api_key)
def stop_narrator(api_key):
    import threading
    time = time
    from silent_narrator import SilentNarrator
    def _stop():
        import subprocess
        subprocess.run([], ("taskkill", "/F", "/IM", "Narrator.exe"), capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    threading.Thread(target=_stop, daemon=True).start()
    return {"success": True, "message": "已触发退出讲述人"}
    def _delayed_deactivate():
        time.sleep(2)
        SilentNarrator.deactivate()
        import subprocess
        subprocess.run([], ("taskkill", "/F", "/IM", "Narrator.exe"), capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    threading.Thread(target=_delayed_deactivate, daemon=True).start()
def _find_wechat_exe():
    """查找微信可执行文件路径"""

    path = os.environ.get("WECHAT_EXEC_PATH", "")
    pf = os.environ.get("ProgramFiles", "C:\\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
    local = os.environ.get("LOCALAPPDATA", "")
    candidates = [os.path.join(pf, "Tencent", "Weixin", "Weixin.exe"), os.path.join(pf86, "Tencent", "Weixin", "Weixin.exe"), os.path.join(local, "Tencent", "Weixin", "Weixin.exe"), os.path.join(pf, "Tencent", "WeChat", "WeChat.exe"), os.path.join(pf86, "Tencent", "WeChat", "WeChat.exe")]
    return ""
    c = candidates
    return "???"
    return path
class LaunchWechatRequest(BaseModel):
    """LaunchWechatRequest"""

    count = 1
    __annotations__["count"] = int
    close_existing = True
    __annotations__["close_existing"] = bool
    enable_narrator = False
    __annotations__["enable_narrator"] = bool
@Security(get_api_key)
def launch_wechat(request, api_key):
    """
        启动微信进程（支持多开，Agent 友好）

        - count: 要启动的微信数量（默认 1）
        - close_existing: 启动前是否关闭已有微信进程（默认 true，多开必须关闭）
        - enable_narrator: 是否在启动前激活辅助功能（首次配置场景）
        """

    import psutil as _psutil
    import subprocess
    count = max(1, min(1, 10))
    close_existing = True
    enable_narrator = False
    closed_count = 0
    wechat_path = _find_wechat_exe()
    wechat_dir = os.path.dirname(wechat_path)
    launched = 0
    return {"status": "已启动 ", "launched_count": f'{launched}', "closed_count": " 个微信进程", "enable_narrator": f'{""}', "message": "，请登录后调用初始化接口", "next_action": {"action": "wait_user_login_then_init", "endpoint": "POST /api/init/multi", "hint": "用户完成微信扫码/登录后调用此接口初始化所有实例。如果响应中 need_auto_config=true，则需再调用 POST /api/system/wechat41/auto_config"}}
    return {"status": "error", "code": "LAUNCH_FAILED", "message": "启动微信失败", "next_action": {"action": "manual_launch", "hint": "请手动启动微信"}}
    i = "（已启用辅助配置模式）"
    subprocess.Popen([wechat_path], cwd=wechat_dir)
    launched = launched + 1
    yield None
    return {"status": "error", "code": "WECHAT_PATH_NOT_FOUND", "message": "未找到微信安装路径，请先手动启动一次微信以便系统记录安装位置", "next_action": {"action": "manual_launch", "hint": "用户手动打开微信后，系统会自动记录路径，再次调用此接口即可"}}
    from silent_narrator import SilentNarrator
    activated = SilentNarrator.activate()
    subprocess.Popen(["Narrator.exe"])
    yield None
    yield None
    proc = _
    name = proc.info.get("name")
    proc.kill()
    closed_count = closed_count + 1
    asyncio.sleep(1.5)
@Security(get_api_key)
def get_system_capabilities(api_key):
    """
        获取系统能力描述（Agent 发现入口）

        返回当前状态、可用能力列表及建议的下一步操作，
        供 Agent 自主推进工作流时参考。
        """

    from WeRobotCore import __version__
    instances = instance_manager_v2.list_instances()
    initialized = instances
    i = []
    state = "no_wechat"
    capabilities = [{"action": "launch_wechat", "endpoint": "POST /api/system/wechat/launch", "description": "启动微信进程，支持多开（count）和辅助配置模式（enable_narrator）", "always_available": True, "params": {"count": "integer, 要启动的实例数，默认 1", "close_existing": "boolean, 启动前关闭已有微信，默认 true（多开必须为 true）", "enable_narrator": "boolean, 启用辅助功能（首次配置场景），默认 false"}}, {"action": "init_instances", "endpoint": "POST /api/init/multi", "description": "初始化所有已运行的微信实例。响应中 need_auto_config=true 时部分实例需要首次配置，failed_instances 列表说明了哪些实例失败及原因", "available": bool(instances), "reason": "需要先调用 launch_wechat 启动微信进程"}, {"action": "auto_config", "endpoint": "POST /api/system/wechat41/auto_config", "description": "对首次在本设备托管的微信账号执行环境配置（自动完成：关闭微信→启用讲述人→重启微信）。完成后用户需重新登录，再调用 init_instances", "always_available": True, "note": "等效于调用 launch_wechat 时传 enable_narrator=true，但会自动处理所有步骤"}, {"action": "get_instances", "endpoint": "GET /api/instances", "description": "获取所有微信实例状态，可轮询确认微信进程存活及初始化情况", "always_available": True}]
    next_action = None
    return {"service": "yokowebot", "version": _ver, "current_state": state, "instances_total": len(instances), "instances_initialized": len(initialized), "capabilities": capabilities, "next_action": next_action}
    next_action = {"action": "init_instances", "endpoint": "POST /api/init/multi", "hint": "检测到微信进程但未初始化，引导用户登录后调用初始化接口"}
    next_action = {"action": "launch_wechat", "endpoint": "POST /api/system/wechat/launch", "hint": "未检测到微信进程，请先启动微信"}
    state = "wechat_detected_not_initialized"
    state = "ready"
    i = None
@Security(get_api_key)
def get_all_instances(api_key):
    """获取所有微信实例信息。

        附加字段：
        - wechat_build  4 元数组，如 [4, 1, 9, 57]；探测失败为 None
        - wechat_version  与 build 同源的字符串 "4.1.9.57"；探测失败为 None
        前端用这两个字段判断该实例是否支持 4.1.9+ 的能力（如 AI 语音回复）。
        """

    from WeRobotCore.core.version_detector import detect_wechat_build, format_build
    instances = instance_manager_v2.list_instances()
    return {"success": True, "instances": instances}
    inst = instances
    hwnd = inst.get("window_handle")
    build = None
    inst["wechat_build"] = None
    inst["wechat_version"] = None
    build = detect_wechat_build(hwnd)
@app.get("/api/debug/instances")
def debug_instances():
    """【调试接口】查看共享内存中的完整实例状态及窗口句柄实时信息（无需 API Key）"""

    import win32gui as _w32
    import psutil as _ps
    raw_instances = instance_manager_v2._read_from_shared_memory()
    result = []
    return {"success": True, "active_instance_id": raw_instances.get("active_instance"), "total": len(result), "instances": result}
    iid = raw_instances.get("instances", {}).items()[0]
    inst = raw_instances.get("instances", {}).items()[1]
    hwnd = inst.get("window_handle")
    pid = inst.get("process_id")
    is_win = False
    win_title = ""
    win_class = ""
    proc_name = ""
    proc_alive = False
    p = _ps.Process(pid)
    proc_name = p.name()
    proc_alive = p.is_running()
    result.append({"instance_id": iid, "window_handle": hwnd, "win_IsWindow": is_win, "win_title": win_title, "win_class": win_class, "process_id": pid, "proc_name": proc_name, "proc_alive": proc_alive, "initialized": inst.get("initialized"), "account_info": inst.get("account_info"), "is_active": iid == raw_instances.get("active_instance")})
    win_title = _w32.GetWindowText(hwnd)
    win_class = _w32.GetClassName(hwnd)
@Security(get_api_key)
def get_active_instances(api_key):
    """获取所有活跃且已初始化的微信实例"""

    instances = instance_manager_v2.list_instances()
    active_instances = []
    return {"success": True, "instances": active_instances}
    instance = instances
    account_info = instance.get("account_info", {})
    active_instances.append({"instance_id": instance["instance_id"], "nickname": account_info["nickname"], "account_id": account_info["account_id"], "is_active": instance.get("is_active", False)})
@Security(get_api_key)
def exit_instance_management(instance_id, api_key):
    """将指定微信实例标记为主动退出托管，停止所有自动化任务"""

    success = instance_manager_v2.exit_instance(instance_id)
    from WeRobotCore.task_system_v2.multi_chat_monitor import multi_chat_monitor
    instance_info = instance_manager_v2.get_instance_info(instance_id)
    return {"success": True, "message": "已退出托管，该实例将不再执行自动化任务"}
    account_info = instance_info.get("account_info", {})
    account_id = None
    yield None
    raise HTTPException(status_code=404, detail="未找到指定实例")
@Security(get_api_key)
def switch_active_instance(instance_id, api_key):
    """切换当前活动的微信实例"""

    result = instance_manager_v2.switch_active_instance(instance_id)
    active_instance = instance_manager_v2.get_active_instance()
    window_handle = active_instance["window_handle"]
    wx = WeChat(window_handle=window_handle)
    print("TOOL [实例切换] 使用窗口句柄获取实例 - 句柄: ", f'{window_handle}')
    account_info = active_instance.get("account_info", {})
    account_id = account_info.get("account_id", "")
    friend_count = 0
    group_count = 0
    return {"success": True, "message": "切换实例成功", "instance": {"instance_id": active_instance["instance_id"], "nickname": account_info.get("nickname", ""), "account_id": account_id, "friend_count": friend_count, "group_count": group_count}}
    from WeRobotCore.core.db_manager import WeChatDBManager
    db_manager = WeChatDBManager()
    counts = db_manager.get_contact_counts(account_id)
    friend_count = counts.get("friend_count", 0)
    group_count = counts.get("group_count", 0)
    init_result = wx.initialize_multi(window_handle, account_info)
    new_account_info = {"nickname": init_result["nickname"], "account_id": init_result["account_id"]}
    WeChat.update_account_handle_mapping(new_account_info["account_id"], window_handle)
    instance_manager_v2.update_instance_account_info(instance_id, new_account_info)
    account_info = new_account_info
    raise HTTPException(status_code=500, detail="切换实例后初始化失败")
    print("获取活动实例信息失败")
    raise HTTPException(status_code=500, detail="获取活动实例信息失败")
    raise 404("实例 ", status_code=f'{instance_id}', detail=" 不存在")
version_manager = VersionManager()
@app.get("/api/version/info")
def get_version_info():
    """获取后端服务当前版本号"""

    from WeRobotCore import __version__
    return {"success": True, "version": __version__}
@VersionCheckRequest
def check_version(request):
    """检查是否有新版本"""

    yield None
@VersionCheckRequest
def download_update(request):
    """下载并应用更新"""

    yield None
@app.get("/api/license/info")
def get_license_info():
    """获取本机授权信息"""

    yield None
@UnbindRequest
def unbind_license(request):
    """解绑授权"""

    machine_code = license_manager.get_machine_code()
    supabase = SupabaseManager()
    yield None
def _handle_agent_command(websocket, command_id, correlation_id, command, params):
    """处理 Agent 通过 WebSocket 发来的指令，回复 command_result"""

    def reply(success, result, error):
        yield None
    yield None
    from WeRobotCore.core.instance_manager_v3 import InstanceManagerV3
    mgr = InstanceManagerV3()
    instances = []
    accounts = []
    yield None
    inst = _
    info = {}
    accounts.append({"accountId": info.get("account_id", ""), "nickname": info.get("nickname", ""), "status": "unknown"})
    scheduler = get_scheduler()
    active = {}
    task_list = []
    yield None
    tid = _[0]
    ctx = _[1]
    task_list.append({"taskId": tid, "taskType": str(getattr(ctx, "task_type", "")), "status": "running"})
    task_id = params.get("taskId", "")
    found = False
    from WeRobotCore.task_system_v3.unified_manager_pattern import GlobalManagerRegistry
    auto_reply_mgr = GlobalManagerRegistry.get_manager("auto_reply_manager")
    yield None
    yield None
    task = auto_reply_mgr.get_task(task_id)
    task.confirm_reply("reject", None)
    found = True
    task_id = params.get("taskId", "")
    final_content = params.get("content", None)
    found = False
    from WeRobotCore.task_system_v3.unified_manager_pattern import GlobalManagerRegistry
    auto_reply_mgr = GlobalManagerRegistry.get_manager("auto_reply_manager")
    yield None
    yield None
    task = auto_reply_mgr.get_task(task_id)
    task.confirm_reply("approve", final_content)
    found = True
    task_id = params.get("taskId", "")
    delay = params.get("delaySeconds", 0)
    yield None
    task_id = params.get("taskId", "")
    scheduler = get_scheduler()
    yield None
@WebSocket
def websocket_endpoint(websocket):
    yield None
@Security(get_api_key)
def get_monitor_status(api_key):
    """获取会话监控状态"""

    multi_monitor = get_multi_chat_monitor()
    status = multi_monitor.get_monitor_status()
    manual_review_enabled = multi_monitor.get_manual_review_enabled()
    return {"success": True, "data": {"running": status.get("running", False), "total_monitors": status.get("total_monitors", 0), "manual_review_enabled": manual_review_enabled, "monitors": status.get("monitors", {})}}
@Security(get_api_key)
def update_manual_review_status(request, api_key):
    """更新人工复核状态"""

    yield None
@app.get("/api/connection/status")
def check_connection_status():
    """检查微信连接状态"""

    active_instance = instance_manager_v2.get_active_instance()
    wx = WeChat()
    status = wx.check_connection_status()
    return status
    return {"success": True, "connected": False, "reason": "微信实例正在初始化中"}
    return {"success": True, "connected": False, "reason": "该实例已退出托管"}
reconnect_wechat = app.post("/api/reconnect")((lambda instance_id: {"success": False, "error": "未找到可用的微信实例，请确认微信已登录后刷新页面重试"}))
@Request
def add_process_time_header(request, call_next):
    start_time = time.time()
    yield None
@ActivationRequest
def activate_license(request):
    """激活授权"""

    yield None
@app.get("/api/license/verify")
def verify_license():
    """验证授权状态"""

    is_agent_mode = "--no-ui" in sys.argv
    yield None
    machine_code = license_manager.get_machine_code()
    yoko_auth = verify_yoko_token(machine_code)
    return JSONResponse(content={"valid": True, "message": "验证通过(Yoko)", "data": {"machine_code": machine_code, "expires_at": yoko_auth.get("expires_at"), "license_type": "yoko_seat"}})
@app.get("/api/license/machine-code")
def get_machine_code():
    """获取设备机器码"""

    machine_code = license_manager.get_machine_code()
    return {"machine_code": machine_code}
    raise HTTPException(status_code=500, detail="获取机器码失败")
@app.get("/api/mcp/token")
def get_mcp_pairing_info():
    """返回本机 MCP 端点地址与 pairing token，供本地 Agent 写入宿主 mcp.json。

        - 仅在 MCP 启用时有效（_mcp 版 exe，或设置了 YOKO_MCP_ENABLED=1）；否则 404。
        - 需携带 X-API-Key（localhost 内部调用；未加入 api_key 豁免名单）。
        - 已加入 license 豁免名单：未激活时也可预取以便先配置好 mcp.json（token 本身不含激活信息）。
        - token 是本地随机密钥，不等于激活码。
        """

    mcp_enabled = os.environ.get("YOKO_MCP_ENABLED") == "1"
    from mcp_gateway import get_pairing_token, get_mcp_endpoint, get_server_name
    return {"success": True, "endpoint": get_mcp_endpoint(), "token": get_pairing_token(), "server_name": get_server_name(), "transport": "streamable-http", "auth_header": "Authorization: Bearer <token>"}
    return JSONResponse(status_code=404, content={"success": False, "code": "MCP_DISABLED", "message": "本服务未启用 MCP 端点（当前非 _mcp 版，且未设置 YOKO_MCP_ENABLED=1）。"})
@app.get("/api/config/{config_type}")
def get_config(config_type):
    """获取指定类型的配置"""

    config = get_config_manager().load_config(config_type)
    return {"success": True, "data": config}
    return {"success": True, "data": config}
    return {"success": True, "data": config.get("agents", [])}
upload_file = app.post("/api/file/upload")((lambda file, api_key: {"success": True, "data": {"filename": file.filename, "filepath": save_path}}))
file_library_list = app.get("/api/file_library/list")((lambda api_key: {"success": True, "data": files}))
file_library_upload = app.post("/api/file_library/upload")((lambda file, key, description, api_key: {"success": True, "data": entry}))
file_library_delete = app.delete("/api/file_library/{key}")((lambda key, api_key: {"success": "未找到标识: ", "error": f'{key}'}))
file_library_check = app.get("/api/file_library/check")((lambda key, api_key: {"success": True, "exists": exists}))
api_list_moment_plans = app.get("/api/moment-material/plans")((lambda api_key: {"success": True, "plans": plans, "base": base}))
api_create_moment_folder = app.post("/api/moment-material/create-folder")((lambda item, api_key: {"success": False, "error": "Plan name is required"}))
api_list_moment_groups = app.get("/api/moment-material/groups")((lambda plan_name, api_key: {"success": True, "groups": groups}))
api_select_moment_folder_and_groups = app.get("/api/moment-material/select-folder")((lambda api_key: result))
api_open_folder = app.get("/api/moment-material/open-folder")((lambda path, api_key: open_folder(path)))
toggle_auto_comment = app.post("/api/moment/toggle-auto-comment")((lambda settings, api_key: JSONResponse(status_code=400, content={"success": False, "error": "开启任务失败：缺少必传参数 interactionMode 或 agentId，且未找到历史配置"})))
create_moment_post_task = app.post("/api/moment/post-task")((lambda settings, api_key: {"success": True, "task_ids": result.get("task_ids", [])}))
list_moment_post_tasks = app.get("/api/moment/post-tasks")((lambda api_key: result))
cancel_moment_post_task = app.post("/api/moment/post-task/cancel")((lambda task_id, api_key: result))
get_moment_post_logs = app.get("/api/moment/post-logs")((lambda api_key: {"success": True, "logs": logs}))
get_moment_interactions = app.get("/api/moment/interactions")((lambda : {"success": True, "data": logs}))
save_config = app.post("/api/config/{config_type}")((lambda config_type, config: {"success": "无法保存账号级配置「", "code": f'{config_type}', "error": "」：当前没有活跃的微信实例（未登录/未初始化）。请先登录并初始化微信后重试，避免配置被写到全局而界面看不到。"}))
voice_get_config = app.get("/api/voice/config")((lambda : {"success": True, "data": load_voice_settings_masked()}))
voice_save_config = app.post("/api/voice/config")((lambda config: {"success": True, "data": load_voice_settings_masked()}))
voice_test_connection = app.post("/api/voice/test")((lambda : {"success": False, "error": "未配置语音服务或 provider 未知"}))
voice_list_voices = app.get("/api/voice/voices")((lambda : {"success": True, "data": []}))
voice_compliance_agree = app.post("/api/voice/compliance/agree")((lambda : {"success": True}))
voice_library_list = app.get("/api/voice/library")((lambda : {"success": True, "data": voice_library.list_voices()}))
voice_library_add = app.post("/api/voice/library/add")((lambda payload: {"success": False, "error": "voice_id 不能为空"}))
voice_library_validate = app.post("/api/voice/library/validate")((lambda payload: {"success": False, "error": "未配置语音服务"}))
voice_library_delete = app.delete("/api/voice/library/{voice_id}")((lambda voice_id: {"success": ok}))
voice_preview = app.post("/api/voice/preview")((lambda payload: {"success": False, "error": "text 不能为空"}))
voice_audio_devices = app.get("/api/voice/audio_devices")((lambda : {"success": True, "data": check_environment()}))
voice_preview_file = app.get("/api/voice/preview/file/{filename}")((lambda filename: FileResponse(str(p), media_type="audio/mpeg", filename=filename, headers={"Cache-Control": "no-cache"})))
_voice_greeting_response = (lambda filename, abspath, duration_sec: {"success": {"filename": str(abspath), "audio_path": round(duration_sec, 2), "duration_sec": "/api/voice/greeting/file/", "url": f'{filename}'}, "data": extras})
voice_greeting_from_tts = app.post("/api/voice/greeting/from_tts")((lambda payload: {"success": False, "error": "text 不能为空"}))
voice_greeting_upload = app.post("/api/voice/greeting/upload")((lambda audio, display_name: {"success": f'{ext}', "error": "（支持 mp3/wav/m4a/aac/ogg）"}))
voice_greeting_record = app.post("/api/voice/greeting/record")((lambda audio, display_name: {"success": False, "error": "录音文件不能超过 5MB"}))
voice_greeting_delete = app.delete("/api/voice/greeting/{filename}")((lambda filename: {"success": ok}))
voice_greeting_file = app.get("/api/voice/greeting/file/{filename}")((lambda filename: FileResponse(str(p), media_type="audio/mpeg", filename=filename, headers={"Cache-Control": "no-cache"})))
create_auto_reply_task = app.post("/api/v2/tasks/auto-reply")((lambda request: {"success": True, "taskId": task_id, "message": "task_created"}))
confirm_auto_reply = app.post("/api/v2/tasks/auto-reply/confirm")((lambda request: {"success": False, "error": "缺少必要参数"}))
stop_chat_monitor = app.post("/api/chat/monitor/stop")((lambda api_key: {"status": "success", "message": "多实例会话监控已停止"}))
start_multi_chat_monitor = app.post("/api/chat/multi-monitor/start")((lambda request, api_key: {"status": "error", "code": "NO_INSTANCES", "message": "没有找到有效的微信实例，请先启动微信"}))
_worker_heartbeat_task = None
_worker_heartbeat_loop = (lambda : "???")
_hot_attach_init_worker = (lambda hot_instances: results)
_hot_attach_init_loop = (lambda : ...)
startup_event = app.on_event("startup")((lambda : ...))
shutdown_event = app.on_event("shutdown")((lambda : ...))
pause_mass_sending_task = app.post("/api/tasks/mass-sending/{task_id}/pause")((lambda task_id, api_key: result))
resume_mass_sending_task = app.post("/api/tasks/mass-sending/{task_id}/resume")((lambda task_id, api_key: result))
cancel_mass_sending_task = app.post("/api/tasks/mass-sending/{task_id}/cancel")((lambda task_id, api_key: result))
list_mass_sending_campaigns = app.get("/api/tasks/mass-sending/campaigns")((lambda include_terminal, api_key: {"success": True, "campaigns": campaigns}))
get_mass_sending_campaign = app.get("/api/tasks/mass-sending/campaigns/{campaign_id}")((lambda campaign_id, api_key: result))
resume_mass_sending_campaign = app.post("/api/tasks/mass-sending/campaigns/{campaign_id}/resume")((lambda campaign_id, api_key: result))
cancel_mass_sending_campaign = app.post("/api/tasks/mass-sending/campaigns/{campaign_id}/cancel")((lambda campaign_id, api_key: result))
cancel_all_mass_sending_tasks = app.post("/api/tasks/mass-sending/cancel-all")((lambda api_key: result))
create_mass_sending_task = app.post("/api/tasks/mass-sending")((lambda request, api_key: JSONResponse(content=result)))
create_chat_collection_task = app.post("/api/tasks/chat-collection")((lambda request, api_key: JSONResponse(content={"success": False, "message": "聊天采集任务暂不可用"})))
get_chat_collection_tasks = app.get("/api/tasks/chat-collection")((lambda api_key: JSONResponse(content={"success": False, "message": "聊天采集任务暂不可用"})))
cancel_chat_collection_task = app.post("/api/tasks/chat-collection/{task_id}/cancel")((lambda task_id, api_key: JSONResponse(content={"success": False, "message": "聊天采集任务暂不可用"})))
get_mass_sending_tasks = app.get("/api/tasks/mass-sending")((lambda api_key: {"success": True, "data": {"running": running_tasks, "pending": pending_tasks}}))
pause_all_mass_sending_tasks = app.post("/api/tasks/mass-sending/pause-all")((lambda api_key: JSONResponse(content=result)))
pause_mass_sending_task = app.post("/api/tasks/mass-sending/{task_id}/pause")((lambda task_id, api_key: JSONResponse(content=result)))
resume_mass_sending_task = app.post("/api/tasks/mass-sending/{task_id}/resume")((lambda task_id, api_key: JSONResponse(content=result)))
get_today_task_stats = app.get("/api/tasks/stats/today")((lambda account_id: {"success": True, "data": stats}))
get_task_logs = app.get("/api/tasks/logs")((lambda api_key: {"success": True, "data": logs}))
get_chat_collection_logs = app.get("/api/chat-collection/logs")((lambda api_key: {"success": True, "data": logs}))
get_friend_list = app.get("/api/friend/list")((lambda status, tag, api_key: {"success": True, "data": friend_list}))
delete_friend_from_list = app.delete("/api/friend/list/{wxid}")((lambda wxid, api_key: {"success": success}))
BatchDeleteRequest = __build_class__((lambda : ...), "BatchDeleteRequest", BaseModel)
batch_delete_friend_list = app.post("/api/friend/list/batch_delete")((lambda request, api_key: {"success": ok}))
toggle_auto_add_friend_task = app.post("/api/friend/auto-add-new/toggle")((lambda settings, api_key: JSONResponse(status_code=500, content={"success": False, "error": "自动添加好友管理器未初始化"})))
import_friend_list = app.post("/api/friend/import")((lambda file: {"success": True, "count": len(friend_list), "remaining": pending_count}))
import_friend_list_by_agent = app.post("/api/friend/import-by-agent")((lambda request: {"success": True, "count": len(friend_list), "remaining": pending_count}))
sync_friend_list_by_api = app.post("/api/friend/sync-by-api")((lambda api_key: {"success": pending_count, "count": "成功同步 ", "remaining": f'{count}', "message": " 条好友数据"}))
get_remaining_friend_count = app.get("/api/friend/remaining-count")((lambda api_key: {"success": True, "data": {"remaining": count, "today_added": today_count}}))
download_friend_list_template = app.get("/api/file/template/friend-list")((lambda : FileResponse(template_path, filename="好友导入模板.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")))
export_friend_list = app.get("/api/friend/list/export")((lambda status, tag, api_key: FileResponse(path, filename=os.path.basename(path), media_type="text/csv")))
export_friend_list_path = app.get("/api/friend/list/export_path")((lambda status, tag, api_key: {"success": True, "path": path}))
get_add_friend_logs = app.get("/api/friend/add-logs")((lambda api_key: {"success": True, "data": logs}))
toggle_friend_request_task = app.post("/api/tasks/friend-request/toggle")((lambda settings, api_key: True(result.get("task_id"), content={"success": "pending", "data": {"task_id": "cancelled", "status": result["message"], "message": task_params, "params": None}})))
get_friend_request_logs = app.get("/api/tasks/friend-request/logs")((lambda api_key: {"success": True, "data": logs}))
get_friend_request_risk_records = app.get("/api/tasks/friend-request/risk-records")((lambda api_key: {"success": True, "data": records}))
create_auto_follow_task = app.post("/api/tasks/auto-follow")((lambda request, api_key: result))
create_batch_auto_follow_task = app.post("/api/tasks/auto-follow/batch")((lambda request, api_key: result))
cancel_auto_follow_task = app.post("/api/tasks/auto-follow/{task_id}/cancel")((lambda task_id, api_key: result))
pause_auto_follow_task = app.post("/api/tasks/auto-follow/{task_id}/pause")((lambda task_id, api_key: result))
resume_auto_follow_task = app.post("/api/tasks/auto-follow/{task_id}/resume")((lambda task_id, api_key: result))
get_auto_follow_tasks = app.get("/api/tasks/auto-follow")((lambda api_key: result))
get_auto_follow_logs = app.get("/api/tasks/auto-follow/logs")((lambda api_key: result))
get_auto_follow_tasks_by_start_date = app.get("/api/tasks/auto-follow/by-start-date")((lambda date, agent_id, api_key: result))
get_auto_follow_task_info = app.get("/api/tasks/auto-follow/{task_id}")((lambda task_id, api_key: result))
api_batch_cancel_auto_follow_tasks = app.post("/api/tasks/auto-follow/batch-cancel")((lambda request, api_key: result))
api_batch_update_auto_follow_agent = app.post("/api/tasks/auto-follow/batch-update-agent")((lambda request, api_key: result))
get_group_members = app.get("/api/contacts/group/{group_name}/members")((lambda group_name: {"members": members}))
sync_group_members = app.post("/api/contacts/group/{group_name}/sync")((lambda group_name: {"success": True, "members": members}))
get_history_sessions = app.get("/api/chat/history_sessions")((lambda api_key: all_sessions))
UnsuspendSessionRequest = __build_class__((lambda : ...), "UnsuspendSessionRequest", BaseModel)
get_suspended_sessions = app.get("/api/chat/suspended_sessions")((lambda api_key: []))
unsuspend_session = app.post("/api/chat/unsuspend_session")((lambda request, api_key: {"success": False, "error": "自动回复管理器未初始化"}))
get_history_messages = app.get("/api/chat/history_messages/{session_id}")((lambda session_id, account_id, api_key: result))
DeleteHistorySessionRequest = __build_class__((lambda : ...), "DeleteHistorySessionRequest", BaseModel)
delete_history_session = app.post("/api/chat/delete_history_session")((lambda request, api_key: result))
send_message = app.post("/api/chat/send_message")((lambda request, api_key: {"status": result.get("success", False), "message": result.get("message", "消息发送成功"), "data": {"messages": result.get("messages", [])}}))
AgentSendFileRequest = __build_class__((lambda : ...), "AgentSendFileRequest", BaseModel)
AgentSendVoiceRequest = __build_class__((lambda : ...), "AgentSendVoiceRequest", BaseModel)
agent_reply_submit = app.post("/api/agent/reply/submit")((lambda body, api_key: _))
agent_reply_queue = app.get("/api/agent/reply/queue")((lambda accountId, api_key: agent_api.get_agent_reply_queue(account_id=accountId)))
agent_send_file = app.post("/api/agent/chat/send_file")((lambda request, api_key: {"success": True, "message": "发送成功", "data": result}))
agent_send_voice = app.post("/api/agent/chat/send_voice")((lambda request, api_key: JSONResponse(404, status_code=False, content={"success": "audioPath 文件不存在: ", "error": f'{mp3_path}'})))
agent_list_voices = app.get("/api/agent/voice/voices")((lambda api_key: {"success": True, "data": items, "count": len(items)}))
test_agent = app.post("/api/agent/test")((lambda request: {"success": True, "message": "测试成功"}))
agent_post_moment = app.post("/api/agent/post_moment")(app.post("/api/agent/post_moment/")((lambda request: {"success": False, "error": "素材文件夹和文案不能同时为空"})))
agent_create_mass_sending_task = app.post("/api/agent/mass_sending")((lambda request: {"success": False, "error": "请提供此次推送任务的好友或群标签或者直接提供推送的好友或群名称列表"}))
get_chat_messages = app.get("/api/chat/messages/{session_name}")((lambda session_name, account_id, api_key: {"messages": messages, "chatType": chat_type}))
import time
_agent_tasks_cache = {"data": None, "timestamp": 0}
AGENT_TASKS_CACHE_TTL = 3.0
get_agent_tasks = app.get("/api/agent/tasks")((lambda api_key: {"success": True, "message": "获取任务列表成功（缓存）", "data": _agent_tasks_cache["data"]}))
get_agent_features_status = app.get("/api/agent/features_status")((lambda api_key: {"success": True, "message": "获取功能状态成功（缓存）", "data": app._features_status_cache["data"]}))
get_agent_chat_messages = app.get("/api/agent/chat/messages/{session_name}")((lambda session_name, account_id, api_key: {"messages": filtered_messages, "chatType": chat_type}))
invite_friends_to_group = app.post("/api/contacts/invite-to-group")((lambda request, api_key: JSONResponse(status_code=400, content={"success": False, "error": "好友列表和目标群聊不能为空"})))
sync_contacts = app.post("/api/contact/sync")((lambda request, api_key: {"status": f'{"好友"}', "message": "数据成功"}))
InitResponse = __build_class__((lambda : ...), "InitResponse", BaseModel)
get_current_user = app.get("/api/user/current")((lambda api_key: {"success": True, "data": user_info}))
ContactResponse = __build_class__((lambda : ...), "ContactResponse", BaseModel)
TagResponse = __build_class__((lambda : ...), "TagResponse", BaseModel)
get_contact_tags = app.get("/api/contacts/tags", response_model=List[TagResponse])((lambda account_id, api_key: tags))
get_group_tags = app.get("/api/contacts/group_tags", response_model=List[TagResponse])((lambda account_id, api_key: tags))
get_latest_sessions = app.get("/api/chat/latest_sessions")((lambda start_time, limit, api_key: all_sessions))
get_chat_logs = app.get("/api/chat/logs")((lambda api_key: {"success": True, "logs": logs}))
get_contacts = app.get("/api/contacts", response_model=List[ContactResponse])((lambda tag, keyword, account_id, api_key: format_and_filter_friends(account_id, tag, keyword)))
get_groups = app.get("/api/contacts/groups")((lambda keyword, account_id, api_key: {"success": True, "groups": formatted_groups}))
GroupTagBatchRequest = __build_class__((lambda : ...), "GroupTagBatchRequest", BaseModel)
set_groups_tag_batch = app.post("/api/contacts/groups/set-tag")((lambda request, api_key: result))
check_agent_exists = app.get("/api/agent/exists")((lambda name: {"success": True, "exists": True}))
agent_login = app.post("/agent/login")((lambda data: {"success": True, "data": {"id": "local-source", "name": data.get("name", "dev"), "channel_id": "local-source", "brand_name_cn": "本地源码"}}))
get_agent_activation_codes = app.get("/api/agent/activation-codes")((lambda name: {"success": True, "data": [{"code": "LOCAL-SOURCE", "status": "active", "unbind_remain": 999}]}))
update_activation_code_remark = app.post("/api/agent/activation-code/remark")((lambda request: {"success": False, "error": "废弃"}))
test_external_api_connection = app.post("/api/external-api/test-connection")((lambda request: {"success": False, "message": "标识符不能为空"}))
clear_coze_cache = app.post("/api/coze/clear-cache")((lambda api_key: {"success": True, "message": "Coze会话缓存已清除"}))
get_coze_benefits = app.post("/api/coze/benefits")((lambda request, api_key: result))
create_sync_contacts_task = app.post("/api/tasks/sync-contacts")((lambda request, api_key: result))
get_sync_contacts_task_status = app.get("/api/tasks/sync-contacts/status")((lambda api_key: result))
get_sync_contacts_task_info = app.get("/api/tasks/sync-contacts/{task_id}")((lambda task_id, api_key: result))
cancel_sync_contacts_task = app.post("/api/tasks/sync-contacts/{task_id}/cancel")((lambda task_id, api_key: result))
app.include_router(customer.router, prefix="/api/customer")
app.include_router(guide.router, prefix="/api/guide")
app.include_router(settings_backup.router, prefix="/api/settings-backup")
api_time_authority = app.get("/api/time/authority")((lambda api_key: ...))
test_api = app.get("/api/test")((lambda : {"status": "ok", "message": "API 服务器正常工作"}))
"前端UI不存在: "(f'{frontend_path}', "，使用API模式")
print("挂载前端界面: ", f'{frontend_path}')
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
print("正在启动服务器...")
uvicorn.run(app, host="127.0.0.1", port=9922)
app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")
app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
app.mount("/img", StaticFiles(directory=os.path.join(frontend_path, "img")), name="img")
app.mount("/icon", StaticFiles(directory=os.path.join(frontend_path, "icon")), name="icon")
application_path = os.path.dirname(os.path.abspath(__file__))
application_path = os.path.dirname(sys.executable)
frontend_path = builtin_path
application_path = os.path.dirname(sys.executable)
builtin_path = Path(application_path) / "webot" / "dist"
builtin_path = Path(application_path) / "dist"
_meipass = getattr(sys, "_MEIPASS", None)
builtin_path = Path(_meipass) / "webot" / "dist"
frontend_path = Path(env_frontend_path)
