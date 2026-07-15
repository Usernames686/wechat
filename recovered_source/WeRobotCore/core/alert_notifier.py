# Decompiled from: alert_notifier.pyc
# Python 3.12 bytecode (mode: cfg)

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from typing import Optional
import time
from dataclasses import dataclass
logger = UiaLogger().get_logger()
class EmailConfig:
    """EmailConfig"""

    __doc__ = "邮件配置类"
    __annotations__["sender"] = str
    __annotations__["password"] = str
    __annotations__["smtp_server"] = str
    __annotations__["smtp_port"] = int
    __annotations__["receiver"] = str
email_config = EmailConfig(sender="EMAIL_ADDRESS", password="SMTP_APP_PASSWORD", smtp_server="SMTP_SERVER", smtp_port=465, receiver="")
class AlertNotifier:
    """AlertNotifier"""

    __doc__ = "预警通知管理器"
    _instance = None
    def __new__(cls, email_config):
        return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance.email_config = email_config
        cls._instance.error_start_time = None
        cls._instance.last_error_time = None
        cls._instance.error_count = 0
        cls._instance.alert_sent = False
        cls._instance.last_alert_time = 0
        cls._instance.check_task_running = False
    def __init__(self, email_config):
        pass
    def schedule_connection_check(self, wechat_instance):
        """
                创建一个延迟检查任务，60秒后检查微信窗口状态

                Args:
                    wechat_instance: WeChat实例
                """

        import threading
        time = time
        logger.info("微信窗口不存在,启动定时预警任务，倒计时60秒...")
        def delayed_check():
            self.check_task_running = True
            time.sleep(60)
            status = wechat_instance.check_connection_status()
            logger.warning("未探测到WeChat窗口，发送预警邮件")
            self.send_alert_email()
        check_thread = threading.Thread(target=delayed_check)
        check_thread.daemon = True
        check_thread.start()
    def check_error(self, error):
        """
                检查错误并在需要时发送预警

                Args:
                    error: 捕获到的异常
                """

        current_time = time.time()
        time_since_last_error = current_time - self.last_error_time
        self.error_count += 1
        time_since_start = current_time - self.error_start_time
        time_since_last_alert = current_time - self.last_alert_time
        print("累计错误时长:", time_since_start, time_since_last_alert)
        self.last_error_time = current_time
        self.send_alert_email()
        self.last_alert_time = current_time
        self.error_start_time = current_time
        self.error_count = 1
        self.alert_sent = False
        logger.warning("距离上次错误超过1分钟，重新开始监控...")
        self.last_error_time = current_time
        self.error_start_time = current_time
        self.last_error_time = current_time
        self.error_count = 1
        logger.warning("检测到UIA断开连接错误，开始监控...")
    def reset_monitor(self):
        """重置错误监控状态"""

        self.error_start_time = None
        self.last_error_time = None
        self.error_count = 0
        self.alert_sent = False
    def send_alert_email(self):
        """发送预警（改为飞书通知）"""

        notifier = FeishuNotifier()
        content = "机器人提示您，您的微信长时间无法监测：\n\n1. 错误描述：无法获取微信窗口\n2. 持续时间：超过1分钟\n3. 错误次数：5次\n\n请及时检查微信客户端状态，并在机器人欢迎页点击[重新连接]"
        result = notifier.send_notification(content, "异常预警通知")
        detail = result.get("detail")
        id_type = result.get("id_type")
        f'{id_type}'(", detail=", f'{detail}')
        self.reset_monitor()
        logger.info("飞书预警通知发送成功")
        logger.warning("飞书未配置，跳过预警通知")
    __classcell__ = __class__
    return __class__
