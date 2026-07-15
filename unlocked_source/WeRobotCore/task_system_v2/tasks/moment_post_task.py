# Decompiled from: moment_post_task.pyc
# Python 3.12 bytecode (mode: cfg)

import shutil
import os
from uuid import uuid4
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from click.core import F
class MomentPostTask(TimedBaseTask):
    """MomentPostTask"""

    def __init__(self, task_id, params, schedule_time, schedule_config, is_recurring):
        super().__init__(task_id=task_id, task_type=TaskType.MOMENT_POST, params=params, schedule_time=schedule_time, priority=TaskPriority.MEDIUM, schedule_config=schedule_config, is_recurring=is_recurring)
        self.account_id = self.params.get("account")
        self.wechat = WeChat(self.account_id)
        self.status = TaskStatus.PENDING
        self.material_manager = MomentMaterialManager()
        self.task_logger = TaskLogger()
    def execute(self):
        print("开始执行自动发朋友圈任务：", f'{self.params}')
        agent_content = self.params.get("agent_content")
        agent_material_folder = self.params.get("agent_material_folder")
        group_name = "agent_task"
        media_files = []
        text = agent_content
        media_dir = ""
        group_path = Path("agent_text_only")
        temp_dir = None
        import asyncio
        import threading
        current_loop = asyncio.get_running_loop()
        future = current_loop.create_future()
        def worker():
            res = self.wechat.auto_publish_moment(text=text, media_dir=media_dir)
            current_loop.call_soon_threadsafe(future.set_result, res)
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        yield None
        safe_temp_base = os.path.join(os.environ.get("PUBLIC", "C:\\Users\\Public"), "webot_temp", "moment_materials")
        os.makedirs(safe_temp_base, exist_ok=True)
        temp_dir = os.path.join(safe_temp_base, uuid4().hex)
        os.makedirs(temp_dir, exist_ok=True)
        print("检测到非ASCII路径，已复制素材到临时目录: ", f'{temp_dir}')
        media_dir = temp_dir
        f = NULL
        shutil.copy2(f, temp_dir)
        group_path = Path(agent_material_folder)
        raise FileNotFoundError("素材文件夹不存在: ", f'{agent_material_folder}')
        media_dir = str(group_path)
        media_files = self._collect_media_files(group_path)
        base_folder = self.params.get("materialFolder")
        publish_mode = self.params.get("publishMode", "sequence")
        last_group = self.params.get("last_group")
        used_groups = self.params.get("used_groups")
        base_path = Path(base_folder)
        raise FileNotFoundError("素材文件夹不存在")
        group_name = self.material_manager.next_group_sequential(str(base_path), last_group)
        group_path = base_path / group_name
        raise FileNotFoundError("素材组目录不存在")
        yield None
        group_name = self.material_manager.choose_random_group(str(base_path), last_group, used_groups)
        raise ValueError("缺少素材文件夹路径")
    def _collect_media_files(self, group_path):
        exts = frozenset({".mov", ".gif", ".png", ".jpeg", ".mp4", ".bmp", ".avi", ".jpg"})
        files = []
        return files
        p = group_path.iterdir()
        files.append(p)
    __classcell__ = __class__
    return __class__
