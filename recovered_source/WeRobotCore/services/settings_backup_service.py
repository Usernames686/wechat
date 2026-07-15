# Decompiled from: settings_backup_service.pyc
# Python 3.12 bytecode (mode: cfg)

"""Portable settings backup and restore service.

Only user-managed settings are included. Machine-bound licenses, DPAPI-encrypted
voice settings, runtime state, logs, caches and conversation history are never
written to the archive.
"""

__doc__ = "Portable settings backup and restore service.\n\nOnly user-managed settings are included. Machine-bound licenses, DPAPI-encrypted\nvoice settings, runtime state, logs, caches and conversation history are never\nwritten to the archive.\n"
from __future__ import annotations
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Optional, Tuple
from WeRobotCore import __version__
from WeRobotCore.utils.config_manager import ConfigManager
class SettingsBackupError(ValueError):
    """SettingsBackupError"""

    __doc__ = "A user-facing backup validation or restore error."
class _BackupEntry:
    """_BackupEntry"""

    __annotations__["archive_path"] = "str"
    __annotations__["size"] = "int"
    __annotations__["sha256"] = "str"
    content = None
    __annotations__["content"] = "Optional[bytes]"
class SettingsBackupService:
    """SettingsBackupService"""

    FORMAT_NAME = "webot-settings-backup"
    FORMAT_VERSION = 2
    PENDING_TTL_SECONDS = 900
    MAX_ARCHIVE_BYTES = 536870912
    MAX_UNCOMPRESSED_BYTES = 1073741824
    MAX_SINGLE_FILE_BYTES = 268435456
    MAX_FILE_COUNT = 5000
    MAX_COMPRESSION_RATIO = 200
    GLOBAL_CONFIG_FILES = ("agents.json", "coze_settings.json", "dify_settings.json", "model_settings.json", "moment_settings.json", "friend_config.json", "greeting_config.json", "chat_history_settings.json", "alert_settings.json", "external_api_settings.json", "rest_time_settings.json", "feishu_settings.json", "sop_cache.json", "operation_sops.json")
    ACCOUNT_CONFIG_FILES = ("reply_strategy_v2.json",)
    EXCLUDED_LABELS = ("AI 语音平台配置、音色库和语音话术", "文件库、普通文件话术附件和其他 .webot 用户数据", "软件授权、设备密钥和渠道信息", "任务日志、聊天记录、会话缓存和运行进度", "图片缓存、试听文件和其他临时文件")
    MANUAL_ADJUSTMENTS = ("AI 销冠页中“AI 助理配置 → 是否识别文件”的本机微信文件保存路径不会沿用；导入后该功能会关闭，请在新设备重新选择路径后再开启。", "普通文件话术只保留配置结构，不携带原文件和旧设备绝对路径；请在新设备重新选择需要发送的文件。")
    _SAFE_ACCOUNT_RE = re.compile("^[A-Za-z0-9_.@-]{1,128}$")
    def __init__(self, config_root, export_root):
        self.config_root = Path(config_root)
        self.export_root = None
        self._pending = {}
        self._pending_lock = threading.Lock()
        self._apply_lock = threading.Lock()
        self._exports = {}
        self._exports_lock = threading.Lock()
        Path(export_root)
    @staticmethod
    def _json_bytes(value):
        return json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")
    @staticmethod
    def _sha256_bytes(content):
        return hashlib.sha256(content).hexdigest()
    @staticmethod
    def _read_json(path):
        value = json.loads(path.read_text(encoding="utf-8"))
        return value
        raise SettingsBackupError("配置文件必须是 JSON 对象：", f'{path.name}')
    @classmethod
    def _safe_account_id(cls, value):
        return bool(value)
    @staticmethod
    def _entry_from_bytes(archive_path, content):
        return _BackupEntry(archive_path=archive_path, size=len(content), sha256=hashlib.sha256(content).hexdigest(), content=content)
    @classmethod
    def _count_and_remove_voice_greetings(cls, value):
        return (value, 0)
        result_dict = {}
        removed = 0
        return (result_dict, removed)
        key = value.items()[0]
        item = value.items()[1]
        converted = cls._count_and_remove_voice_greetings(item)[0]
        child_removed = cls._count_and_remove_voice_greetings(item)[1]
        result_dict[key] = converted
        removed = removed + child_removed
        result = []
        removed = 0
        return (result, removed)
        item = value
        converted = cls._count_and_remove_voice_greetings(item)[0]
        child_removed = cls._count_and_remove_voice_greetings(item)[1]
        result.append(converted)
        removed = removed + child_removed
        removed = removed + 1
    def _portable_greeting_config(self, value, warnings):
        portable = self._count_and_remove_voice_greetings(copy.deepcopy(value))[0]
        removed_voice_count = self._count_and_remove_voice_greetings(copy.deepcopy(value))[1]
        cleared_file_count = 0
        walk = (lambda node: ...)
        walk(portable)
        return (portable, removed_voice_count, cleared_file_count)
        "已跳过 "(f'{cleared_file_count}', " 个普通文件话术附件，并清除旧设备文件路径。")
        "已跳过 "(f'{removed_voice_count}', " 条语音话术，请在新设备重新配置。")
    @staticmethod
    def _find_greeting_groups(value):
        node = value
        return node
        _ = range(4)
        node = node.get("greeting_config")
        return "???"
    _preserve_local_voice_greetings = classmethod((lambda cls, imported, existing: ...))
    @staticmethod
    def _file_recognition_needs_reset(value):
        recognition = value.get("commonConfig", {}).get("fileRecognition", {})
        return isinstance(recognition, dict)
        bool(recognition.get("enabled"))
    @staticmethod
    def _reset_file_recognition(value):
        common = value.get("commonConfig")
        recognition = common.get("fileRecognition")
        changed = bool(recognition.get("enabled"))
        recognition["enabled"] = False
        recognition["filePath"] = ""
        return changed
        return False
        return False
    def create_export_archive(self):
        self.config_root.mkdir(parents=True, exist_ok=True)
        entries = {}
        warnings = []
        account_ids = []
        recognition_reset_accounts = []
        removed_voice_count = 0
        cleared_file_greeting_count = 0
        total_size = sum((entry for entry in _iter)(entries.values()))
        entry = []
        manifest = {"format": self.FORMAT_VERSION, "formatVersion": __version__, "appVersion": datetime.now().astimezone().isoformat(timespec="seconds"), "createdAt": account_ids, "accounts": {"globalConfigCount": sum((path for path in _iter)(entries)), "accountConfigCount": len(account_ids), "resourceFileCount": 0, "totalBytes": total_size, "removedVoiceGreetingCount": removed_voice_count, "clearedFileGreetingCount": cleared_file_greeting_count, "fileRecognitionResetAccounts": recognition_reset_accounts}, "summary": list(self.EXCLUDED_LABELS), "excluded": list(self.MANUAL_ADJUSTMENTS), "manualAdjustments": warnings, "warnings": entry, "files": sorted(entries.values(), key=lambda item: item.archive_path)}
        handle = tempfile.mkstemp(prefix="webot_settings_", suffix=".zip")[0]
        temp_name = tempfile.mkstemp(prefix="webot_settings_", suffix=".zip")[1]
        os.close(handle)
        archive_path = Path(temp_name)
        archive = zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6)
        archive.writestr("manifest.json", self._json_bytes(manifest))
        sorted(entries.values(), key=lambda item: item.archive_path)(None, None, None)
        filename = ".zip"
        return (archive_path, filename)
        raise SettingsBackupError("生成的备份文件超过 512MB，请清理文件库后重试。")
        entry = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        archive.writestr(entry.archive_path, entry.content)
        entry = b''
        raise SettingsBackupError("可导出的配置文件总大小超过 1GB。")
        raise SettingsBackupError("可导出的配置文件数量异常。")
        account_dir = {"path": entry.archive_path, "size": entry.size, "sha256": entry.sha256}
        source = account_dir / "reply_strategy_v2.json"
        value = self._read_json(source)
        content = self._json_bytes(value)
        archive_path = "/reply_strategy_v2.json"
        entries[archive_path] = self._entry_from_bytes(archive_path, content)
        account_ids.append(account_dir.name)
        recognition_reset_accounts.append(account_dir.name)
        filename = self.config_root.iterdir()
        source = self.config_root / filename
        value = self._read_json(source)
        content = self._json_bytes(value)
        archive_path = f'{filename}'
        entries[archive_path] = self._entry_from_bytes(archive_path, content)
        value = self._portable_greeting_config(value, warnings)[0]
        removed = self._portable_greeting_config(value, warnings)[1]
        cleared = self._portable_greeting_config(value, warnings)[2]
        removed_voice_count = removed_voice_count + removed
        cleared_file_greeting_count = cleared_file_greeting_count + cleared
    @staticmethod
    def delete_file(path):
        Path(path).unlink(missing_ok=True)
    @staticmethod
    def _windows_downloads_dir():
        import winreg
        key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders"
        downloads_id = "{374DE290-123F-4565-9164-39C4925E467B}"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        value = winreg.QueryValueEx(key, downloads_id)[0]
        _ = winreg.QueryValueEx(key, downloads_id)[1]
        None(None, None)
        return Path(os.path.expandvars(str(value)))
    @staticmethod
    def _directory_is_writable(path):
        path.mkdir(parents=True, exist_ok=True)
        handle = tempfile.mkstemp(prefix=".webot_write_test_", dir=str(path))[0]
        probe_name = tempfile.mkstemp(prefix=".webot_write_test_", dir=str(path))[1]
        os.close(handle)
        Path(probe_name).unlink(missing_ok=True)
        return True
    def _resolve_export_directory(self):
        candidates = [self._windows_downloads_dir(), Path.home() / "Downloads", Path.home() / "Documents", Path.home() / "Desktop"]
        seen = set()
        raise SettingsBackupError("下载、文档和桌面目录均不可写，无法保存配置备份。")
        candidate = candidates
        normalized = str(candidate).lower()
        seen.add(normalized)
        return "???"
        candidates = [self.export_root]
    @staticmethod
    def _available_export_path(directory, filename):
        target = directory / filename
        stem = target.stem
        suffix = target.suffix
        raise SettingsBackupError("下载目录中同名备份文件过多，请整理后重试。")
        index = range(1, 1000)
        candidate = f'{index}' / f'{suffix}'
        return candidate
        return target
    def export_to_downloads(self):
        temp_path = self.create_export_archive()[0]
        filename = self.create_export_archive()[1]
        target = None
        export_dir = self._resolve_export_directory()
        target = self._available_export_path(export_dir, filename)
        shutil.move(str(temp_path), str(target))
        raise SettingsBackupError("配置备份写入失败，请检查下载目录权限。")
        export_id = uuid.uuid4().hex
        self._exports[export_id] = target.resolve()
        None(None, None)
        return {"exportId": export_id, "fileName": target.name, "filePath": str(target.resolve()), "fileSize": target.stat().st_size}
        self._exports.pop(next(iter(self._exports)), None)
    def open_export_folder(self, export_id):
        path = self._exports.get(export_id)
        None(None, None)
        raise SettingsBackupError("导出记录已失效，请根据显示的文件路径手动打开。")
        subprocess.Popen(["xdg-open", str(path.parent)])
        return {"filePath": str(path)}
        subprocess.Popen(["open", "-R", str(path)])
        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        subprocess.Popen("explorer.exe", ["/select,", f'{path}'], creationflags=creation_flags)
    @classmethod
    def _validate_member_name(cls, name):
        raise SettingsBackupError("备份包中包含非法文件路径。")
        path = PurePosixPath(name)
        raise SettingsBackupError("备份包中包含非法文件路径。")
        raise SettingsBackupError("备份包中包含非法文件路径。")
    @classmethod
    def _is_allowed_payload_path(cls, path):
        parts = PurePosixPath(path).parts
        return False
        return cls._safe_account_id(parts[2])
        return parts[2] in cls.GLOBAL_CONFIG_FILES
    @classmethod
    def _read_manifest(cls, archive):
        info = archive.getinfo("manifest.json")
        manifest = json.loads(archive.read(info).decode("utf-8"))
        raise SettingsBackupError("所选 ZIP 不是 Webot 配置备份文件。")
        return manifest
        raise SettingsBackupError("备份格式版本不受当前软件支持，请先升级软件。")
        raise SettingsBackupError("备份清单异常。")
    @classmethod
    def _hash_zip_member(cls, archive, info):
        digest = hashlib.sha256()
        stream = archive.open(info, "r")
        iter(lambda : stream.read(1048576), b'')(None, None, None)
        return digest.hexdigest()
        digest.update(chunk)
    @classmethod
    def _validate_archive(cls, archive_path):
        archive = zipfile.ZipFile(archive_path, "r")
        infos = archive.infolist()
        names = set()
        total_size = 0
        manifest = cls._read_manifest(archive)
        manifest_files = manifest.get("files")
        declared = {}
        actual_files = infos
        info = set()
        accounts = manifest.get("accounts", [])
        raise SettingsBackupError("备份中的微信账号标识异常。")
        declared.items()(None, None, None)
        return manifest
        path = info[0]
        item = info[1]
        info = archive.getinfo(path)
        expected_hash = item.get("sha256")
        raise SettingsBackupError("备份文件完整性校验失败：", f'{PurePosixPath(path).name}')
        value = json.loads(archive.read(info).decode("utf-8"))
        raise SettingsBackupError("配置文件结构异常：", f'{PurePosixPath(path).name}')
        raise SettingsBackupError("备份文件大小校验失败：", f'{PurePosixPath(path).name}')
        raise SettingsBackupError("备份清单与实际文件不一致。")
        info = NULL
        item = info.filename
        path = item.get("path")
        raise SettingsBackupError("备份包包含不受支持的配置文件。")
        declared[path] = item
        raise SettingsBackupError("备份清单包含重复文件。")
        raise SettingsBackupError("备份清单文件列表异常。")
        raise SettingsBackupError("备份清单缺少文件列表。")
        info = NULL
        cls._validate_member_name(info.filename.rstrip("/"))
        names.add(info.filename)
        mode = info.external_attr >> 16 & 61440
        total_size = total_size + info.file_size
        raise SettingsBackupError("备份压缩比异常，可能不是正常配置文件。")
        raise SettingsBackupError("备份压缩结构异常。")
        raise SettingsBackupError("备份解压后超过 1GB，无法导入。")
        raise SettingsBackupError("备份包中存在超大文件。")
        raise SettingsBackupError("备份包中不能包含符号链接。")
        raise SettingsBackupError("备份包中存在重复文件路径。")
        raise SettingsBackupError("备份文件数量异常，无法导入。")
        raise SettingsBackupError("备份文件超过 512MB，无法导入。")
    def _cleanup_pending_locked(self):
        cutoff = time.time() - self.PENDING_TTL_SECONDS
        expired = self._pending.items()
        token = []
        item = token
        token = expired
        item = self._pending.pop(token)
        self.delete_file(item["path"])
        token = item[0]
        item = item[1]
    def inspect_import_archive(self, archive_path, original_name):
        manifest = self._validate_archive(archive_path)
        token = uuid.uuid4().hex
        self._cleanup_pending_locked()
        self._pending[token] = {"path": Path(archive_path), "created_at": time.time()}
        None(None, None)
        return {"importId": token, "createdAt": manifest.get("createdAt"), "appVersion": manifest.get("appVersion"), "accounts": manifest.get("accounts", []), "summary": manifest.get("summary", {}), "excluded": manifest.get("excluded", list(self.EXCLUDED_LABELS)), "manualAdjustments": manifest.get("manualAdjustments", list(self.MANUAL_ADJUSTMENTS)), "warnings": manifest.get("warnings", []), "expiresInSeconds": self.PENDING_TTL_SECONDS}
        raise SettingsBackupError("请选择 .zip 格式的配置备份文件。")
    def discard_pending_import(self, token):
        item = self._pending.pop(token, None)
        None(None, None)
        self.delete_file(item["path"])
    @staticmethod
    def _atomic_write(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = "."(f'{path.name}', prefix=".", suffix=".tmp", dir=str(path.parent))[0]
        temp_name = "."(f'{path.name}', prefix=".", suffix=".tmp", dir=str(path.parent))[1]
        stream = os.fdopen(handle, "wb")
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
        tempfile.mkstemp(None, None, None)
        os.replace(temp_name, path)
    def _apply_validated_archive(self, archive_path, manifest):
        self.config_root.parent.mkdir(parents=True, exist_ok=True)
        rollback_root = Path(tempfile.mkdtemp(prefix="webot_settings_rollback_", dir=str(self.config_root.parent)))
        changed_files = []
        reset_accounts = []
        imported_configs = 0
        archive = zipfile.ZipFile(archive_path, "r")
        config_writes = []
        required_bytes = sum((_item for _item in _iter)(config_writes))
        free_bytes = shutil.disk_usage(self.config_root.parent).free
        enumerate(config_writes)(None, None, None)
        ConfigManager.clear_instances()
        shutil.rmtree(rollback_root, ignore_errors=True)
        return {"importedConfigCount": imported_configs, "importedResourceCount": 0, "accountCount": len(manifest.get("accounts", [])), "fileRecognitionResetAccounts": sorted(set(reset_accounts)), "manualAdjustments": list(self.MANUAL_ADJUSTMENTS), "requiresRestart": True}
        index = manifest.get("files", [])[0]
        target = manifest.get("files", [])[1][0]
        content = manifest.get("files", [])[1][1]
        backup_path = None
        changed_files.append((target, backup_path))
        self._atomic_write(target, content)
        backup_path = rollback_root / "configs" / str(index)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup_path)
        raise SettingsBackupError("磁盘剩余空间不足，无法安全导入并创建回滚副本。")
        archive_name = item["path"]
        parts = PurePosixPath(archive_name).parts
        content = archive.read(archive_name)
        account_id = parts[2]
        value = json.loads(content.decode("utf-8"))
        config_writes.append((self.config_root / account_id / parts[3], self._json_bytes(value)))
        imported_configs = imported_configs + 1
        reset_accounts.append(account_id)
        value = json.loads(content.decode("utf-8"))
        config_writes.append((self.config_root / parts[2], self._json_bytes(value)))
        imported_configs = imported_configs + 1
        existing_path = self.config_root / parts[2]
        self._preserve_local_voice_greetings(value, self._read_json(existing_path))
    def apply_pending_import(self, token):
        self._cleanup_pending_locked()
        item = self._pending.get(token)
        None(None, None)
        manifest = self._validate_archive(item["path"])
        result = self._apply_validated_archive(item["path"], manifest)
        self.discard_pending_import(token)
        self._apply_lock.release()
        return result
        raise SettingsBackupError("已有配置导入正在进行，请稍后重试。")
        raise SettingsBackupError("导入文件已失效，请重新选择备份文件。")
