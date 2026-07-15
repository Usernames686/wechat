# Decompiled from: version_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import sys
import shutil
import tempfile
import requests
import zipfile
import subprocess
import logging
import platform
import re
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
class VersionManager:
    """VersionManager"""

    _instance = None
    _initialized = False
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
    def __init__(self):
        self.supabase = SupabaseManager()
        self.config_manager = ConfigManager()
        self.application_path = os.path.dirname(os.path.abspath(__file__))
        self.application_path = os.path.dirname(os.path.dirname(os.path.dirname(self.application_path)))
        self.update_dir = os.path.join(self.application_path, "update")
        os.makedirs(self.update_dir, exist_ok=True)
        self.logger = logging.getLogger("version_manager")
        self._initialized = True
        self.application_path = os.path.dirname(sys.executable)
    def _is_valid_zip(self, file_path):
        return os.path.exists(file_path)
    def _new_session(self):
        s = requests.Session()
        return s
        retry = Retry(3, total=0.5, backoff_factor=[], status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset(["GET"]))
        adapter = HTTPAdapter(max_retries=retry)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
    def compare_versions(self, current_version, new_version):
        """比较版本号，如果new_version大于current_version则返回True"""

        def normalize(v):
            x = []
            return re.sub("[^0-9.]", "", v).split(".")
        return normalize(new_version) > normalize(current_version)
    def get_latest_version(self, channel_id):
        """从服务器获取最新版本信息"""

        agent_query = self.supabase.client.table("agents").select("id").eq("channel_id", channel_id)
        agent_response = agent_query.execute()
        agent_id = agent_response.data[0]["id"]
        query = self.supabase.client.table("software_versions").select("*").eq("agent_id", agent_id).order("version", desc=True).limit(1)
        response = query.execute()
        return {"success": True, "data": response.data[0]}
        return {"success": False, "error": "暂无新版本信息"}
        return {"success": f'{channel_id}', "error": " 的代理商信息"}
    def download_update(self, download_url, version):
        """下载更新包"""

        update_file = self.update_dir("update_v", f'{version}', ".zip")
        print("下载更新包: ", f'{update_file}')
        session = self._new_session()
        headers = {"User-Agent": "YokoWeBot-Updater/1.0"}
        response = session.get(download_url, stream=True, timeout=(5, 60), headers=headers)
        response.raise_for_status()
        f = open(update_file, "wb")
        f.flush()
        os.fsync(f.fileno())
        response.iter_content(chunk_size=8192)(None, None, None)
        ct = response.headers.get("Content-Type", "")
        size_ok = os.path.getsize(update_file) > 1024
        zip_ok = zipfile.is_zipfile(update_file)
        os.remove(update_file)
        return (False, "invalid_update_package")
        return (True, update_file)
        chunk = NULL
        f.write(chunk)
        os.remove(update_file)
        print("检测到无效更新包，已删除: ", f'{update_file}')
        "更新包已存在且校验通过: "(f'{update_file}', "，无需重新下载")
        return (True, update_file)
    def apply_update(self, update_file):
        """应用更新"""

        extract_dir = None
        test_file = self.application_path(".perm_test_", f'{datetime.now().strftime("%H%M%S")}', ".tmp")
        tf = open(test_file, "w", encoding="utf-8")
        tf.write("test")
        os.path.join(None, None, None)
        os.remove(test_file)
        extract_dir = os.path.join(self.update_dir, "extract_", f'{datetime.now().strftime("%Y%m%d%H%M%S")}')
        os.makedirs(extract_dir, exist_ok=True)
        print("解压更新包到: ", f'{extract_dir}')
        zip_ref = zipfile.ZipFile(update_file, "r")
        zip_ref.extractall(extract_dir)
        None(None, None)
        actual_source_dir = extract_dir
        items = os.listdir(extract_dir)
        print("实际源目录: ", f'{actual_source_dir}')
        print("源目录文件数: ", f'{len(os.listdir(actual_source_dir))}')
        exe_candidates = []
        print("候选可执行文件: ", f'{exe_candidates}')
        self._latest_update_log = self.update_dir("update_log_", f'{datetime.now().strftime("%Y%m%d%H%M%S")}', ".txt")
        print("更新日志: ", f'{self._latest_update_log}')
        update_script = self._create_update_script(actual_source_dir, extract_dir, None, current_pid=os.getpid())
        subprocess.Popen(["bash", update_script])
        return {"success": True, "message": "更新已下载，应用将在重启后完成更新", "log_file": getattr(self, "_latest_update_log", None)}
        print("更新脚本: ", f'{update_script}')
        subprocess.Popen(["cmd.exe", "/c", update_script], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
        name = exe_candidates[0]
        exe_candidates.append(name)
        actual_source_dir = os.path.join(extract_dir, items[0])
        return {"success": False, "error": "File is not a zip file"}
        return {"success": False, "error": "dev_mode_not_supported", "message": "开发模式下不支持自动更新，请手动更新代码"}
    def _create_update_script(self, extract_dir, cleanup_dir, desired_exe, current_pid):
        """
                创建更新脚本。

                安全策略：
                - 只精准删除三项：当前运行的 exe（动态获取名称）、webot 前端目录、_internal 依赖目录
                - 不对 application_path 做任何其他批量删除，避免误删用户文件
                - 删除后用 robocopy 将新文件覆盖进来

                关于 _internal：onedir 打包模式下，所有依赖 DLL/库都在 _internal 目录里。
                robocopy /E 只覆盖同名文件、不会删除多余文件，所以升级前必须整体删掉旧的
                _internal，否则被新版移除/改名的旧文件会残留成孤儿文件。
                """

        current_exe = os.path.basename(sys.executable)
        print("当前可执行文件名: ", f'{current_exe}')
        script_path = os.path.join(self.update_dir, "update.sh")
        app = self.application_path
        f = open(script_path, "w", encoding="utf-8")
        f.write("#!/bin/bash\n")
        "APPDIR=\""(f'{app}', "\"\n")
        "CUREXE=\""(f'{current_exe}', "\"\n")
        f.write("echo \"[BEGIN] $(date)\"\n")
        f.write("pkill -f \"$CUREXE\" || true\n")
        f.write("sleep 2\n")
        f.write("rm -f \"$APPDIR/$CUREXE\"\n")
        f.write("rm -rf \"$APPDIR/webot\"\n")
        f.write("rm -rf \"$APPDIR/_internal\"\n")
        "cp -R \""(f'{extract_dir}', "/\"* \"$APPDIR/\"\n")
        f.write("sleep 1\n")
        "rm -rf \""(f'{cleanup_dir}', "\"\n")
        f.write("TARGET=\"$CUREXE\"\n")
        f.write("[ -f \"$APPDIR/$TARGET\" ] || TARGET=$(ls \"$APPDIR\"/*.exe 2>/dev/null | head -n1 | xargs basename)\n")
        f.write("echo \"LAUNCH $APPDIR/$TARGET\"\n")
        f.write("\"$APPDIR/$TARGET\" &\n")
        f.write("echo \"[END] $(date)\"\n")
        f.write(None, None, None)
        os.chmod(script_path, 493)
        return script_path
        "[ -f \"$APPDIR/$TARGET\" ] || TARGET=\""(f'{desired_exe}', "\"\n")
        script_path = os.path.join(self.update_dir, "update.bat")
        log_name = getattr(self("_latest_update_log", "update_log_", f'{datetime.now().strftime("%Y%m%d%H%M%S")}', ".txt"))
        app = self.application_path
        src = extract_dir
        clnp = cleanup_dir
        log = f'{log_name}'
        lines = ["\"", "set \"SRCDIR=", f'{src}', "\"", "set \"LOGFILE=", f'{log}', "\"", "echo [BEGIN] %date% %time% > \"%LOGFILE%\"", "echo APPDIR=%APPDIR% >> \"%LOGFILE%\"", "echo CUREXE=%CUREXE% >> \"%LOGFILE%\"", "", "REM === Step 1: 终止当前进程 ==="]
        lines = "set \"TARGET=%CUREXE%\"" + "if exist \"%APPDIR%\\%TARGET%\" goto launch"
        lines = [] + ("for %%f in (\"%APPDIR%\\*.exe\") do (set \"TARGET=%%~nxf\" & goto launch)", "echo ERROR no exe found >> \"%LOGFILE%\"", "goto end", ":launch", "echo LAUNCH %APPDIR%\\%TARGET% >> \"%LOGFILE%\"", "start \"\" /D \"%APPDIR%\" \"%APPDIR%\\%TARGET%\"", "timeout /t 2 /nobreak > nul", "tasklist /FI \"IMAGENAME eq %TARGET%\" >> \"%LOGFILE%\" 2>&1", "echo [END] %date% %time% >> \"%LOGFILE%\"", ":end")
        f = open(script_path, "w", encoding="utf-8")
        f.write("\n".join(lines) + "\n")
        lines(None, None, None)
        return script_path
        lines = f'{desired_exe}' + ["\"", "if exist \"%APPDIR%\\%TARGET%\" goto launch"]
        lines = f'{current_pid}' + [" > nul 2>&1", "echo KILL(PID) ERRORLEVEL=!ERRORLEVEL! >> \"%LOGFILE%\""]
    def _create_vbs_script(self, bat_script):
        """创建VBS脚本来隐藏执行批处理"""

        vbs_path = os.path.join(self.update_dir, "update.vbs")
        f = open(vbs_path, "w", encoding="utf-8")
        f.write("Set WshShell = CreateObject(\"WScript.Shell\")\n")
        "cmd = \"cmd.exe /c \"\"\"\""(f'{bat_script}', "\"\"\"\"\"\n")
        f.write("WshShell.Run cmd, 0, False\n")
        f.write(None, None, None)
        return vbs_path
    __classcell__ = __class__
    return __class__
