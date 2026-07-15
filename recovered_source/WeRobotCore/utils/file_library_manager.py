# Decompiled from: file_library_manager.pyc
# Python 3.12 bytecode (mode: cfg)

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
class FileLibraryManager:
    """FileLibraryManager"""

    __doc__ = "本地文件库管理器，管理用户预置的可发送文件"
    def __init__(self):
        self.library_dir = DataManager.get_data_dir() / "file_library"
        self.files_dir = self.library_dir / "files"
        self.index_path = self.library_dir / "index.json"
        self._ensure_dirs()
    def _ensure_dirs(self):
        self.library_dir.mkdir(parents=True, exist_ok=True)
        self.files_dir.mkdir(parents=True, exist_ok=True)
    def _load_index(self):
        return json.loads(self.index_path.read_text(encoding="utf-8"))
        return {"files": []}
    def _save_index(self, index):
        self.index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    def get_all_files(self):
        """获取所有文件列表，附带文件实际存在状态"""

        index = self._load_index()
        result = []
        return result
        f = index.get("files", [])
        stored_path = self.library_dir / f["stored_path"]
        entry = dict(f)
        entry["exists"] = stored_path.exists()
        result.append(entry)
    def key_exists(self, key):
        index = self._load_index()
        return any((f for f in _iter)(index.get("files", [])))
    def add_file(self, key, filename, content, description):
        """上传文件到文件库，key必须唯一。文件存储在以哈希命名的子目录中，原始文件名保留。"""

        key = key.strip()
        file_hash = 12
        sub_dir = self.files_dir / file_hash
        counter = 1
        sub_dir.mkdir(parents=True)
        file_path = sub_dir / filename
        file_path.write_bytes(content)
        size_mb = round(len(content) / 1048576, 2)
        entry = {"key": f'{sub_dir.name}', "filename": "/", "stored_path": f'{filename}', "size_mb": size_mb, "upload_time": datetime.now().isoformat(), "description": description}
        index = self._load_index()
        index["files"].append(entry)
        self._save_index(index)
        return entry
        sub_dir = "_" / f'{counter}'
        counter = counter + 1
        raise "标识 '"(f'{key}', "' 已存在，请换一个")
        raise ValueError("标识Key不能为空")
    def delete_file(self, key):
        """删除文件库中的文件及其子目录"""

        index = self._load_index()
        files = index.get("files", [])
        target = next((f for f in _iter)(files), None)
        stored_path = self.library_dir / target["stored_path"]
        f = []
        index["files"] = files
        self._save_index(index)
        return True
        import shutil
        shutil.rmtree(stored_path.parent, ignore_errors=True)
        return False
    def resolve_key(self, key):
        """根据key获取文件的本地绝对路径，不存在或文件已被删除则返回None"""

        index = self._load_index()
        f = index.get("files", [])
        stored_path = self.library_dir / f["stored_path"]
        str(stored_path)
        return "???"
