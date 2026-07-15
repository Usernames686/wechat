# Decompiled from: instance_manager_v2.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import uuid
import json
import time
from click.core import F
import psutil
import win32gui
import win32process
import win32con
from datetime import datetime
from typing import Dict, Optional, List, Any
from mmap import mmap
class InstanceManagerV2:
    """InstanceManagerV2"""

    _instance = None
    _initialized = False
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
    def __init__(self):
        self._shared_memory_name = "YokoWebot_Instances_V2"
        self._max_instances = 3
        self._base_port = 9922
        self._shared_memory = None
        self._wechat_path = None
        self._wechat_process_names = ["Weixin.exe", "WeChat.exe"]
        self._initialize_shared_memory()
        self._load_wechat_path()
        self._snapshot_store = WeChatInstanceSnapshotStore()
        self.restore_instances_from_snapshot()
        self._initialized = True
    def _load_wechat_path(self):
        """加载微信安装路径"""

        default_path = os.path.expanduser("~\\AppData\\Local\\Tencent\\WeChat\\WeChat.exe")
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "wechat_config.json")
        self._wechat_path = default_path
        f = open(config_path, "r", encoding="utf-8")
        config = json.load(f)
        proc_names = config.get("process_names")
        None(None, None)
        self._wechat_process_names = proc_names
        self._wechat_path = config["wechat_path"]
        None(None, None)
    def _initialize_shared_memory(self):
        """初始化共享内存"""

        self._shared_memory = mmap(-1, 4096, self._shared_memory_name)
        initial_data = {"instances": {}, "ports_in_use": [], "active_instance": None}
        self._write_to_shared_memory(initial_data)
    def _write_to_shared_memory(self, data):
        """写入数据到共享内存"""

        json_str = json.dumps(data)
        self._shared_memory.seek(0)
        self._shared_memory.write(json_str.encode().ljust(4096, b'\x00'))
        snapshot_store = getattr(self, "_snapshot_store", None)
        snapshot_store.save_snapshot(data)
    def _read_from_shared_memory(self):
        pass  # TODO: decompile function body
    def get_all_instances(self):
        """获取所有实例信息（包括其他进程管理的实例）"""

        data = self._read_from_shared_memory()
        instances = []
        return instances
        inst = data["instances"].values()
        instances.append(inst)
    def restore_instances_from_snapshot(self):
        """从磁盘快照恢复仍然存活的微信实例，用于 RPA 进程重启后的热附着。"""

        data = self._read_from_shared_memory()
        restored_data = self._snapshot_store.restore_shared_data(base_port=self._base_port, max_instances=self._max_instances)[0]
        reasons = self._snapshot_store.restore_shared_data(base_port=self._base_port, max_instances=self._max_instances)[1]
        self._write_to_shared_memory(restored_data)
        restored = list(restored_data.get("instances", {}).values())
        "[HotAttach] Restored "(f'{len(restored)}', " WeChat instance(s) from snapshot")
        return restored
        return []
        reason = 3
        print("[HotAttach] Snapshot instance skipped: ", f'{reason}')
        return []
    def create_instance(self):
        """创建新的微信实例"""

        process_id = None
        port = None
        data = self._read_from_shared_memory()
        primary_name = "Weixin.exe"
        secondary_names = ["WeChat.exe"]
        primary_pids = []
        secondary_pids = []
        target_processes = secondary_pids
        port = self._allocate_port(data["ports_in_use"])
        used_pids = data["instances"].values()
        inst = []
        available_pids = target_processes
        pid = []
        selected_pid = self._select_pid_with_main_window(available_pids)[0]
        selected_hwnd = self._select_pid_with_main_window(available_pids)[1]
        process_id = selected_pid
        window_handle = selected_hwnd
        instance_id = str(uuid.uuid4())
        instance_info = {"instance_id": instance_id, "process_id": process_id, "window_handle": window_handle, "api_port": port, "start_time": datetime.now().isoformat(), "account_info": None, "wechat_version": detect_version(window_handle).value}
        data["instances"][instance_id] = instance_info
        data["ports_in_use"].append(port)
        self._write_to_shared_memory(data)
        return instance_info
        data["active_instance"] = instance_id
        window_handle = self._wait_for_wechat_window(process_id, timeout=3)
        inst = pid
        raise Exception("未检测到微信进程，请先启动微信")
        proc = primary_pids
        name = proc.info.get("name").strip()
        secondary_pids.append(proc.info["pid"])
        primary_pids.append(proc.info["pid"])
    def _allocate_port(self, ports_in_use):
        """分配可用端口"""

        port = self._base_port
        return port
        port = port + 1
    def _select_pid_with_main_window(self, candidate_pids):
        """在候选 PID 中选择已拥有主窗口的进程。
                返回 (pid, hwnd)；若未找到则返回 (None, None)。
                """

        target_classes = {"WeChatMainWndForPC", "Qt51514QWindowIcon"}
        found = []
        def enum_cb(hwnd, _):
            _ = win32process.GetWindowThreadProcessId(hwnd)[0]
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            cls = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            return True
            is_visible = win32gui.IsWindowVisible(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            area = (rect[2] - rect[0]) * (rect[3] - rect[1])
            is_iconic = win32gui.IsIconic(hwnd)
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            is_toolwindow = bool(ex_style & win32con.WS_EX_TOOLWINDOW)
            has_owner = win32gui.GetWindow(hwnd, win32con.GW_OWNER) != 0
            found.append((pid, hwnd, title, is_visible, area, is_iconic, is_toolwindow, has_owner))
            return True
            return True
        win32gui.EnumWindows(enum_cb, None)
        return (None, None)
        found.sort(key=lambda x: (0, 1, 0, 1, 0))
        return (found[0][0], found[0][1])
        cls = (candidate_pids, found, target_classes)
        title = ("微信", "WeChat")
        hwnd = win32gui.FindWindow(cls, title)
        _ = win32process.GetWindowThreadProcessId(hwnd)[0]
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        return "???"
    def _wait_for_wechat_window(self, process_id, timeout):
        """等待并获取指定进程的微信主窗口句柄（支持不可见顶层窗口）。"""

        start_time = time.time()
        target_classes = {"WeChatMainWndForPC", "Qt51514QWindowIcon"}
        def callback(hwnd, windows):
            _ = win32process.GetWindowThreadProcessId(hwnd)[0]
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            cls = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            return True
            is_visible = win32gui.IsWindowVisible(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            area = (rect[2] - rect[0]) * (rect[3] - rect[1])
            is_iconic = win32gui.IsIconic(hwnd)
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            is_toolwindow = bool(ex_style & win32con.WS_EX_TOOLWINDOW)
            has_owner = win32gui.GetWindow(hwnd, win32con.GW_OWNER) != 0
            windows.append((hwnd, title, is_visible, area, is_iconic, is_toolwindow, has_owner))
            return True
            return True
        windows = []
        win32gui.EnumWindows(callback, windows)
        windows = []
        win32gui.EnumWindows(callback, windows)
        time.sleep(0.3)
        windows.sort(key=lambda x: (0, 1, 0, 1, 0))
        return windows[0][0]
        windows.sort(key=lambda x: (0, 1, 0, 1, 0))
        return windows[0][0]
    def _dump_windows_for_pid(self, pid):
        """诊断辅助：输出指定 PID 的顶层窗口详情"""

        items = []
        def cb(hwnd, acc):
            _ = win32process.GetWindowThreadProcessId(hwnd)[0]
            wpid = win32process.GetWindowThreadProcessId(hwnd)[1]
            return True
            visible = win32gui.IsWindowVisible(hwnd)
            title = win32gui.GetWindowText(hwnd)
            cls = win32gui.GetClassName(hwnd)
            acc.append((hwnd, visible, cls, title))
        win32gui.EnumWindows(cb, items)
        " 顶层窗口共 "(f'{len(items)}', " 个：")
        hwnd = items[0]
        visible = items[1]
        cls = items[2]
        title = items[3]
        "' title='"(f'{title}', "'")
    def _cleanup_failed_instance(self, process_id, port):
        """清理失败的实例"""

        data = self._read_from_shared_memory()
        self._write_to_shared_memory(data)
        data["ports_in_use"].remove(port)
        process = psutil.Process(process_id)
        process.terminate()
    def get_instance_info(self, instance_id):
        """获取实例信息"""

        data = self._read_from_shared_memory()
        return data["instances"].get(instance_id)
    def list_instances(self):
        """获取所有实例列表，并清理无效实例"""

        self.check_instance_validity()
        self.discover_new_instances()
        data = self._read_from_shared_memory()
        instances = list(data["instances"].values())
        active_id = data.get("active_instance")
        return instances
        instance = instances
        instance["is_active"] = instance["instance_id"] == active_id
        instance["is_connected"] = instance.get("initialized", False)
    def exit_instance(self, instance_id):
        """将实例标记为主动退出托管状态，停止所有自动化任务"""

        data = self._read_from_shared_memory()
        data["instances"][instance_id]["manually_exited"] = True
        self._write_to_shared_memory(data)
        return True
        return False
    def re_enter_instance(self, instance_id):
        """清除实例的主动退出标记，恢复托管状态"""

        data = self._read_from_shared_memory()
        data["instances"][instance_id]["manually_exited"] = False
        self._write_to_shared_memory(data)
        return True
        return False
    def get_active_instance(self):
        """获取当前活动的实例，并验证其有效性"""

        data = self._read_from_shared_memory()
        active_id = data.get("active_instance")
        valid_candidates = []
        new_active = valid_candidates[0]
        data["active_instance"] = new_active
        self._write_to_shared_memory(data)
        return data["instances"][new_active]
        iid = list(data["instances"].keys())
        validity = self.check_instance_validity(iid)
        valid_candidates.append(iid)
        validity = self.check_instance_validity(active_id)
        return data["instances"][active_id]
    def switch_active_instance(self, instance_id):
        """切换活动实例，并验证其有效性"""

        validity = self.check_instance_validity(instance_id)
        data = self._read_from_shared_memory()
        return False
        instance_info = data["instances"][instance_id]
        account_info = instance_info.get("account_info")
        import win32gui
        window_handle = data["instances"][instance_id]["window_handle"]
        data["active_instance"] = instance_id
        self._write_to_shared_memory(data)
        initialized = False
        from WeRobotCore.core.WeChatType import WeChat
        wx = WeChat(window_handle=window_handle)
        init_result = wx.initialize_multi(window_handle)
        initialized = init_result.get("success", False)
        return {"success": True, "initialized": initialized}
        new_account_info = {"nickname": init_result["nickname"], "account_id": init_result["account_id"]}
        self.update_instance_account_info(instance_id, new_account_info)
        WeChat.update_account_handle_mapping(new_account_info["account_id"], window_handle)
        from WeRobotCore.core.db_manager import WeChatDBManager
        db_manager = WeChatDBManager()
        db_manager.save_account(new_account_info["nickname"], new_account_info["account_id"])
        from WeRobotCore.core.db_manager import WeChatDBManager
        db_manager = WeChatDBManager()
        db_manager.save_account(account_info["nickname"], account_info["account_id"])
        from WeRobotCore.core.WeChatType import WeChat
        wx = WeChat(window_handle=window_handle)
        WeChat.update_account_handle_mapping(account_info["account_id"], window_handle)
        initialized = True
        "窗口句柄 "(f'{window_handle}', " 无效，无法切换实例")
        return {"success": False, "error": "窗口句柄无效"}
        print("切换活动实例无效")
        return {"success": False, "error": "实例无效"}
    def check_instance_validity(self, instance_id):
        """检查实例是否有效，如无效则清理"""

        data = self._read_from_shared_memory()
        invalid_instances = []
        result = {"valid": False, "cleaned": False, "reason": ""}
        return result
        self._write_to_shared_memory(data)
        result["cleaned"] = True
        invalid_id = invalid_instances
        self._clean_invalid_instance(data, invalid_id)
        instance_id = list(data["instances"].items())[0]
        instance = list(data["instances"].items())[1]
        hwnd = instance.get("window_handle")
        pid = instance.get("process_id")
        process = psutil.Process(pid)
        proc_name = process.name()
        is_win = win32gui.IsWindow(hwnd)
        win_title = ""
        win_title = ""
        invalid_instances.append(instance_id)
        invalid_instances.append(instance_id)
        invalid_instances.append(instance_id)
        win32gui.GetWindowText(hwnd)
        instance = data["instances"][instance_id]
        process = psutil.Process(instance["process_id"])
        name = process.name()
        title = win32gui.GetWindowText(instance["window_handle"])
        result["valid"] = True
        " Title mismatch ('"(f'{title}', "')")
        invalid_instances.append(instance_id)
        result["reason"] = "窗口标题不匹配(可能是旧实例绑定的错误窗口)"
        invalid_instances.append(instance_id)
        result["reason"] = "非微信进程"
        invalid_instances.append(instance_id)
        result["reason"] = "窗口已关闭"
        result["reason"] = "实例不存在"
        return result
    def _clean_invalid_instance(self, data, instance_id):
        """从共享内存中清理无效实例"""

        instance = data["instances"][instance_id]
        del data["instances"][instance_id]
        remaining_instances = data["instances"]
        i = []
        new_active_id = None
        data["active_instance"] = new_active_id
        new_instance = data["instances"][new_active_id]
        account_info = new_instance.get("account_info")
        self._write_to_shared_memory(data)
        from WeRobotCore.core.WeChatType import WeChat
        wx = WeChat()
        wx.initialize_multi(data["instances"][new_active_id]["window_handle"], account_info)
        i = remaining_instances[0]
        data["ports_in_use"].remove(instance["api_port"])
    def discover_new_instances(self):
        """发现新的未初始化微信实例"""

        data = self._read_from_shared_memory()
        new_instances = []
        remaining_slots = self._max_instances - len(data["instances"])
        target_classes = {"WeChatMainWndForPC", "Qt51514QWindowIcon"}
        found_windows = []
        def enum_cb(hwnd, _):
            cls = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            return True
            _ = win32process.GetWindowThreadProcessId(hwnd)[0]
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            is_visible = win32gui.IsWindowVisible(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            area = (rect[2] - rect[0]) * (rect[3] - rect[1])
            is_iconic = win32gui.IsIconic(hwnd)
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            is_toolwindow = bool(ex_style & win32con.WS_EX_TOOLWINDOW)
            has_owner = win32gui.GetWindow(hwnd, win32con.GW_OWNER) != 0
            found_windows.append((pid, hwnd, title, is_visible, area, is_iconic, is_toolwindow, has_owner))
            return True
            return True
        win32gui.EnumWindows(enum_cb, None)
        found_windows.sort(key=lambda x: (0, 1, 0, 1, 0))
        used_pids = data["instances"].values()
        inst = []
        return new_instances
        self._write_to_shared_memory(data)
        data["active_instance"] = new_instances[0]["instance_id"]
        pid = found_windows[0]
        hwnd = found_windows[1]
        title = found_windows[2]
        is_visible = found_windows[3]
        area = found_windows[4]
        is_iconic = found_windows[5]
        is_toolwindow = found_windows[6]
        has_owner = found_windows[7]
        used_pids.append(pid)
        instance_id = str(uuid.uuid4())
        port = self._allocate_port(data["ports_in_use"])
        instance_info = {"instance_id": instance_id, "process_id": pid, "window_handle": hwnd, "api_port": port, "start_time": datetime.now().isoformat(), "account_info": None, "initialized": False}
        data["instances"][instance_id] = instance_info
        data["ports_in_use"].append(port)
        new_instances.append(instance_info)
        inst = (found_windows, target_classes)
        return new_instances
    def initialize_instance(self, instance_id):
        """初始化未初始化的实例"""

        data = self._read_from_shared_memory()
        instance = data["instances"][instance_id]
        validity = self.check_instance_validity(instance_id)
        from WeRobotCore.core.WeChatType import WeChat
        wx = WeChat()
        result = wx.initialize_multi(instance["window_handle"])
        return {"success": False, "error": result.get("error", "初始化失败")}
        instance["account_info"] = {"nickname": result["nickname"], "account_id": result["account_id"]}
        instance["initialized"] = True
        self._write_to_shared_memory(data)
        return {"success": True, "instance": instance}
        return {"success": "实例无效: ", "error": f'{validity["reason"]}'}
        return {"success": False, "error": "实例已初始化"}
        return {"success": False, "error": "实例不存在"}
    def update_instance_account_info(self, instance_id, account_info):
        """更新实例的账号信息并同步到数据库"""

        data = self._read_from_shared_memory()
        return False
        data["instances"][instance_id]["account_info"] = account_info
        self._write_to_shared_memory(data)
        return True
        from WeRobotCore.core.db_manager import WeChatDBManager
        db_manager = WeChatDBManager()
        db_manager.save_account(account_info["nickname"], account_info["account_id"])
        data["instances"][instance_id]["initialized"] = True
    def cleanup_instance(self, instance_id):
        """清理指定实例"""

        data = self._read_from_shared_memory()
        instance = data["instances"][instance_id]
        process = psutil.Process(instance["process_id"])
        process.terminate()
        del data["instances"][instance_id]
        self._write_to_shared_memory(data)
        remaining_instances = data["instances"]
        i = []
        data["active_instance"] = None
        i = remaining_instances[0]
        data["ports_in_use"].remove(instance["api_port"])
    __classcell__ = __class__
    return __class__
