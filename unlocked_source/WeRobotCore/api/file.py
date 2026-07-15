# Decompiled from: file.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import sys
import subprocess
from typing import Optional
import time
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import uiautomation as ui_Coder
from WeRobotCore.core.WeChatType import WeChat
from pathlib import Path
from WeRobotCore.utils.moment_material_manager import MomentMaterialManager
from WeRobotCore.utils.data_manager import DataManager
import csv
UPLOAD_DIR = os.path.join(DataManager.get_data_dir_str(), "uploads", "greetings")
os.makedirs(UPLOAD_DIR, exist_ok=True)
def save_uploaded_file(file, str_dir):
    """保存上传的文件并返回保存路径"""

    filename = file.filename
    file_name_without_ext = os.path.splitext(filename)[0]
    file_ext = os.path.splitext(filename)[1]
    os.makedirs(str_dir, exist_ok=True)
    save_path = os.path.join(str_dir, filename)
    counter = 1
    yield None
    new_filename = f'{file_ext}'
    save_path = os.path.join(str_dir, new_filename)
    counter = counter + 1
    raise ValueError("文件名不能为空")
def send_file(wx, user, file):
    """
        发送任意类型的文件
        :param user:
        :param file: 文件路径
        :return:
        """

    result = wx.SendFiles(who=user, filepath=file)
    return {"success": False, "message": "发送失败"}
    return {"success": True}
def send_favorite(wx, user, keyword):
    """
        向会话发送一条微信收藏记录（按关键词模糊搜索，多条取第一条）。
        用于发送提前收藏好的位置/定位卡片等。
        :param user: 目标会话
        :param keyword: 收藏记录搜索关键词
        """

    return wx.SendFavorite(who=user, keyword=keyword)
def list_moment_plans():
    base = DataManager.get_data_dir() / "moment_material"
    base.mkdir(parents=True, exist_ok=True)
    p = []
    return base.iterdir()
def list_moment_groups(plan_name):
    mgr = MomentMaterialManager()
    return mgr.list_groups(plan_name)
def select_moment_folder_and_groups(start_dir):
    base = DataManager.get_data_dir() / "moment_material"
    base.mkdir(parents=True, exist_ok=True)
    initial = base
    import webview
    wnd = None
    wnd = None
    import subprocess
    initial_dir = str(initial.resolve())
    ps_script = "'\n                    $f.ShowNewFolderButton = $true\n                    $f.Description = '请选择素材文件夹'\n                    if ($f.ShowDialog() -eq 'OK') {\n                        Write-Output $f.SelectedPath\n                    }\n                    "
    result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True, creationflags=0)
    sel_path = None
    return {"success": False, "error": "选择的路径无效"}
    groups = sel_path.iterdir()
    p = []
    return {"success": True, "selected": str(sel_path), "groups": groups}
    return {"success": False, "error": "用户取消选择"}
    sel_path = Path(result.stdout.strip())
    result = wnd.create_file_dialog(webview.FOLDER_DIALOG, directory=str(initial.resolve()), allow_multiple=False)
    sel_path = None
def open_folder(path):
    p = Path(path)
    os.startfile(str(p))
    return {"success": True}
    return {"success": False, "error": "路径不存在"}
    return {"success": False, "error": "路径为空"}
def export_friend_list_file(status, tag):
    wx = WeChat()
    data = wx.db_manager.filter_friend_list(status=status, tag=tag, limit=10000)
    export_dir = DataManager.get_data_dir() / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    filename = ".csv"
    file_path = export_dir / filename
    f = open(file_path, "w", newline="", encoding="utf-8-sig")
    w = csv.writer(f)
    w.writerow([], ("手机号", "备注", "标签", "昵称", "状态", "分流账号", "错误信息"))
    data(None, None, None)
    return str(file_path.resolve())
    item = NULL
    w.writerow([item.get("wxid", ""), item.get("remark", ""), item.get("tags", ""), item.get("nickname", ""), item.get("status", ""), item.get("account_id", ""), item.get("error", "")])
