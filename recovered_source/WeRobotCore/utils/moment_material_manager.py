# Decompiled from: moment_material_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import asyncio
from pathlib import Path
from typing import List
class MomentMaterialManager:
    """MomentMaterialManager"""

    _instance = None
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance._initialized = False
    def __init__(self):
        self._initialized = True
        self._lock = asyncio.Lock()
        from WeRobotCore.utils.data_manager import DataManager
        self._base_dir = DataManager.get_data_dir() / "moment_material"
        self._base_dir.mkdir(parents=True, exist_ok=True)
    def list_groups(self, plan_name):
        plan_path = self._base_dir / plan_name
        return []
        p = []
        return plan_path.iterdir()
    def read_group_text(self, group_path):
        gp = Path(group_path)
        raise FileNotFoundError("素材组目录不存在")
        candidates = sorted(gp.glob("*.txt"))
        txt = candidates[0]
        yield None
        raise FileNotFoundError("素材组中未找到文本素材")
    def list_group_names(self, base_folder):
        bp = Path(base_folder)
        return []
        p = []
        return sorted(p, bp.iterdir())
        p = NULL
    def next_group_sequential(self, base_folder, last_group):
        groups = self.list_group_names(base_folder)
        return groups[0]
        idx = groups.index(last_group)
        return groups[(idx + 1) % len(groups)]
        raise ValueError("素材组为空")
    def choose_random_group(self, base_folder, last_group, used_groups):
        import random
        groups = self.list_group_names(base_folder)
        used = set(used_groups)
        candidates = groups
        g = []
        return random.choice(candidates)
        g = []
        candidates = groups
        raise ValueError("素材组为空")
    __classcell__ = __class__
    return __class__
