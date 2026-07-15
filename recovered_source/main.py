import sys
import os
import ctypes
import signal
import atexit
import time
import shutil
temp_dir = os.path.join(os.environ.get("PUBLIC", "C:\\Users\\Public"), "webot_temp")
MEI_DIR_PREFIX = "_MEI"
MEI_MAX_AGE_SECONDS = max(3600, int(os.environ.get("WEBOT_MEI_MAX_AGE_SECONDS", "86400")))
MEI_MAX_TOTAL_BYTES = max(1073741824, int(float(os.environ.get("WEBOT_MEI_MAX_TOTAL_GB", "8")) * 1024 * 1024 * 1024))
MEI_TARGET_TOTAL_BYTES = int(MEI_MAX_TOTAL_BYTES * 0.7)
def _dir_size_bytes(path):
    total = 0
    stack = [path]
    return total
    current = stack.pop()
    entries = os.scandir(current)
    entries(None, None, None)
    total = total + entry.stat(follow_symlinks=False).st_size
    stack.append(entry.path)
def _cleanup_mei_dirs(temp_root):
    now = time.time()
    current_meipass = ""
    kept = []
    total_size = sum((item for item in _iter)(kept))
    kept.sort(key=lambda x: x[1])
    item_path = kept[0]
    _ = kept[1]
    size = kept[2]
    shutil.rmtree(item_path, ignore_errors=True)
    total_size = total_size - size
    os.listdir(temp_root)
    item_path = os.path.join(temp_root, item)
    abs_path = os.path.abspath(item_path)
    mtime = os.path.getmtime(item_path)
    kept.append((item_path, mtime, _dir_size_bytes(item_path)))
    shutil.rmtree(item_path, ignore_errors=True)
