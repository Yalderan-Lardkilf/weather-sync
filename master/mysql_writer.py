"""
master/mysql_writer.py

处理 MySQL 数据库数据写入。
"""

import logging
from shared.weather_dao import CurrentWeatherDAO, MinutelyForecastDAO, HourlyForecastDAO, DailyForecastDAO, WeatherAlertsDAO

class MySQLWriter:
    def __init__(self, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
        self.MYSQL_HOST = MYSQL_HOST
        self.MYSQL_PORT = MYSQL_PORT
        self.MYSQL_USER = MYSQL_USER
        self.MYSQL_PASSWORD = MYSQL_PASSWORD
        self.MYSQL_DB = MYSQL_DB
        self.current_weather_dao = CurrentWeatherDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
        self.minutely_forecast_dao = MinutelyForecastDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
        self.hourly_forecast_dao = HourlyForecastDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
        self.daily_forecast_dao = DailyForecastDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
        self.weather_alerts_dao = WeatherAlertsDAO(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)

    def save_current_weather(self, weather_data):
        """将当前天气数据写入MySQL"""
        try:
            if self.current_weather_dao.insert(weather_data):
                logging.info("当前天气数据已写入MySQL")
                return True
            else:
                logging.error("当前天气数据写入MySQL失败")
                return False
        except Exception as e:
            logging.error(f"MySQL写入失败: {e}")
            return False

    def save_minutely_forecast(self, forecast_data):
        """将分钟级天气数据写入MySQL"""
        try:
            if self.minutely_forecast_dao.insert(forecast_data):
                logging.info("分钟级天气数据已写入MySQL")
                return True
            else:
                logging.error("分钟级天气数据写入MySQL失败")
                return False
        except Exception as e:
            logging.error(f"MySQL写入失败: {e}")
            return False

    def save_hourly_forecast(self, forecast_data):
        """将小时级天气数据写入MySQL"""
        try:
            if self.hourly_forecast_dao.insert(forecast_data):
                logging.info("小时级天气数据已写入MySQL")
                return True
            else:
                logging.error("小时级天气数据写入MySQL失败")
                return False
        except Exception as e:
            logging.error(f"MySQL写入失败: {e}")
            return False

    def save_daily_forecast(self, forecast_data):
        """将每日天气数据写入MySQL"""
        try:
            if self.daily_forecast_dao.insert(forecast_data):
                logging.info("每日天气数据已写入MySQL")
                return True
            else:
                logging.error("每日天气数据写入MySQL失败")
                return False
        except Exception as e:
            logging.error(f"MySQL写入失败: {e}")
            return False

    def save_weather_alerts(self, alert_data):
        """将天气警报数据写入MySQL"""
        try:
            if self.weather_alerts_dao.insert(alert_data):
                logging.info("天气警报数据已写入MySQL")
                return True
            else:
                logging.error("天气警报数据写入MySQL失败")
                return False
        except Exception as e:
            logging.error(f"MySQL写入失败: {e}")
            return False