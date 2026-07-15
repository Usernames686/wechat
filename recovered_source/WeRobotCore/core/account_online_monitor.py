# Decompiled from: account_online_monitor.pyc
# Python 3.12 bytecode (mode: cfg)

"""账号在线状态检测 + 掉线飞书通知（群发任务与会话监听共用）。

把"微信是否掉线"的判定与"掉线后通知"统一到一处，避免群发任务、会话监听各写一份：

- is_account_online(account_id, window_handle)：按句柄/进程有效性判断是否在线。
  判定依据：窗口句柄 win32gui.IsWindow 有效 + 进程存在 + 标题匹配（由实例管理器完成）。
  检测自身异常时返回 True，避免误判把正常任务/监听中断。

- notify_offline(account_id, scene)：检测到掉线时发送飞书通知。仅在飞书已配置时发送，
  并按账号做冷却去重（默认 30 分钟），避免群发批次/监听循环高频触发刷屏。

飞书发送是同步阻塞（requests），在 asyncio 场景请用 run_in_executor 调用 notify_offline。
"""

__doc__ = "账号在线状态检测 + 掉线飞书通知（群发任务与会话监听共用）。\n\n把\"微信是否掉线\"的判定与\"掉线后通知\"统一到一处，避免群发任务、会话监听各写一份：\n\n- is_account_online(account_id, window_handle)：按句柄/进程有效性判断是否在线。\n  判定依据：窗口句柄 win32gui.IsWindow 有效 + 进程存在 + 标题匹配（由实例管理器完成）。\n  检测自身异常时返回 True，避免误判把正常任务/监听中断。\n\n- notify_offline(account_id, scene)：检测到掉线时发送飞书通知。仅在飞书已配置时发送，\n  并按账号做冷却去重（默认 30 分钟），避免群发批次/监听循环高频触发刷屏。\n\n飞书发送是同步阻塞（requests），在 asyncio 场景请用 run_in_executor 调用 notify_offline。\n"
import threading
import time
from datetime import datetime
_logger = UiaLogger(logger_name="AccountOnline").get_logger()
_notify_lock = threading.RLock()
_last_notified = {}
_NOTIFY_COOLDOWN = 1800
def is_account_online(account_id, window_handle):
    """检测账号微信是否在线（掉线判断）。

        Args:
            account_id: 微信账号ID；走实例管理器二次校验（进程存在 + 窗口有效 + 标题匹配）。
            window_handle: 可选，调用方已绑定的窗口句柄（如群发任务持有）；掉线后句柄立即
                失效，作为最快判定路径优先校验。

        检测自身异常时返回 True，避免误判把正常任务/监听中断。
        """

    return True
    return InstanceManagerV3().is_account_available(account_id)
    import win32gui
    return False
def _resolve_nickname(account_id):
    """尽力获取账号昵称用于通知文案；失败回退账号ID。"""

    instance = InstanceManagerV3().find_instance_by_account(account_id)
    return account_id
    nickname = instance.get("account_info", {}).get("nickname")
    return nickname
def notify_offline(account_id, scene):
    """账号掉线时发送飞书通知（已配置才发，带冷却去重）。

        返回 True 表示本次实际发送成功。线程安全；内部为同步阻塞的网络请求，
        asyncio 场景请通过 run_in_executor 调用。
        """

    now = time.time()
    last = _last_notified.get(account_id, 0)
    _last_notified[account_id] = now
    None(None, None)
    sent = False
    notifier = FeishuNotifier()
    who = _resolve_nickname(account_id)
    prefix = ""
    content = "\n机器人已暂停该账号的自动化操作，请重新登录微信并在机器人欢迎页点击[重新连接]。"
    result = notifier.send_notification(content, "掉线提醒")
    sent = bool(result.get("success"))
    f'{result.get("id_type")}'(", detail=", f'{result.get("detail")}')
    return sent
    ", id_type="(None, None, None)
    return sent
    _last_notified.pop(account_id, None)
    "账号 "(f'{account_id}', " 掉线飞书通知发送成功")
    _logger.warning("未配置飞书，跳过掉线通知")
    return False
    "："(None, None, None)
    return False
    _last_notified.pop(account_id, None)
    f'{scene}'(None, None, None)
    return False
def reset_offline_notify(account_id):
    """账号恢复在线时清除冷却记录，便于下次掉线再次通知。"""

    _last_notified.pop(account_id, None)
    None(None, None)