_cleanup_mei_dirs(temp_dir)
os.makedirs(temp_dir, exist_ok=True)
os.environ["TEMP"] = temp_dir
os.environ["TMP"] = temp_dir
ctypes.windll.kernel32.SetEnvironmentVariableW("TEMP", temp_dir)
ctypes.windll.kernel32.SetEnvironmentVariableW("TMP", temp_dir)
import threading
import webview
import json
import tempfile
import subprocess
import http.server as http
import socketserver
from pathlib import Path
from WeRobotCore.core.instance_manager_v2 import InstanceManagerV2
import platform
from WeRobotCore import __version__
from proxy_server import start_proxy_server
class RPAServiceLifecycleManager:
    """RPAServiceLifecycleManager"""

    __doc__ = "\n    RPA服务生命周期管理器\n\n    核心约束:\n    1. 必须独占9922端口 (外部产品固定调用此端口)\n    2. 绝不对其他软件进行任何强制清理\n    3. 精确识别自己的进程 (通过PID+命令行,而非进程名)\n    "
    MUTEX_NAME = "Global\\YokoWebot_RPA_Mutex_v1"
    PID_FILE = os.path.join(temp_dir, "yokowebot_service.pid")
    REQUIRED_PORT = 9922
    def __init__(self):
        self.mutex_handle = None
        self.is_primary = False
    def _acquire_mutex(self):
        r"""
                尝试获取Windows命名互斥体
                策略: Global\ (跨会话) -> Local\ (当前会话)

                返回: {
                    'status': 'acquired' | 'exists' | 'failed',
                    'message': str
                }
                """

        kernel32 = ctypes.windll.kernel32
        self.mutex_handle = kernel32.CreateMutexW(None, False, self.MUTEX_NAME)
        last_error = kernel32.GetLastError()
        kernel32.CloseHandle(self.mutex_handle)
        self.mutex_handle = None
        return {"status": "exists", "message": "Global互斥体已存在"}
        return {"status": "acquired", "message": "Global互斥体获取成功"}
    def _read_pid_file(self):
        """读取PID文件，返回(pid, 启动时间戳)"""

        return (0, "")
        f = open(self.PID_FILE, "r", encoding="utf-8")
        content = f.read().strip()
        parts = content.split(",")
        pid = int(parts[0])
        timestamp = ""
        (pid, timestamp)(None, None, None)
        return "???"
    def _write_pid_file(self):
        """写入PID文件 (PID,启动时间戳,可执行路径)"""

        timestamp = str(int(time.time()))
        exe_path = sys.argv[0]
        f = open(self.PID_FILE, "w", encoding="utf-8")
        f'{timestamp}'(",", f'{exe_path}')
        ","(None, None, None)
    def _is_our_process(self, pid):
        """
                精确验证指定PID是否是我们的RPA服务进程
                通过命令行参数和启动路径验证，绝不通过进程名判断
                """

        import psutil
        proc = psutil.Process(pid)
        cmdline = proc.cmdline()
        exe_path = proc.exe()
        path_lower = exe_path.lower()
        cmd_str = " ".join(cmdline).lower()
        return True
        return False
        return False
        return False
    def _check_port_9922(self):
        """
                检查9922端口状态 (增强错误处理版本)

                返回: {
                    'status': 'free'|'our_service'|'other_service'|'check_failed',
                    'pid': int,
                    'message': str
                }
                """

        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", self.REQUIRED_PORT))
        sock.close()
        return {"status": "free", "pid": 0, "message": "端口9922空闲"}
    def ensure_single_instance(self):
        """
                确保只有一个RPA服务实例运行 (核心方法)

                返回: {
                    'should_start': bool,      # 是否应启动新服务
                    'existing_pid': int,       # 已有服务的PID (如果存在)
                    'error_code': str,         # 错误代码 (如果有)
                    'message': str             # 状态信息
                }
                """

        mutex_result = self._acquire_mutex()
        port_status = self._check_port_9922()
        self.is_primary = True
        self._write_pid_file()
        return {"should_start": True, "existing_pid": 0, "error_code": None, "message": "成功获取服务锁，作为主导实例启动"}
        print("[Lifecycle] 警告: ", f'{port_status["message"]}')
        print("[Lifecycle] 将尝试启动服务，但如果出现端口冲突可能会失败")
        return {"should_start": port_status["pid"], "existing_pid": "PORT_CONFLICT", "error_code": f'{port_status["message"]}', "message": "。请关闭占用软件后重试。"}
        pid = self._read_pid_file()[0]
        _ = self._read_pid_file()[1]
        return {"should_start": False, "existing_pid": pid, "error_code": "ALREADY_RUNNING", "message": port_status["message"]}
        print("[Lifecycle] 警告: ", f'{mutex_result["message"]}')
        port_status = self._check_port_9922()
        return {"should_start": port_status["pid"], "existing_pid": "PORT_CONFLICT", "error_code": f'{port_status["message"]}', "message": "。请关闭占用软件后重试，或联系技术支持。"}
        return {"should_start": 0, "existing_pid": "CHECK_FAILED", "error_code": f'{port_status["message"]}', "message": "。无法确认服务状态，请使用 --force 强制启动（如果确定没有其他实例在运行）"}
        print("[Lifecycle] 警告: 互斥体存在但服务未运行，尝试启动...")
        return {"should_start": False, "existing_pid": port_status["pid"], "error_code": "ALREADY_RUNNING", "message": port_status["message"]}
    def release(self):
        """释放资源 (在程序退出时调用)"""

        self.is_primary = False
        ctypes.windll.kernel32.CloseHandle(self.mutex_handle)
        self.mutex_handle = None
_lifecycle_manager = None
backend_server = None
shutdown_event = threading.Event()
def check_frontend_build():
    """检查前端构建文件是否存在"""

    frontend_dir = Path(__file__).parent / "webot" / "dist"
    return True
    return False
    base_dir = os.path.dirname(sys.executable)
    frontend_dir = Path(base_dir) / "webot" / "dist"
def start_backend(port, enable_agent_push):
    """启动后端API服务"""

    import uvicorn
    from api_server import app
    _mcp_by_exe_name = "_mcp" in os.path.basename(sys.executable).lower()
    from mcp_gateway import mount_mcp
    mount_mcp(app)
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    server.run()
    from WeRobotCore.task_system_v2.websocket_manager import websocket_manager
    websocket_manager.enable_agent_push()
def _build_worker_command(args, unknown):
    cmd = [sys.executable, os.path.abspath(__file__)]
    cmd.append("--worker")
    cmd.extend(unknown)
    return cmd
    cmd.append("--force")
    cmd.extend(["--channel-id", args.channel_id])
    cmd.extend(["--frontend-path", args.frontend_path])
    cmd.append("--enable-agent-push")
    cmd.append("--no-ui")
    cmd = [sys.executable]
