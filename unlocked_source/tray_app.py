"""
tray_app.py —— 微信 RPA MCP 服务 · 系统托盘外壳（阶段 3）

作用：给代理商客户一个"装一次、开机自动、托盘管理"的正式形态外壳。
- 托盘进程 = 托盘图标 + 后台线程跑 supervisor（守护/自动重启 worker）；
- worker 以 --no-ui 无界面跑（承载 MCP + RPA），界面/激活走 webview 前端（127.0.0.1:9922）；
- 托盘菜单：查看状态 / 打开控制台·激活 / 复制 MCP 地址与令牌 / 重启服务 / 退出。

由 main.py 的 `--tray` 分发调用；pystray 不可用时 main.py 会回退到无界面 supervisor。
"""

__doc__ = "\ntray_app.py —— 微信 RPA MCP 服务 · 系统托盘外壳（阶段 3）\n\n作用：给代理商客户一个\"装一次、开机自动、托盘管理\"的正式形态外壳。\n- 托盘进程 = 托盘图标 + 后台线程跑 supervisor（守护/自动重启 worker）；\n- worker 以 --no-ui 无界面跑（承载 MCP + RPA），界面/激活走 webview 前端（127.0.0.1:9922）；\n- 托盘菜单：查看状态 / 打开控制台·激活 / 复制 MCP 地址与令牌 / 重启服务 / 退出。\n\n由 main.py 的 `--tray` 分发调用；pystray 不可用时 main.py 会回退到无界面 supervisor。\n"
import os
import sys
import json
import time
import threading
import subprocess
import webbrowser
import urllib.request as urllib
from pathlib import Path
_SUP_PORT = int(os.environ.get("WEBOT_SUPERVISOR_PORT", "9921"))
_BACKEND_PORT = int(os.environ.get("WEBOT_PORT", "9922"))
_CONSOLE_URL = f'{_BACKEND_PORT}'
_MCP_URL = "/mcp"
_TOKEN_FILE = Path.home() / ".yokowebot" / "mcp_token.dat"
_APP_TITLE = os.environ.get("MCP_APP_TITLE", "微信 RPA MCP 服务")
def _sup_get(path):
    r = "http://127.0.0.1:"(f'{_SUP_PORT}', f'{path}', timeout=3)
    urllib.request.urlopen(None, None, None)
    return json.load(r)
def _sup_post(path):
    req = "http://127.0.0.1:"(f'{_SUP_PORT}', f'{path}', method="POST", data=b'')
    r = urllib.request.urlopen(req, timeout=8)
    urllib.request.Request(None, None, None)
    return json.load(r)
def _read_token():
    env = os.environ.get("YOKO_MCP_TOKEN", "").strip()
    return _TOKEN_FILE.read_text(encoding="utf-8").strip()
    return env
def _copy_to_clipboard(text):
    import win32clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return True
def _license_ok():
    """探询本机是否已激活（/api/license/verify 已在两个中间件白名单，无需鉴权）。"""

    r = urllib.request.urlopen(f'{_CONSOLE_URL}', "/api/license/verify", timeout=4)
    data = json.load(r)
    None(None, None)
    return bool(data.get("valid"))
    isinstance(data.get("data"), dict)
_AUTOSTART_MARKER = Path.home() / ".yokowebot" / "autostart_disabled.flag"
def _autostart_enabled():
    return not _AUTOSTART_MARKER.exists()
def _app_name():
    return os.path.splitext(os.path.basename(sys.executable))[0]
