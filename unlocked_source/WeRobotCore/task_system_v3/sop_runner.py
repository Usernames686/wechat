# Decompiled from: sop_runner.pyc
# Python 3.12 bytecode (mode: cfg)

"""
SOP 编排执行器 - Task System V3

把"运营SOP"（一个有序动作序列）对某个目标按序执行：

设计要点：
- 复用统一调度器 + PermissionManager(EXCLUSIVE)：SOP 作为 TaskType.SOP_FLOW 接入同一个调度器，
  与自动回复 / 群发 / 跟单等共用同一把"RPA 独占锁"，保证同一时刻只有一个 RPA 在操作微信窗口，
  绝不另起调度器，避免两套调度器抢同一个 UI。本模块只负责"拿到锁之后按顺序跑动作"。
- 线性顺序执行；每个动作类型声明"适用的目标类型"作为前置条件，不满足则【跳过并记日志】，
  不中断整个 SOP（例如"拉群"只适用单聊好友，遇到群目标自动跳过）。
- 每次运行落一条运行记录到本地（前端展示二期再做）。

MVP 动作类型：
- pull_into_group  拉群（把单聊好友拉入指定群）—— 仅单聊好友，RPA
- greeting         发打招呼（发送话术组）       —— 单聊/群，RPA
- create_follow    创建跟单任务                 —— 单聊/群，非RPA（仅登记未来定时任务，不占用本次持锁的窗口操作）
"""

__doc__ = "\nSOP 编排执行器 - Task System V3\n\n把\"运营SOP\"（一个有序动作序列）对某个目标按序执行：\n\n设计要点：\n- 复用统一调度器 + PermissionManager(EXCLUSIVE)：SOP 作为 TaskType.SOP_FLOW 接入同一个调度器，\n  与自动回复 / 群发 / 跟单等共用同一把\"RPA 独占锁\"，保证同一时刻只有一个 RPA 在操作微信窗口，\n  绝不另起调度器，避免两套调度器抢同一个 UI。本模块只负责\"拿到锁之后按顺序跑动作\"。\n- 线性顺序执行；每个动作类型声明\"适用的目标类型\"作为前置条件，不满足则【跳过并记日志】，\n  不中断整个 SOP（例如\"拉群\"只适用单聊好友，遇到群目标自动跳过）。\n- 每次运行落一条运行记录到本地（前端展示二期再做）。\n\nMVP 动作类型：\n- pull_into_group  拉群（把单聊好友拉入指定群）—— 仅单聊好友，RPA\n- greeting         发打招呼（发送话术组）       —— 单聊/群，RPA\n- create_follow    创建跟单任务                 —— 单聊/群，非RPA（仅登记未来定时任务，不占用本次持锁的窗口操作）\n"
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from WeRobotCore.utils.data_manager import DataManager
logger = get_logger("sop_runner")
ACTION_TARGET_TYPES = {"pull_into_group": {"single"}, "greeting": {"single", "group"}, "create_follow": {"single", "group"}}
__annotations__["ACTION_TARGET_TYPES"] = Dict[(str, Optional[set])]
ACTION_IS_RPA = {"pull_into_group": True, "greeting": True, "create_follow": False}
__annotations__["ACTION_IS_RPA"] = Dict[(str, bool)]
class SopRunner:
    """SopRunner"""

    __doc__ = "SOP 序列执行器。一次 run() = 对一个目标按序跑完一个 SOP。"
    def __init__(self, config_manager, wechat_instance, account_id):
        self.config_manager = config_manager
        self.wechat = wechat_instance
        self.account_id = account_id
        self._log_dir = os.path.join(DataManager.get_data_dir_str(), "sop_runs", account_id)
    def run(self, sop, target, source):
        """执行一个 SOP。

                sop:    {id, name, actions:[{type, params}]}
                target: {name, chat_type, wxid?}  # name=会话名/好友名/群名
                source: 触发来源（如 group_join）
                """

        target_type = target.get("chat_type", "single")
        actions = sop.get("actions", [])
        run_record = {"run_id": f'{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}', "sop_id": sop.get("id"), "sop_name": sop.get("name", ""), "account_id": self.account_id, "target": target, "source": source, "started_at": datetime.now().isoformat(), "finished_at": None, "status": "running", "steps": []}
        ") 共"(f'{len(actions)}', "步")
        run_record["status"] = "completed"
        run_record["finished_at"] = datetime.now().isoformat()
        self._persist(run_record)
        return run_record
        idx = enumerate(actions, start=1)[0]
        action = enumerate(actions, start=1)[1]
        atype = action.get("type")
        params = action.get("params", {})
        step = {"index": idx, "type": atype, "status": "", "reason": "", "ts": datetime.now().isoformat()}
        applicable = ACTION_TARGET_TYPES.get(atype)
        yield None
        step["status"] = "skipped"
        step["reason"] = f'{atype}'
        f'{atype}'(" 跳过：", f'{step["reason"]}')
        run_record["steps"].append(step)
    def _dispatch(self, atype, params, target, source):
        """把动作派发到对应处理器。返回 (是否成功, 说明)。"""

        return ("未知动作类型: ", f'{atype}')
        yield None
        yield None
        yield None
    def _action_greeting(self, params, target):
        greeting_group_id = params.get("greetingGroupId")
        from WeRobotCore.utils.greeting_manager import GreetingManager
        gm = GreetingManager(self.config_manager)
        yield None
        return (False, "无可用微信实例")
        return (False, "未配置话术组")
    def _action_pull_into_group(self, params, target):
        group_name = params.get("targetGroupName")
        res = self.wechat.invite_friends_to_group([target.get("name")], group_name)
        ok = bool(res)
        return (ok, res.get("message", ""))
        return (False, "无可用微信实例")
        return (False, "未配置目标群")
        res.get("success")
    def _action_create_follow(self, params, target):
        from WeRobotCore.task_system_v3.unified_manager_pattern import get_auto_follow_manager
        mgr = get_auto_follow_manager()
        time_start = params.get("timeStart", "09:00")
        time_end = params.get("timeEnd", "12:00")
        task_request = {"account_id": self.account_id, "friend_wxid": target.get("wxid"), "friend_name": target.get("name"), "chat_type": target.get("chat_type", "single"), "agent_id": params.get("agentId"), "follow_scenario": params.get("followScenario", "新好友"), "follow_days": params.get("followDays", 2), "follow_frequency": params.get("frequency", 0), "time_range_start": time_start, "time_range_end": time_end, "first_run_next_day": params.get("firstRun") == "next_day"}
        yield None
        now = datetime.now()
        end = now + timedelta(hours=1)
        time_start = now.strftime("%H:%M")
        time_end = end.strftime("%H:%M")
        return (False, "跟单管理器不可用")
    def _persist(self, run_record):
        os.makedirs(self._log_dir, exist_ok=True)
        fpath = os.path.join(self._log_dir, f'{run_record["run_id"]}', ".json")
        f = open(fpath, "w", encoding="utf-8")
        json.dump(run_record, f, ensure_ascii=False, indent=2)
        None(None, None)