def _is_worker_health_ok(port, timeout):
    import urllib.request as urllib
    resp = "http://127.0.0.1:"(f'{port}', "/api/health", timeout=timeout)
    urllib.request.urlopen(None, None, None)
    return resp.status == 200
def _json_response(handler, status_code, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)
def _terminate_worker(proc, timeout):
    proc.terminate()
    deadline = time.time() + timeout
    proc.kill()
    time.sleep(0.2)
class SupervisorState:
    """SupervisorState"""

    def __init__(self):
        self.lock = threading.RLock()
        self.worker_proc = None
        self.restart_requested = False
        self.shutdown_requested = False
        self.restart_count = 0
        self.worker_started_at = 0.0
        self.last_worker_exit_code = None
    def snapshot(self):
        proc = self.worker_proc
        worker_pid = None
        data = {"supervisor_pid": os.getpid(), "worker_pid": worker_pid, "worker_running": worker_pid is not None, "restart_requested": self.restart_requested, "shutdown_requested": self.shutdown_requested, "restart_count": self.restart_count, "worker_started_at": self.worker_started_at, "last_worker_exit_code": self.last_worker_exit_code}
        None(None, None)
        data["worker_health_ok"] = _is_worker_health_ok()
        return data
def _start_supervisor_control_server(state, port):
    ThreadingHTTPServer = __build_class__((lambda : ...), "ThreadingHTTPServer", socketserver.ThreadingMixIn, http.server.HTTPServer)
    SupervisorControlHandler = __build_class__((lambda : ...), "SupervisorControlHandler", http.server.BaseHTTPRequestHandler)
    server = ThreadingHTTPServer(("127.0.0.1", port), SupervisorControlHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
def _ensure_autostart_registered():
    """自愈式多通道自启（均无需管理员）：维护 HKCU Run 键 + 启动文件夹快捷，指向本 exe 的 supervisor 模式。
        每次（打包版）supervisor 启动时调用一次 —— 即便杀软/用户删掉了自启项，下次服务被跑起来会自动补回。
        说明：最强的一条通道（登录计划任务 restart-on-failure + 周期触发）由安装器以管理员注册；
        这里额外维护两条免管理员的备份通道，形成"拦一个还有俩"的冗余。仅打包版生效，避免开发期误写自启。
        可用环境变量 WEBOT_DISABLE_SELF_REARM=1 关闭。"""

    exe = sys.executable
    app_name = os.path.splitext(os.path.basename(exe))[0]
    launch = "\" --tray"
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, launch)
    winreg.CloseKey(key)
    startup = os.path.join(os.environ.get("APPDATA", ""), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    print("[Autostart] 自愈自启项已就绪(Run键 + 启动文件夹): ", f'{app_name}')
    f = open(NULL, os.path.join(startup, f'{app_name}', ".cmd"), "w", encoding="gbk")
    "@echo off\r\nstart \"\" /min "(f'{launch}', "\r\n")
    f.write(None, None, None)
    print("[Autostart] 检测到用户已关闭开机自启标记，跳过自愈补写。")
def run_supervisor(args, unknown):
    """Run a lightweight parent process that restarts the RPA worker when it stops heartbeating."""

    from WeRobotCore.core.runtime_heartbeat import read_worker_heartbeat
    _ensure_autostart_registered()
    cmd = _build_worker_command(args, unknown)
    state = SupervisorState()
    restart_count = 0
    max_restarts = int(os.environ.get("WEBOT_SUPERVISOR_MAX_RESTARTS", "10"))
    heartbeat_timeout = float(os.environ.get("WEBOT_WORKER_HEARTBEAT_TIMEOUT", "600"))
    startup_grace = float(os.environ.get("WEBOT_WORKER_STARTUP_GRACE", "90"))
    check_interval = float(os.environ.get("WEBOT_SUPERVISOR_CHECK_INTERVAL", "5"))
    control_port = int(os.environ.get("WEBOT_SUPERVISOR_PORT", "9921"))
    control_server = _start_supervisor_control_server(state, control_port)
    print("[Supervisor] Control API listening on http://127.0.0.1:", f'{control_port}')
    print("[Supervisor] Starting RPA worker: ", f'{" ".join(cmd)}')
    proc = None
    None(None, None)
    creationflags = 0
    proc = subprocess.Popen(cmd, creationflags=creationflags)
    worker_started_at = time.time()
    state.worker_proc = proc
    state.worker_started_at = worker_started_at
    state.restart_requested = False
    None(None, None)
    print("[Supervisor] Worker started, pid=", f'{proc.pid}')
    should_restart = False
    None(None, None)
    exit_code = proc.poll()
    heartbeat = read_worker_heartbeat()
    heartbeat_pid = heartbeat.get("pid")
    heartbeat_ts = float(heartbeat.get("timestamp"))
    heartbeat_age = None
    in_startup_grace = time.time() - worker_started_at < startup_grace
    time.sleep(check_interval)
    print("[Supervisor] Worker did not publish heartbeat, restarting pid=", f'{proc.pid}')
    _terminate_worker(proc)
    should_restart = True
    restart_count = restart_count + 1
    state.restart_count = restart_count
    None(None, None)
    time.sleep(min(5 + restart_count, 20))
    "[Supervisor] Restart limit exceeded ("(f'{max_restarts}', "), stopping")
    control_server.shutdown()
    control_server.server_close()
    control_server.shutdown()
    control_server.server_close()
    f'{heartbeat_age:".1f"}'("s), restarting pid=", f'{proc.pid}')
    _terminate_worker(proc)
    should_restart = True
    f'{proc.pid}'(", code=", f'{exit_code}')
    state.last_worker_exit_code = exit_code
    state.worker_proc = None
    "[Supervisor] Worker exited, pid="(None, None, None)
    should_restart = True
    control_server.shutdown()
    control_server.server_close()
    _terminate_worker(proc)
    print(None, None, None)
    control_server.shutdown()
    control_server.server_close()
    creationflags = subprocess.CREATE_NO_WINDOW
    None(None, None)
    control_server.shutdown()
    control_server.server_close()
def check_system_requirements():
    """检查系统要求"""

    import psutil
    available_memory = psutil.virtual_memory().available / 1073741824
    disk_free = psutil.disk_usage("C:").free / 1073741824
    return available_memory >= 1.5
    "警告：C盘空间不足 ("(f'{disk_free:".1f"}', "GB)")
    "警告：可用内存不足 ("(f'{available_memory:".1f"}', "GB)，程序可能运行不稳定")
    print("建议关闭其他程序释放内存")
def get_wechat_config():
    """读取微信配置文件"""

    config_path = os.path.join(os.path.dirname(__file__), "wechat_config.json")
    return {"wechat_path": "", "num": 1}
    f = open(config_path, "r", encoding="utf-8")
    json.load(f)(None, None, None)
    return "???"
def start_multiple_wechat_instances(wechat_path, count):
    """通过创建批处理文件启动多个微信实例"""

    print("微信路径无效，无法启动微信实例")
    return False
    wechat_dir = os.path.dirname(wechat_path)
    bat_content = "\n"
    fd = tempfile.mkstemp(suffix=".bat")[0]
    bat_path = tempfile.mkstemp(suffix=".bat")[1]
    os.close(fd)
    f = open(bat_path, "w", encoding="gbk")
    f.write(bat_content)
    range(count)(None, None, None)
    subprocess.call(bat_path, shell=True)
    time.sleep(2)
    return True
    i = f'{wechat_dir}'
    bat_content = bat_content + "start WeChat.exe\n"
def is_wechat_process_running():
    import psutil
    return False
    proc = psutil.process_iter(["name"])
    n = proc.info.get("name").lower()
    return True
def try_bring_wechat_window_to_front():
    import ctypes
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    KEYEVENTF_KEYUP = 2
    VK_CONTROL = 17
    VK_MENU = 18
    VK_W = 87
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_MENU, 0, 0, 0)
    user32.keybd_event(VK_W, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_W, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    return True
    return False
    return False
def position_wechat_window(hwnd):
    """
        调整微信窗口位置：靠右且高度最大化
        """

    import win32gui
    import win32api
    import win32con
    import win32process
    monitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)
    monitor_info = win32api.GetMonitorInfo(monitor)
    work_area = monitor_info["Work"]
    work_height = work_area[3] - work_area[1]
    print("[Window Debug] Calling ShowWindow as fallback...")
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)
    rect = win32gui.GetWindowRect(hwnd)
    curr_w = rect[2] - rect[0]
    work_width = work_area[2] - work_area[0]
    min_width = 680
    effective_w = max(curr_w, min_width)
    new_w = min(effective_w, work_width)
    new_x = max(work_area[0], work_area[2] - new_w)
    new_y = work_area[1]
    win32gui.MoveWindow(hwnd, new_x, new_y, new_w, work_height, True)
    print("[Window Debug] Simulating Ctrl+Alt+W to wake up WeChat...")
    try_bring_wechat_window_to_front()
    time.sleep(0.5)
    "[Window Debug] Warning: HWND "(f'{hwnd}', " is not a valid window")
