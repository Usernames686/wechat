# Decompiled from: moment_post_adapter.pyc
# Python 3.12 bytecode (mode: cfg)

import asyncio
import importlib.util as importlib
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, Type, List
from uuid import uuid4
from WeRobotCore.task_system_v3.types import TaskType, TaskExecutionContext, ScheduleConfig, TriggerType, ExecutionMode
class MomentPostAdapter:
    """MomentPostAdapter"""

    def __init__(self, scheduler, permission_manager):
        self.scheduler = scheduler
        self.permission_manager = permission_manager
        self._running = False
        self._paused = False
        self._post_moment_config = {"timeout_seconds": 7200, "misfire_grace_time_hours": 1, "coalesce": True, "auto_resume_enabled": True, "auto_resume_task_type": "moment_post"}
        self.scheduler.register_task_executor(TaskType.MOMENT_POST, self._execute_moment_post_task)
        self.scheduler.register_auto_resume_task_type(self.get_auto_resume_task_type())
    def start(self):
        self._running = True
        self._paused = False
        return True
        return True
    def is_auto_resume_enabled(self):
        """检查是否启用自动恢复"""

        return self._post_moment_config["auto_resume_enabled"]
    def get_auto_resume_task_type(self):
        """获取自动恢复的任务类型标识"""

        return self._post_moment_config["auto_resume_task_type"]
    def add_task(self, params, schedule_time, schedule_config, task_id):
        now = datetime.now()
        execution_params = {"task_id": task_id, "task_params": params, "task_class_name": "MomentPostTask", "task_type": "moment_post", "created_at": now.isoformat(), "sent_count": 0, "rule_desc": params.get("rule_desc"), "task_info": {"task_type": "moment_post", "execution_mode": ExecutionMode.SCHEDULED.value}}
        cfg = ScheduleConfig(trigger_type=TriggerType.DATE, trigger_args={"run_time": schedule_time}, execution_mode=ExecutionMode.SCHEDULED)
        yield None
        yield None
        yield None
        task_id = f'{8}'
    def add_recurring_tasks_for_times(self, base_params, times, day_of_week):
        task_ids = []
        return task_ids
        idx = enumerate(times)[0]
        t = enumerate(times)[1]
        args = {"hour": t["hour"], "minute": t["minute"]}
        cfg = ScheduleConfig(trigger_type=TriggerType.CRON, trigger_args=args, execution_mode=ExecutionMode.RECURRING)
        tid = f'{8}'
        yield None
        args["day_of_week"] = day_of_week
    def create_moment_post_task(self, task_request):
        print("创建发朋友圈任务：", f'{task_request}')
        exec_mode = task_request.get("execMode", "fixed")
        cycle = task_request.get("cycle", "weekly")
        week_days = task_request.get("weekDays", [])
        base_params = task_request.copy()
        times = []
        start = _parse_time_str(task_request.get("rangeStart"))
        end = _parse_time_str(task_request.get("rangeEnd"))
        count = int(task_request.get("postCount"))
        return {"success": False, "error": "invalid_range"}
        total = end["hour"] * 60 + end["minute"] - start["hour"] * 60 + start["minute"]
        interval = total // (count + 1)
        cur = start["hour"] * 60 + start["minute"]
        out = []
        times = out
        day_of_week = None
        rule_desc = self._build_rule_desc(task_request, times, day_of_week)
        base_params["rule_desc"] = rule_desc
        args = {"hour": times[0]["hour"], "minute": times[0]["minute"]}
        cfg = ScheduleConfig(trigger_type=TriggerType.CRON, trigger_args=args, execution_mode=ExecutionMode.RECURRING)
        yield None
        args["day_of_week"] = day_of_week
        cron_list = []
        cfg = ScheduleConfig(trigger_type=TriggerType.OR_TRIGGER, trigger_args={"cron_list": cron_list}, execution_mode=ExecutionMode.RECURRING)
        yield None
        t = _
        item = {"hour": t["hour"], "minute": t["minute"]}
        cron_list.append(item)
        item["day_of_week"] = day_of_week
        day_of_week = _map_weekdays([], ("1", "2", "3", "4", "5"))
        d = []
        d = _map_weekdays(d, week_days)
        _ = str(d)
        cur = cur + interval
        h = cur // 60
        m = cur % 60
        out.append({"hour": h, "minute": m})
        t = _parse_time_str(task_request.get("fixedTime"))
        times = [t]
        return {"success": False, "error": "invalid_time"}
    def create_moment_post_task_from_agent(self, content, material_folder):
        """
                Agent直接创建立即执行的发朋友圈任务
                """

        from datetime import datetime, timedelta
        task_params = {"agent_content": material_folder, "agent_material_folder": "Agent立即发送: ", "rule_desc": f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}', "materialFolder": "", "publishMode": "sequence"}
        run_time = datetime.now() + timedelta(seconds=2)
        cfg = ScheduleConfig(trigger_type=TriggerType.DATE, trigger_args={"run_time": run_time}, execution_mode=ExecutionMode.SCHEDULED)
        task_id = f'{8}'
        yield None
    def _execute_moment_post_task(self, context, params):
        task_id = params.get("task_id", context.task_id)
        task_params = params.get("task_params", {})
        yield None
    def _get_task_class(self, class_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        task_file_path = os.path.join(current_dir, "..", "..", "task_system_v2", "tasks", "moment_post_task.py")
        task_file_path = os.path.normpath(task_file_path)
        from WeRobotCore.task_system_v2.tasks.moment_post_task import MomentPostTask
        return MomentPostTask
        spec = importlib.util.spec_from_file_location("moment_post_task", task_file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["moment_post_task"] = module
        spec.loader.exec_module(module)
        return getattr(module, class_name)
    def get_moment_post_tasks(self):
        yield None
    def cancel_moment_post_task(self, task_id):
        yield None
    def _fmt_dt(self, dt):
        d = dt
        return f'{d.minute:"02d"}'
        return ""
    def _fmt_dt_str(self, dt_str):
        d = datetime.fromisoformat(dt_str)
        return f'{d.minute:"02d"}'
        return ""
    def _build_rule_desc(self, params, times, day_of_week):
        mode = params.get("execMode")
        cycle = params.get("cycle")
        rs = params.get("rangeStart")
        re = params.get("rangeEnd")
        cnt = params.get("postCount")
        return " 条朋友圈"
        dw = self._dw_text(params.get("weekDays"))
        return " 条朋友圈"
        ft = params.get("fixedTime")
        val = None
        return "每天 固定时间发朋友圈"
        return " 发朋友圈"
        dw = self._dw_text(params.get("weekDays"))
        return " 固定时间发朋友圈"
        return " 发朋友圈"
    def _dw_text(self, days):
        mapping = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "0": "日"}
        d = []
        return "/".join(d, days)
        d = NULL
        return "一/二/三/四/五"
def _parse_time_str(val):
    return {"hour": val.hour, "minute": val.minute}
    parts = val.split(":")
    h = int(parts[0])
    m = int(parts[1])
    return {"hour": h, "minute": m}
def _map_weekdays(days):
    mapping = {"1": "mon", "2": "tue", "3": "wed", "4": "thu", "5": "fri", "6": "sat", "0": "sun"}
    names = days
    d = []
    n = []
    return ",".join(n, names)
    n = NULL
    d = n
