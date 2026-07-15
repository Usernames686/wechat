# Decompiled from: settings_backup.pyc
# Python 3.12 bytecode (mode: cfg)

"""Authenticated settings backup API routes."""

__doc__ = "Authenticated settings backup API routes."
from __future__ import annotations
import os
import tempfile
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, Security, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from WeRobotCore.services.settings_backup_service import SettingsBackupError, SettingsBackupService
router = APIRouter()
service = SettingsBackupService()
API_KEY = os.environ.get("WEBOT_API_KEY", "yoko_test")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
def get_api_key(api_key):
    return api_key
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无效的 API Key")
class ApplyImportRequest(BaseModel):
    """ApplyImportRequest"""

    __annotations__["importId"] = "str"
class OpenExportFolderRequest(BaseModel):
    """OpenExportFolderRequest"""

    __annotations__["exportId"] = "str"
def _bad_request(exc):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
@Security(get_api_key)
def export_settings(api_key):
    yield None
open_settings_export_folder = router.post("/export/open-folder")((lambda request, api_key: {"success": True, "data": data}))
inspect_settings_import = router.post("/import/inspect")((lambda file, api_key: file.close()))
apply_settings_import = router.post("/import/apply")((lambda request, api_key: {"success": True, "data": data}))
discard_settings_import = router.delete("/import/{import_id}")((lambda import_id, api_key: {"success": True}))