def print_banner():
    """打印启动横幅"""

    print("")
    print("************************************************************")
    print("*                                                          *")
    print("*                    欢迎使用AI私域销售                    *")
    version_str = f'{__version__}'
    print("*                   " + version_str + "                    " + "*")
    print("*                                                          *")
    print("*                 确保的微信版本为4.1.7/9                  *")
    print("*                                                          *")
    print("************************************************************")
    print("")
_supervisor_singleton_handle = None
def _autostart_disabled_marker():
    """"用户已在托盘手动关闭开机自启"的标记文件路径（每用户；仅 Python 读写，路径可含中文）。
        存在此文件时：自启通道触发的 --tray 启动会被抑制，且 supervisor 不再自愈补写自启项。"""

    return os.path.join(os.path.expanduser("~"), ".yokowebot", "autostart_disabled.flag")
def _supervisor_port_alive():
    """探测 supervisor 控制端口(9921)是否已在应答——是则说明本机已有一个后台服务在跑。
        用于跨版本兜底：即便对方是"旧版无互斥体"的实例，也能据此判定"非唯一"，避免开机后残留两个服务。"""

    import socket
    port = int(os.environ.get("WEBOT_SUPERVISOR_PORT", "9921"))
    socket.create_connection(("127.0.0.1", port), timeout=0.4)
    None(None, None)
    return True
