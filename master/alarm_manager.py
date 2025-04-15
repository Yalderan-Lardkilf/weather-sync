"""
master/alarm_manager.py

告警管理核心模块，负责检查预警规则并触发通知。
"""

import logging
from datetime import datetime
from shared.db_connector import get_db_connection
from master.sms_sender import SmsSender

class AlarmManager:
    """
    告警管理器，根据预设规则检查天气数据并触发告警。
    """

    ALERT_RULES = {
        "temp_increase": {
            "type": "temp_increase",
            "threshold": 5,  # 24小时内升温≥5℃
            "message": "气温快速上升预警：{city}24小时内升温{delta}℃"
        },
        "temp_decrease": {
            "type": "temp_decrease",
            "threshold": 5,  # 24小时内降温≥5℃
            "message": "寒潮预警：{city}24小时内降温{delta}℃"
        },
        "extreme_weather": {
            "type": "extreme_weather",
            "conditions": ["暴雨", "暴雪", "高温红色"],
            "message": "极端天气预警：{city}当前天气{weather}"
        }
    }

    SMS_API_URL = "http://your-sms-api.com/send"  # 替换为真实的短信API地址

    def __init__(self, mysql_config):
        """
        初始化告警管理器。
        参数：
            mysql_config: MySQL数据库配置
        """
        self.mysql_config = mysql_config
        self.db_connection = None  # 数据库连接
        self.sms_sender = SmsSender(self.SMS_API_URL)
        self.alert_rules = self.ALERT_RULES

    def check_alerts(self, weather_data):
        """
        检查天气数据是否触发任何预警规则。
        参数：
            weather_data: 天气数据
        """
        logging.info("开始检查告警...")
        for rule_name, rule in self.alert_rules.items():
            try:
                if self._is_alert_triggered(rule, weather_data):
                    message = rule["message"].format(**weather_data)
                    self._trigger_alert(message)
            except Exception as e:
                logging.error(f"检查规则 {rule_name} 失败: {e}")

    def _is_alert_triggered(self, rule, weather_data):
        """
        根据规则类型判断是否触发告警。
        参数：
            rule: 预警规则
            weather_data: 天气数据
        """
        if rule_type := rule.get("type") == "temp_increase":
            # TODO: 实现温度升高判断逻辑
            return False
        elif rule_type == "temp_decrease":
            # TODO: 实现温度降低判断逻辑
            return False
        elif rule_type == "extreme_weather":
            # TODO: 实现极端天气判断逻辑
            return False
        else:
            logging.warning(f"未知的规则类型: {rule_type}")
            return False

    def _trigger_alert(self, message):
        """
        触发告警，发送短信并记录到数据库。
        参数：
            message: 告警消息
        """
        logging.info(f"触发告警: {message}")
        try:
            # TODO: 从配置中获取管理员手机号列表
            phone_numbers = ["13800138000"]
            self.sms_sender.send_sms(phone_numbers, message)
            self._record_alert(message)
        except Exception as e:
            logging.error(f"发送告警失败: {e}")

    def _record_alert(self, message):
        """
        将告警信息记录到数据库。
        参数：
            message: 告警消息
        """
        try:
            if not self.db_connection:
                self.db_connection = get_db_connection(**self.mysql_config)
            cursor = self.db_connection.cursor()
            cursor.execute("""
                INSERT INTO alerts (message, timestamp)
                VALUES (%s, %s)
            """, (message, datetime.utcnow()))
            self.db_connection.commit()
            logging.info("告警已记录到数据库")
        except Exception as e:
            logging.error(f"记录告警到数据库失败: {e}")
        finally:
            if self.db_connection:
                self.db_connection.close()
                self.db_connection = None