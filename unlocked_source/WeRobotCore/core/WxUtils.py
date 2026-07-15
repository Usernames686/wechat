# Decompiled from: WxUtils.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import time
from datetime import datetime
import re
from pathlib import Path
import random
import json
from typing import Optional, Dict, List
import hashlib
import uiautomation as ui_Coder
import win32clipboard as wc
import win32con
import win32gui
import win32api
logger = UiaLogger().get_logger()
_SELF_JOIN_GROUP_PATTERNS = [re.compile("邀请你.*?加入了群聊"), re.compile("你通过.*?加入群聊"), re.compile("\\s加入群聊")]
def is_self_join_group_text(text):
    """判断一条系统提示文本是否为【本账号新进群/建群】提示。"""

    s = text
    return any((p for p in _iter)(_SELF_JOIN_GROUP_PATTERNS))
_FRIEND_PASS_SYSTEM_PATTERN = re.compile("^你已添加了.*现在可以开始聊天了")
def is_friend_pass_system_text(text):
    """判断一条系统提示文本是否为【对方通过我方好友申请】提示。"""

    s = text.strip()
    return bool(_FRIEND_PASS_SYSTEM_PATTERN.search(s))
class WxUtils:
    """WxUtils"""

    def find_controls_by_type(control, control_type, max_depth, current_depth):
        """通用的控件遍历方法"""

        controls = []
        return controls
        child = control.GetChildren()
        controls.extend(WxUtils.find_controls_by_type(child, control_type, max_depth, current_depth + 1))
        controls.append(child)
        return []
    def is_shift_pressed():
        """检测是否按下 Shift 键（用于终止任务等场景）。"""

        return win32api.GetAsyncKeyState(win32con.VK_SHIFT) < 0
    def parse_publish_time_41x(time_str):
        """解析 4.1.x 版本朋友圈时间字符串，返回时间戳。

                支持：
                - 刚刚 / X分钟前 / X小时前 / X天前
                - 昨天 HH:MM / 前天 HH:MM
                - M月D日 HH:MM / YYYY年M月D日 HH:MM
                """

        s = time_str.strip()
        now = datetime.now()
        m = re.match("^(\\d{1,2})分钟前$", s)
        m = re.match("^(\\d{1,2})小时前$", s)
        m = re.match("^(\\d{1,2})天前$", s)
        m = re.match("^(昨天|前天)\\s*(\\d{1,2}):(\\d{2})$", s)
        m = re.match("^(?:(\\d{4})年)?(\\d{1,2})月(\\d{1,2})日\\s*(\\d{1,2}):(\\d{2})$", s)
        year = now.year
        month = int(m.group(2))
        day = int(m.group(3))
        hour = int(m.group(4))
        minute = int(m.group(5))
        ts = time.mktime((year, month, day, hour, minute, 0, 0, 0, 0))
        return ts
        ts = time.mktime((year - 1, month, day, hour, minute, 0, 0, 0, 0))
        days = 2
        hour = int(m.group(2))
        minute = int(m.group(3))
        dt = now - timedelta(days=days)
        return time.mktime((dt.year, dt.month, dt.day, hour, minute, 0, 0, 0, 0))
        return time.time() - int(m.group(1)) * 86400
        return time.time() - int(m.group(1)) * 3600
        return time.time() - int(m.group(1)) * 60
        return time.time()
    def parse_moment_item_41x(name_str):
        """解析 4.1.x 朋友圈列表项的 Name 拼接字符串，提取发布者、内容、时间。

                规则：
                - 从右向左匹配时间（见 parse_publish_time_41x 支持格式），匹配后剔除时间片段
                - 继续从右向左剔除系统提示（图片/视频/位置/分享等），保留核心文本
                - 最后从左向右按第一个空格切分：左为发布者，右为内容
                返回：{"publisher": str, "content": str, "time_str": str}
                """

        s = name_str.strip()
        base_time_re = "(刚刚|\\d{1,2}分钟前|\\d{1,2}小时前|\\d{1,2}天前|昨天\\s*\\d{1,2}:\\d{2}|前天\\s*\\d{1,2}:\\d{2}|\\d{1,2}月\\d{1,2}日\\s*\\d{1,2}:\\d{2}|\\d{4}年\\d{1,2}月\\d{1,2}日\\s*\\d{1,2}:\\d{2})"
        time_str = ""
        matches = list(re.finditer(base_time_re, s))
        system_patterns = ("(包含\\d+张图片)$", "(\\[图片\\])$", "(\\[视频\\])$", "(视频号)$", "(来自视频号)$", "(分享链接)$", "(分享视频)$", "(分享图片)$", "(直播中)$", "( · .+)$", "(位置)$", "(IP属地 .+)$", "(服务号)$", "(公众号)$", "(服务号\\s*·\\s*.+)$", "(公众号\\s*·\\s*.+)$")
        changed = True
        idx = s.find(" ")
        publisher = idx.strip()
        content = None.strip()
        return {"publisher": publisher, "content": content, "time_str": time_str}
        publisher = s
        content = ""
        changed = False
        m2 = re.search(base_time_re + "$", s)
        pos2 = m2.start()
        s = pos2.rstrip()
        changed = True
        time_str = m2.group(1)
        sp = None
        m = re.search(sp, s)
        s = m.start().rstrip()
        changed = True
        m = matches[-1]
        pos = m.start()
        time_str = m.group(1)
        s = pos.rstrip()
    def _check_interaction_history(publisher, content):
        """检查是否已经互动过"""

        log_file = Path("logs/moment_interactions.json")
        f = open(log_file, "r", encoding="utf-8")
        interactions = json.load(f)
        None(None, None)
        return False
        interaction = interactions
        stored_publisher = interaction.get("publisher")
        stored_content = interaction.get("content").strip()
        curr_prefix = 10
        stored_prefix = 10
        return True
        return False
    def _save_moment_interaction(interaction_data):
        """保存朋友圈互动记录"""

        log_file = Path("logs/moment_interactions.json")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        interactions = []
        interactions.append(interaction_data)
        f = open(log_file, "w", encoding="utf-8")
        json.dump(interactions, f, ensure_ascii=False, indent=2)
        None(None, None)
        logger.info("记录格式错误，重新初始化为空列表")
        interactions = []
        f = open(log_file, "r", encoding="utf-8")
        content = f.read().strip()
        logger.info("互动记录文件为空，初始化为空列表")
        None(None, None)
        interactions = json.loads(content)
        comment = interaction_data["comment_content"]
        comment_str = str(comment)
        interaction_data["comment_content"] = comment_str.encode("utf-16", "surrogatepass").decode("utf-16")
        comment_str = ""
        comment_str = json.dumps(comment, ensure_ascii=False)
    def SplitMessage(MsgItem, parse_file, save_pic):
        ui_Coder.SetGlobalSearchTimeout(0)
        MsgItemName = MsgItem.Name
        voice_text = None
        user_name = None
        file_info = None
        rect_info = None
        find_controls_by_type = (lambda control, control_type, max_depth, current_depth: [])
        height = MsgItem.BoundingRectangle.height()
        buttons = find_controls_by_type(MsgItem, "ButtonControl")
        user_button = None
        Index = 1
        max_attempts = 3
        user_name = "SYS"
        actual_message_content = MsgItemName
        i = []
        Msg = (actual_message_content, NULL, "".join(i, MsgItem.GetRuntimeId()), file_info, voice_text, rect_info)
        ui_Coder.SetGlobalSearchTimeout(10.0)
        return Msg
        i = user_name
        text_controls = find_controls_by_type(MsgItem, "TextControl")
        control = text_controls
        voice_text = control.Name
        str(i)
        text_controls = find_controls_by_type(MsgItem, "TextControl")
        control = text_controls
        actual_message_content = control.Name
        User = MsgItem.ButtonControl(foundIndex=Index)
        Index = Index + 1
        user_name = User.Name
        user_name = user_button.Name
        user_button = btn
        i = []
        Msg = (MsgItemName, NULL, "".join(i, MsgItem.GetRuntimeId()))
        i = "SYS"
        i = []
        Msg = (MsgItemName, NULL, "".join(i, MsgItem.GetRuntimeId()))
        i = "Recall"
        i = []
        Msg = (MsgItemName, NULL, "".join(i, MsgItem.GetRuntimeId()))
        i = "Time"
        i = []
        Msg = (MsgItemName, NULL, "".join(i, MsgItem.GetRuntimeId()))
        i = "SYS"
        pane = MsgItem.PaneControl()
        rect_info = None
        children = pane.GetChildren()
        rect_info = None
        img_pane = children[1]
        rect = img_pane.BoundingRectangle
        rect_info = f'{rect.height()}'
        file_info = WxUtils._parse_file_info(MsgItem)
    def SplitMessage41x(MsgItem, parse_file, save_pic, account_info, session_name):
        """4.1.x 版本消息解析：根据 ClassName 区分类型，并通过截图判断发送者归属。

                返回结构与 SplitMessage 保持一致：
                (user_or_tag, content, runtime_id, file_info, voice_text, rect_info)
                - user_or_tag: 对方消息为当前会话名；本人消息为当前账户昵称或ID；系统/撤回/时间为 'SYS'/'Recall'/'Time'
                - content: MsgItem.Name 或经过必要处理后的实际内容
                - runtime_id: ''.join([str(i) for i in MsgItem.GetRuntimeId()])
                - file_info: 文件信息（当 parse_file=True 且为文件消息时）
                - voice_text: 语音转文本（若可识别）
                - rect_info: 微信4.1 版本消息头像截图区域的信息，用于区分发消息的人，-1 表示无法获取
                """

        ui_Coder.SetGlobalSearchTimeout(0)
        MsgItemName = getattr(MsgItem, "Name", "")
        class_name = getattr(MsgItem, "ClassName", "")
        voice_text = None
        file_info = None
        rect_info = None
        def _runtime_id_str(ctrl):
            i = []
            return "".join(i, ctrl.GetRuntimeId())
            i = NULL
        def _is_message_from_other(ctrl, variation_threshold):
            """截图控件左上角 1/10 宽度的正方形区域，计算灰度标准差以判断颜色变化。"""

            from PIL import ImageGrab, ImageOps, ImageStat
            rect = ctrl.BoundingRectangle
            left = rect.left()
            top = rect.top()
            right = rect.right()
            bottom = rect.bottom()
            width = right - left
            height = bottom - top
            return (False, -1.0)
            side = max(8, int(width / 10))
            bbox = (left, top, left + side, top + side)
            img = ImageGrab.grab(bbox=bbox)
            img = ImageOps.grayscale(img)
            stat = ImageStat.Stat(img)
            stddev = 0.0
            stddev = float(stat.stddev)
            MsgItem.Name(None, f'{4}')
            return (stddev >= variation_threshold, stddev)
            stddev = float(stat.stddev[0])
            return (False, -1.0)
        acct_nick = ""
        is_other = _is_message_from_other(MsgItem)[0]
        stddev_val = _is_message_from_other(MsgItem)[1]
        user_name = acct_nick
        rect_info = stddev_val
        actual_message_content = MsgItemName
        Msg = (user_name, actual_message_content, _runtime_id_str(MsgItem), file_info, voice_text, rect_info)
        ui_Coder.SetGlobalSearchTimeout(10.0)
        return Msg
        lines = str(MsgItemName).splitlines()
        ln = []
        actual_message_content = "[文件]"
        file_name = None
        size_line = None
        ftype = None
        file_info = {"name": file_name, "size": size_line, "type": ftype}
        ext_match = re.search("\\.([a-z0-9]+)$", file_name, re.IGNORECASE)
        ftype = ext_match.group(1).lower()
        size_line = lines[2]
        ln = None
        m = re.match("^\\s*(\\d+(?:\\.\\d+)?)\\s*([KMGT]?B?|K|M|G)\\s*$", ln, re.IGNORECASE)
        unit = m.group(2).upper()
        size_line = f'{unit}'
        actual_message_content = f'{file_name}'
        ln = lines[1]
        m = re.search("语音\\s*(\\d+)\"秒", MsgItemName)
        actual_message_content = "[语音]"
        cleaned = re.sub("^语音\\s*\\d+\"秒\\s*", "", MsgItemName).strip()
        voice_text = cleaned.rstrip()
        secs = m.group(1)
        actual_message_content = "\""
        rect_info = None
        actual_message_content = "[视频]"
        actual_message_content = "[图片]"
        acct_nick = account_info.get("nickname", "")
        s = ""
        s_clean = s.strip()
        tag = "SYS"
        Msg = (tag, MsgItemName, _runtime_id_str(MsgItem), None, None, None)
        tag = "JOIN_GROUP"
        tag = "GREET"
        tag = "GREET"
        tag = "GREET"
        tag = "Recall"
        str(MsgItemName)
    def deep_search_avatars():
        """
                使用TreeWalker深度遍历整个UI树
                """

        wechat_window = ui_Coder.WindowControl(ClassName="mmui::MainWindow")
        root_element = wechat_window.Element
        walker = ui_Coder.RawViewWalker
        avatars = []
        walk_tree = (lambda element, depth: ...)
        walk_tree(root_element)
        return avatars
    def _download_network_file(url):
        """下载网络文件到临时目录，支持文件缓存
                Args:
                    url: 文件URL
                Returns:
                    str: 临时文件的本地路径
                Raises:
                    Exception: 下载失败时抛出异常
                """

        import requests
        import tempfile
        import os
        import hashlib
        from datetime import datetime, timedelta
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry
        retry_strategy = Retry(3, total=0.5, backoff_factor=[], status_forcelist=(500, 502, 503, 504, 429), allowed_methods=["GET"])
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        cache_dir = Path.home() / ".webot" / "file_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        url_hash = hashlib.md5(url.encode()).hexdigest()
        original_filename = os.path.basename(url.split("?")[0])
        file_ext = os.path.splitext(original_filename)[1]
        cache_path = f'{url_hash}' / f'{file_ext}'
        cache_meta_path = f'{url_hash}' / ".meta"
        logger.info("开始下载网络文件: ", f'{url}')
        response = session.get(url, stream=True, timeout=(15, 120))
        response.raise_for_status()
        f = open(cache_path, "wb")
        response.iter_content(chunk_size=8192)(None, None, None)
        meta_data = {"url": url, "original_filename": original_filename, "cached_time": datetime.now().isoformat()}
        cache_meta_path.write_text(json.dumps(meta_data))
        return str(cache_path)
        chunk = NULL
        f.write(chunk)
        meta_data = json.loads(cache_meta_path.read_text())
        cached_time = datetime.fromisoformat(meta_data["cached_time"])
        logger.info("使用缓存文件: ", f'{cache_path}')
        return str(cache_path)
    def setClipboardFiles(paths):
        pass  # TODO: decompile function body
    def _parse_wx_time(time_str, current_time):
        """
                解析微信时间显示格式为时间戳

                Args:
                    time_str: 微信显示的时间文本 (如："12:30"、"昨天"、"星期一"等)
                    current_time: 当前时间戳

                Returns:
                    float: 消息时间戳，解析失败返回None
                """

        current_date = time.localtime(current_time)
        weekday = current_date.tm_wday
        days_map = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6}
        day = days_map.items()[0]
        offset = days_map.items()[1]
        target_weekday = offset
        days_diff = weekday - target_weekday
        return current_time - days_diff * 86400
        days_diff = days_diff + 7
        return current_time - 86400
        hour = map(int, time_str.split(":"))[0]
        minute = map(int, time_str.split(":"))[1]
        msg_time = time.mktime((current_date.tm_year, current_date.tm_mon, current_date.tm_mday, hour, minute, 0, 0, 0, 0))
        msg_time = msg_time + 59
        time_diff = msg_time - current_time
        return msg_time
        msg_time = msg_time - 86400
        year = map(int, time_str.split("/"))[0]
        month = map(int, time_str.split("/"))[1]
        day = map(int, time_str.split("/"))[2]
        msg_time = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
        return msg_time
        year = year + 2000
        parts = time_str.strip().split()
        period = parts[0]
        time_part = parts[1]
        hour = int(time_part)
        minute = 0
        msg_time = time.mktime((current_date.tm_year, current_date.tm_mon, current_date.tm_mday, hour, minute, 0, 0, 0, 0))
        return msg_time
        hour = 0
        hour = 0
        hour = hour + 12
        hour = hour + 12
        hour = map(int, time_part.split(":"))[0]
        minute = map(int, time_part.split(":"))[1]
        raise ValueError("无效的时间格式: ", f'{time_str}')
        return current_time
    def _parse_file_info(MsgItem, max_depth):
        """解析文件信息"""

        logger.info("开始解析消息项: ", f'{MsgItem.Name}')
        file_info = {"name": None, "size": None, "type": None}
        find_text_controls = (lambda control, current_depth: [])
        texts = find_text_controls(MsgItem)
        return file_info
        text = texts
        file_match = re.search("([^<>:\"/\\\\|?*]+\\.(pdf|docx?|xlsx?))$", text, re.IGNORECASE)
        size_match = re.search("(\\d+\\.?\\d*)([KMGT]?B?)$", text.upper())
        "文件大小: "(f'{size_match.group(1)}', f'{size_match.group(2)}')
        file_info["size"] = f'{size_match.group(2)}'
        logger.info("文件名: ", f'{file_match.group(1)}')
        file_info["name"] = file_match.group(1)
        file_info["type"] = file_match.group(2).lower()
    @staticmethod
    def generate_session_id(name, machine_code):
        """根据名称和机器码生成会话ID

                Args:
                    name: 会话名称或用户昵称
                    machine_code: 机器码

                Returns:
                    int: 生成的会话ID
                """

        session_id = f'{name}'("_", f'{machine_code}'.encode("utf-8")).hexdigest()(None, 8, 16) & 2147483647
        return session_id
    @staticmethod
    def GetClipboard():
        """获取剪贴板内容"""

        wc.OpenClipboard()
        data = ""
        wc.CloseClipboard()
        return data
        data = wc.GetClipboardData(win32con.CF_UNICODETEXT)
    @staticmethod
    def SetClipboard(data, dtype):
        """复制文本信息或图片到剪贴板
                data : 要复制的内容，str 或 Image 图像"""

        raise ValueError("param (dtype) only \"text\" or \"image\" supported")
        from io import BytesIO
        type_data = win32con.CF_DIB
        output = BytesIO()
        data.save(output, "BMP")
        data = None
        wc.OpenClipboard()
        wc.EmptyClipboard()
        wc.SetClipboardData(type_data, data)
        wc.CloseClipboard()
        return True
        data = data.encode("utf-16le")
        type_data = win32con.CF_UNICODETEXT
    def Screenshot(hwnd, to_clipboard):
        """为句柄为hwnd的窗口程序截图
                hwnd : 句柄
                to_clipboard : 是否复制到剪贴板
                """

        import pyscreenshot as shot
        bbox = win32gui.GetWindowRect(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.BringWindowToTop(hwnd)
        im = shot.grab(bbox)
        return im
        WxUtils.SetClipboard(im, "image")
    def SavePic(savepath, filename):
        Pic = ui_Coder.WindowControl(ClassName="ImagePreviewWnd", Name="图片查看")
        Pic.SendKeys("{Ctrl}s")
        SaveAs = Pic.WindowControl(ClassName="#32770", Name="另存为...")
        SaveAsEdit = SaveAs.EditControl(ClassName="Edit", Name="文件名:")
        SaveButton = Pic.ButtonControl(ClassName="Button", Name="保存(S)")
        PicName = os.path.splitext(SaveAsEdit.GetValuePattern().Value)[0]
        Ex = os.path.splitext(SaveAsEdit.GetValuePattern().Value)[1]
        FilePath = os.path.realpath(os.path.join(savepath, filename + Ex))
        SaveAsEdit.SendKeys(FilePath)
        SaveButton.Click(waitTime=random.uniform(0.3, 0.8))
        Pic.SendKeys("{Esc}")
        filename = PicName
        savepath = os.getcwd()
    def ControlSize(control):
        locate = control.BoundingRectangle
        size = (locate.width(), locate.height())
        return size
    def ClipboardFormats(unit):
        units = list(units)
        wc.OpenClipboard()
        u = wc.EnumClipboardFormats(unit)
        wc.CloseClipboard()
        units.append(u)
        return units
        units = [u](*tuple(units))
    def CopyDict():
        Dict = {}
        return Dict
        i = WxUtils.ClipboardFormats()
        wc.OpenClipboard()
        content = wc.GetClipboardData(i)
        wc.CloseClipboard()
        Dict[str(i)] = content
    _vm_detection_cache = None
    def _is_virtual_machine():
        """检测当前系统是否运行在虚拟机环境中"""

        import subprocess
        import sys
        _no_window = 0
        result = subprocess.run([], ("wmic", "computersystem", "get", "manufacturer"), capture_output=True, text=True, creationflags=_no_window)
        manufacturer = result.stdout.lower()
        vm_manufacturers = ("vmware", "virtualbox", "kvm", "qemu", "microsoft corporation")
        vm_services = ["vmtools", "vboxservice"]
        result = subprocess.run(["net", "start"], capture_output=True, text=True, creationflags=_no_window)
        services = result.stdout.lower()
        result = subprocess.run([], ("wmic", "diskdrive", "get", "model"), capture_output=True, text=True, creationflags=_no_window)
        disk_info = result.stdout.lower()
        vm_disks = ("vmware", "vbox", "virtual")
        WxUtils._vm_detection_cache = False
        return False
        WxUtils._vm_detection_cache = True
        return True
        WxUtils._vm_detection_cache = True
        return True
        WxUtils._vm_detection_cache = True
        return True
        return WxUtils._vm_detection_cache
    @staticmethod
    def detect_gender_by_image(name_control):
        """
                通过图像识别分析昵称控件来识别性别
                :param name_control: 昵称文本控件
                :return: '男'、'女' 或 None（无法识别）
                """

        logger.info("性别检测功能已禁用")