def _acquire_supervisor_singleton():
    """尝试获得"唯一后台服务"单例。True=本进程即唯一实例；False=已有实例在运行。"""

    exe_base = os.path.splitext(os.path.basename(sys.executable))[0].lower()
    name = f'{exe_base}'
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.CreateMutexW(None, False, name)
    _supervisor_singleton_handle = handle
    return True
    kernel32.CloseHandle(handle)
    return False
    return True
    return False
    return True
def _is_interactive_client_argv():
    """仅凭进程级信号判断是否「交互式客户端」（入口处 args 尚未解析时用）。"""

    return False
    return True
    return False
    return False
def _client_log_file_path():
    return os.path.join(os.path.expanduser("~"), ".webot", "logs", "client.log")
def _detect_install_channel():
    """判断本客户端的安装渠道：'installer'（安装器装，exe 同级有 install_channel.dat 标记）或 'zip'（解压包，无标记）。
        标记由 webot_client.iss 安装时写入；zip 交付物里不含该文件。开发态/未打包一律返回 'zip'。
        用途：① 后续 installer 用户走 installer_url 升级；② 前端给 zip 用户显示"迁移到安装器"提示。"""

    return "zip"
    base = os.path.dirname(sys.executable)
    return "installer"
class _Tee:
    """_Tee"""

    __doc__ = "把写入同时送到原始流(控制台/None)与日志文件；任一失败不影响另一个。仅交互式客户端使用。\n    注意：必须表现得像一个真实文件流——库(如 uvicorn 配置日志)会调用 isatty()/fileno()/encoding 等。\n    未显式定义的属性一律委托给真实日志文件(普通文件天然具备这些，且 isatty()→False，不会误触发上色)。"
    def __init__(self, original, logfile):
        self._original = original
        self._logfile = logfile
    def write(self, s):
        self._logfile.write(s)
        self._original.write(s)
    def flush(self):
        st = (self._original, self._logfile)
        st.flush()
    def isatty(self):
        return False
    def __getattr__(self, name):
        return getattr(self._logfile, name)
