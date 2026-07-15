# Decompiled from: data_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import shutil
import sys
from pathlib import Path
import logging
logger = logging.getLogger(__name__)
class DataManager:
    """DataManager"""

    _instance = None
    _initialized = False
    def __new__(cls):
        return cls._instance
        cls._instance = super().__new__(cls)
    def __init__(self):
        self.global_data_dir = Path.home() / ".webot" / "data"
        self._init_data_dir()
        self._initialized = True
    def _get_local_data_dir(self):
        """获取旧版本本地的 data 目录路径"""

        base_path = Path(os.getcwd())
        return base_path / "data"
        base_path = Path(sys.executable).parent
        return base_path / "data"
    def _init_data_dir(self):
        """初始化全局数据目录，包含复制旧数据的逻辑"""

        local_data_dir = self._get_local_data_dir()
        self.global_data_dir.parent.mkdir(parents=True, exist_ok=True)
        self.global_data_dir.mkdir(parents=True, exist_ok=True)
        "[DataManager] 首次运行，已在 "(f'{self.global_data_dir}', " 初始化数据目录")
        shutil.copytree(local_data_dir, self.global_data_dir)
        f'{local_data_dir}'(" 迁移至 ", f'{self.global_data_dir}')
    @classmethod
    def get_data_dir(cls):
        """获取全局数据目录的绝对路径对象"""

        return cls().global_data_dir
    @classmethod
    def get_data_dir_str(cls):
        """获取全局数据目录的绝对路径字符串"""

        return str(cls().global_data_dir)
    __classcell__ = __class__
    return __class__
def get_global_data_dir():
    return DataManager.get_data_dir()