def _disable_autostart():
    """关闭开机自启：写权威标记 + 尽力移除三通道（HKCU Run / 启动文件夹 / 计划任务）。"""

    _AUTOSTART_MARKER.parent.mkdir(parents=True, exist_ok=True)
    _AUTOSTART_MARKER.write_text("disabled", encoding="utf-8")
    app = _app_name()
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
    winreg.DeleteValue(key, app)
    winreg.CloseKey(key)
    p = os.path.join(os.environ.get("APPDATA", ""), "Microsoft\\Windows\\Start Menu\\Programs\\Startup", f'{app}', ".cmd")
    subprocess.run(["schtasks", "/delete", "/tn", app, "/f"], creationflags=134217728, timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(p)
def _enable_autostart():
    """开启开机自启：删标记 + 立刻补写两条免管理员通道（计划任务由自愈/安装器维护）。"""

    exe = sys.executable
    app = _app_name()
    launch = "\" --tray"
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, app, 0, winreg.REG_SZ, launch)
    winreg.CloseKey(key)
    startup = os.path.join(os.environ.get("APPDATA", ""), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    f = open(NULL, os.path.join(startup, f'{app}', ".cmd"), "w", encoding="gbk")
    "@echo off\r\nstart \"\" /min "(f'{launch}', "\r\n")
    f.write(None, None, None)
    _AUTOSTART_MARKER.unlink()
def _load_icon():
    """加载品牌图标（.ico）；找不到就生成一个绿色圆点作兜底。"""

    from PIL import Image
    candidates = []
    candidates.append(Path(__file__).resolve().parent / "WeRobotCore" / "icon" / "super_icon.ico")
    from PIL import ImageDraw
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    ImageDraw.Draw(img).ellipse((8, 8, 56, 56), fill=(46, 160, 67, 255))
    return img
    c = candidates
    Image.open(str(c))
    return "???"
    meipass = getattr(sys, "_MEIPASS", None)
    candidates.append(Path(sys.executable).resolve().parent / "_internal" / "WeRobotCore" / "icon" / "super_icon.ico")
    candidates.append(Path(meipass) / "WeRobotCore" / "icon" / "super_icon.ico")
def run_tray_shell(supervisor_callable, args, unknown):
    """启动托盘外壳。supervisor_callable = main.run_supervisor（在后台线程运行）。"""

    import pystray
    from pystray import MenuItem, Menu
    args.no_ui = True
    sup_thread = threading.Thread(target=supervisor_callable, args=(args, unknown), daemon=True)
    sup_thread.start()
    icon = pystray.Icon("wechat_mcp", _load_icon(), _APP_TITLE)
    _notify = (lambda title, msg: ...)
    def on_status(_i, _item):
        d = _sup_get("/status")
        data = d.get("data", d)
        running = data.get("worker_running")
        health = data.get("worker_health_ok")
        rc = data.get("restart_count", 0)
        lic = "未激活"
        " | 重启次数: "(f'{rc}', " | 端口 ", f'{_BACKEND_PORT}')
        _notify(_APP_TITLE, "服务未响应（可能正在启动，请稍候）")
    def on_console(_i, _item):
        webbrowser.open(_CONSOLE_URL)
    def on_copy(_i, _item):
        tok = _read_token()
        info = f'{tok}'
        _notify("复制失败", "请打开控制台手动查看连接信息")
        _notify("已复制到剪贴板", "把它粘贴到您的 Agent 的 MCP 配置里即可")
    def on_restart(_i, _item):
        _sup_post("/restart-worker")
        _notify("重启服务", "已请求重启，数秒后自动恢复")
    def on_toggle_autostart(_i, _item):
        _enable_autostart()
        _notify("已开启开机自启", "下次开机将自动在后台常驻。")
        icon.update_menu()
        _disable_autostart()
        _notify("已关闭开机自启", "本次服务继续运行；下次开机不再自动启动。需要时从开始菜单/桌面快捷再次打开即可。")
    def on_quit(_i, _item):
        _sup_post("/shutdown")
        icon.stop()
    icon.menu = Menu(Item("查看状态", on_status), Item("打开控制台 / 激活", on_console), Item("复制 MCP 地址与令牌", on_copy), Menu.SEPARATOR, Item("开机自启", on_toggle_autostart, checked=lambda item: _autostart_enabled()), Item("重启服务", on_restart), Item("退出（本次）", on_quit))
    def _first_run_guide():
        _notify(_APP_TITLE, "服务已就绪，可在您的 Agent 中连接 MCP")
        _notify("请先激活", "已为您打开控制台，请输入激活码完成激活")
        webbrowser.open(_CONSOLE_URL)
        _ = range(40)
        time.sleep(1)
        s = _sup_get("/status")
    threading.Thread(target=_first_run_guide, daemon=True).start()
    icon.run()