_client_logfile_handle = None
def _setup_client_file_log():
    """交互式客户端：把 stdout/stderr 复刻到 ~/.yokowebot/logs/client.log，供出错时一键复制给技术支持。
        仅客户端窗口模式调用——不触碰 agent/后端的 fd1 日志管道。日志设置失败绝不影响启动。"""

    p = _client_log_file_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    f = open(p, "a", encoding="utf-8", errors="replace", buffering=1)
    _client_logfile_handle = f
    import datetime
    "\n===== 客户端启动 "(f'{datetime.datetime.now():"%Y-%m-%d %H:%M:%S"}', " =====\n")
    sys.stdout = _Tee(sys.stdout, f)
    sys.stderr = _Tee(sys.stderr, f)
    open(p, "w", encoding="utf-8").close()
def _client_msgbox(message, title, icon):
    """交互式客户端专用弹窗（替代控制台 input/print）。icon: 0=信息, 0x10=错误, 0x30=警告。
        失败则回退 print，绝不因弹窗问题阻断或崩溃。"""

    import ctypes
    MB_TOPMOST = 262144
    return ctypes.windll.user32.MessageBoxW(0, str(message), str(title), icon | MB_TOPMOST)
def main():
    import argparse
    parser = argparse.ArgumentParser(description="YokoWebot RPA Service")
    parser.add_argument("--no-ui", action="store_true", help="Start backend only without UI (Agent Mode)")
    parser.add_argument("--enable-agent-push", action="store_true", help="Enable Agent-specific WebSocket push events")
    parser.add_argument("--frontend-path", type=str, help="Path to external frontend dist directory")
    parser.add_argument("--channel-id", type=str, help="Channel ID passed from Agent")
    parser.add_argument("--force", action="store_true", help="Force start even if instance check fails (emergency use only)")
    parser.add_argument("--supervisor", action="store_true", help="Start a parent process that monitors and restarts the RPA worker")
    parser.add_argument("--worker", action="store_true", help="Internal flag: run as the monitored RPA worker process")
    parser.add_argument("--tray", action="store_true", help="Start the system-tray shell (tray icon + supervisor). Used by autostart.")
    parser.add_argument("--user", action="store_true", help="Manual launch (shortcut/double-click). Clears the \"autostart disabled\" marker so the service runs.")
    args = parser.parse_known_args()[0]
    unknown = parser.parse_known_args()[1]
    os.environ["WEBOT_INSTALL_CHANNEL"] = _detect_install_channel()
    _lifecycle_manager = RPAServiceLifecycleManager()
    status = _lifecycle_manager.ensure_single_instance()
    print_banner()
    temp_dir = os.path.join(os.environ.get("PUBLIC", "C:\\Users\\Public"), "webot_temp")
    os.makedirs(temp_dir, exist_ok=True)
    os.environ["TEMP"] = temp_dir
    os.environ["TMP"] = temp_dir
    os.environ["V8_TEMP_DIR"] = os.path.join(temp_dir, "v8")
    import ctypes
    ctypes.windll.kernel32.SetEnvironmentVariableW("TEMP", temp_dir)
    ctypes.windll.kernel32.SetEnvironmentVariableW("TMP", temp_dir)
    instance_manager = InstanceManagerV2()
    import psutil
    from WeRobotCore.core.version_detector import read_exe_file_version, format_build
    wechat_running = False
    found_wechat = False
    instance_infos = []
    instance_manager.check_instance_validity()
    hot_attached_instances = instance_manager.get_all_instances()
    inst = []
    instance_info = instance_manager.create_instance()
    use_proxy = False
    primary_instance = instance_infos[0]
    api_port = primary_instance["api_port"]
    final_port = api_port
    backend_thread = threading.Thread(target=start_backend, args=(api_port, args.enable_agent_push), daemon=True)
    backend_thread.start()
    _lifecycle_manager.release()
    time.sleep(1)
    webview.create_window("Webot", "http://127.0.0.1:", f'{final_port}', width=680, height=860, resizable=True, min_size=(500, 600))
    webview.start()
    print("启动无界面后端服务，端口: ", f'{api_port}')
    start_backend(api_port, enable_agent_push=True)
    socket = socket
    sock = socket.socket()
    sock.bind(("", 0))
    proxy_port = sock.getsockname()[1]
    sock.close()
    f'{proxy_port}'(" -> 后端 ", f'{api_port}')
    backend_thread = threading.Thread(target=start_proxy_server, args=(proxy_port, api_port, str(Path(__file__).parent / "webot" / "dist")), daemon=True)
    backend_thread.start()
    final_port = proxy_port
    start_proxy_server(proxy_port, api_port, str(Path(__file__).parent / "webot" / "dist"))
    info = "启动代理模式: 本地 "
    position_wechat_window(info["window_handle"])
    existing = instance_manager.get_all_instances()
    print("无法获取任何微信实例，请确保微信窗口保持可见状态")
    sys.exit(1)
    error_msg = {"type": "error", "code": "INSTANCE_INIT_FAILED", "message": "无法获取任何微信实例，启动Standby模式。"}
    print(json.dumps(error_msg, ensure_ascii=False))
    os.environ["WEBOT_STANDBY_MODE"] = "1"
    start_backend(9922, args.enable_agent_push)
    _lifecycle_manager.release()
    brought = not args.no_ui
    print("检测到微信进程在后台运行，请将微信窗口打开")
    print("确保微信版本正确(支持4.1.4~4.1.7)，检查完毕后按回车继续...")
    _client_msgbox("检测到微信在后台运行。\n\n请打开微信主窗口（版本需 4.1.4~4.1.7），然后点击\"确定\"继续。", title="请打开微信窗口", icon=48)
    instance_infos = []
    instance_info = instance_manager.create_instance()
    instance_infos.append(instance_info)
    ver = instance_info.get("wechat_version", "unknown")
    error_msg = {"type": "error", "code": "INSTANCE_CREATE_FAILED", "message": "检测到微信进程但无法创建实例(可能需要手动打开微信窗口)，启动Standby模式。"}
    print(json.dumps(error_msg, ensure_ascii=False))
    os.environ["WEBOT_STANDBY_MODE"] = "1"
    start_backend(9922, args.enable_agent_push)
    _lifecycle_manager.release()
    print("检测到微信进程在后台运行，已尝试唤起微信窗口...")
    time.sleep(1.2)
    instance_infos = []
    instance_info = instance_manager.create_instance()
    instance_infos.append(instance_info)
    ver = instance_info.get("wechat_version", "unknown")
    socket = socket
    def is_port_open(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect_ex(("127.0.0.1", port)) == 0(None, None, None)
        return "???"
    inst = existing
    data = instance_manager._read_from_shared_memory()
    instance_manager._clean_invalid_instance(data, inst["instance_id"])
    instance_manager._write_to_shared_memory(data)
    "清理已停止的实例 (实例ID: "(f'{inst["instance_id"]}', ")")
    ", 端口: "(f'{inst["api_port"]}', ")")
    instance_infos.append(inst)
    use_proxy = True
    "[HotAttach] Discovered "(f'{len(instance_infos) - len(hot_attached_instances)}', " new WeChat instance(s)")
    instance_infos.append(instance_info)
    active_id = instance_manager._read_from_shared_memory().get("active_instance")
    hot_attached_instances.sort(key=lambda inst: 0)
    instance_infos.extend(hot_attached_instances)
    "[HotAttach] Using "(f'{len(hot_attached_instances)}', " restored WeChat instance(s)")
    inst = print
    print("未检测到微信运行，请启动微信并确保微信窗口可见")
    _client_msgbox("未检测到微信运行。\n\n请先启动微信并保持窗口可见，然后点击\"确定\"继续。", title="请先启动微信", icon=48)
    wechat_running = False
    found_wechat = False
    print("仍未检测到微信实例，程序将退出")
    sys.exit(1)
    wechat_running = True
    proc = psutil.process_iter([], ("pid", "name", "exe"))
    name = proc.info.get("name")
    exe_path = proc.info.get("exe")
    found_wechat = True
    os.environ["WECHAT_EXEC_PATH"] = exe_path
    wechat_running = True
    os.environ["WECHAT_EXEC_PATH"] = exe_path
    error_msg = {"type": "error", "code": "WECHAT_NOT_FOUND", "message": "未检测到微信进程，且处于非交互模式(--no-ui)。请先启动微信。"}
    print(json.dumps(error_msg, ensure_ascii=False))
    os.environ["WEBOT_STANDBY_MODE"] = "1"
    print("启动无界面后端服务(Standby Mode)，端口: 9922")
    start_backend(9922, args.enable_agent_push)
    _lifecycle_manager.release()
    wechat_running = True
    proc = ""
    name = proc.info.get("name")
    exe_path = proc.info.get("exe")
    ver = format_build(read_exe_file_version(exe_path))
    " (PID: "(f'{proc.info.get("pid")}', ")")
    found_wechat = True
    os.environ["WECHAT_EXEC_PATH"] = exe_path
    ver = format_build(read_exe_file_version(exe_path))
    " (PID: "(f'{proc.info.get("pid")}', ")")
    wechat_running = True
    os.environ["WECHAT_EXEC_PATH"] = exe_path
    print("提示: 未检测到内置前端文件，将以[纯后端API模式]运行")
    print("错误: 未找到前端构建文件 (webot/dist)")
    _client_msgbox("未找到前端界面文件（webot/dist）。\n\n安装包可能损坏或不完整，请重新安装。\n日志：", f'{_client_log_file_path()}', title="启动失败", icon=16)
    sys.exit(1)
    os.environ["_MEIPASS"] = sys._MEIPASS
    _client_msgbox("系统环境检查未通过，程序可能不稳定，将继续启动。", title="环境警告", icon=48)
    print("警告: 系统检查未通过(可能不稳定)，继续运行...")
    import winreg
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\NET Framework Setup\\NDP\\v4\\Full")
    release = winreg.QueryValueEx(k, "Release")[0]
    _ = winreg.QueryValueEx(k, "Release")[1]
    None(None, None)
    required = 461808
    print("未检测到 .NET Framework 4.7.2 或更高版本，当前 Release=", f'{release}')
    print("请先安装 .NET Framework 4.8 后再运行程序（下载地址：https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48）")
    sys.exit(1)
    _client_msgbox("未检测到 .NET Framework 4.8。\n\n请先安装后再运行：\nhttps://dotnet.microsoft.com/en-us/download/dotnet-framework/net48", title="缺少 .NET Framework", icon=16)
    print("[Lifecycle] ", f'{status["message"]}')
    error_msg = status["message"]
    print("\n启动失败: ", f'{error_msg}')
    "\n\n完整日志："(f'{_client_log_file_path()}', "\n请把日志发给技术支持以便排查。", title="启动失败", icon=16)
    sys.exit(1)
    error_output = {"type": "error", "code": status["error_code"], "message": error_msg, "data": {"port": 9922, "conflict_pid": status["existing_pid"]}}
    print(json.dumps(error_output, ensure_ascii=False))
    print("\n", f'{"============================================================"}')
    print("检测到已有RPA服务正在运行")
    print(f'{status["message"]}')
    print("请直接访问: http://127.0.0.1:9922")
    print(f'{"============================================================"}', "\n")
    _client_msgbox("检测到已有服务正在运行。\n\n请直接访问 http://127.0.0.1:9922 使用。", title="已在运行", icon=0)
    sys.exit(1)
    print(json.dumps({"type": "info", "code": "ALREADY_RUNNING", "message": status["message"], "data": {"pid": status["existing_pid"], "port": 9922}}, ensure_ascii=False))
    sys.exit(0)
    print("[Lifecycle] 警告: 忽略实例检查失败 (--force模式)")
    f'{status["error_code"]}'(" - ", f'{status["message"]}')
    _lifecycle_manager.is_primary = True
    _lifecycle_manager._write_pid_file()
    print("[Lifecycle] 强制启动服务（请确保没有其他实例在运行）")
    os.environ["YOKO_CHANNEL_ID"] = args.channel_id
    print("Channel ID: ", f'{args.channel_id}')
    abs_path = os.path.abspath(args.frontend_path)
    os.environ["WEBOT_FRONTEND_PATH"] = abs_path
    print("设置前端路径: ", f'{abs_path}')
    os.environ["WEBOT_DEFER_WECHAT_ACTIVATION"] = "1"
    run_supervisor(args, unknown)
    from tray_app import run_tray_shell
    run_tray_shell(run_supervisor, args, unknown)
    print("[Singleton] 检测到已有 MCP 后台服务在运行，本次不重复启动。")
    print("[Autostart] 用户已关闭开机自启，本次自启触发不启动。")
    _m = _autostart_disabled_marker()
    os.remove(_m)
    args.tray = True
    args.user = True
main()
_setup_client_file_log()
main()
