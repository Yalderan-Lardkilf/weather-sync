"""
shared/weather_dao.py

定义数据库访问对象 (DAO)，用于处理天气数据的 CRUD 操作。
"""

import logging
from shared.db_connector import get_db_connection

class BaseWeatherDAO:
    """
    DAO 基类，封装数据库连接和通用操作。
    """
    def __init__(self, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, table_name):
        self.MYSQL_HOST = MYSQL_HOST
        self.MYSQL_PORT = MYSQL_PORT
        self.MYSQL_USER = MYSQL_USER
        self.MYSQL_PASSWORD = MYSQL_PASSWORD
        self.MYSQL_DB = MYSQL_DB
        self.table_name = table_name

    def get_connection(self):
        """
        获取数据库连接。
        """
        return get_db_connection(
            host=self.MYSQL_HOST, port=self.MYSQL_PORT, user=self.MYSQL_USER, password=self.MYSQL_PASSWORD, db=self.MYSQL_DB
        )

    def execute_sql(self, sql, params=None):
        """
        执行 SQL 语句。
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logging.error(f"执行SQL失败: {e}")
            return False

class CurrentWeatherDAO(BaseWeatherDAO):
    """
    `current_weather` 表的 DAO。
    """
    def __init__(self, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
        super().__init__(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, "current_weather")

    def insert(self, weather_data):
        """
        插入当前天气数据。
        """
        sql = """
        INSERT INTO current_weather (dt, sunrise, sunset, temp, feels_like, pressure, humidity, dew_point, uvi, clouds, visibility, wind_speed, wind_deg, wind_gust, weather_id, weather_main, weather_description, weather_icon)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            weather_data["dt"],
            weather_data["sunrise"],
            weather_data["sunset"],
            weather_data["temp"],
            weather_data["feels_like"],
            weather_data["pressure"],
            weather_data["humidity"],
            weather_data["dew_point"],
            weather_data["uvi"],
            weather_data["clouds"],
            weather_data["visibility"],
            weather_data["wind_speed"],
            weather_data["wind_deg"],
            weather_data["wind_gust"],
            weather_data["weather"][0]["id"],
            weather_data["weather"][0]["main"],
            weather_data["weather"][0]["description"],
            weather_data["weather"][0]["icon"],
        )
        return self.execute_sql(sql, params)

class MinutelyForecastDAO(BaseWeatherDAO):
    """
    `minutely_forecast` 表的 DAO。
    """
    def __init__(self, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
        super().__init__(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, "minutely_forecast")

    def insert(self, forecast_data):
        """
        插入分钟级天气数据。
        """
        sql = """
        INSERT INTO minutely_forecast (dt, precipitation)
        VALUES (%s, %s)
        """
        success = True
        for minute in forecast_data:
            params = (
                minute["dt"],
                minute["precipitation"],
            )
            if not self.execute_sql(sql, params):
                success = False
        return success

class HourlyForecastDAO(BaseWeatherDAO):
    """
    `hourly_forecast` 表的 DAO。
    """
    def __init__(self, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
        super().__init__(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, "hourly_forecast")

    def insert(self, forecast_data):
        """
        插入小时级天气数据。
        """
        sql = """
        INSERT INTO hourly_forecast (dt, temperature, feels_like, pressure, humidity, wind_speed, wind_deg, clouds, pop, weather)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success = True
        for hour in forecast_data:
            params = (
                hour["dt"],
                hour["temp"],
                hour["feels_like"],
                hour["pressure"],
                hour["humidity"],
                hour["wind_speed"],
                hour["wind_deg"],
                hour["clouds"],
                hour["pop"],
                hour["weather"][0]["main"] if hour["weather"] else None,
            )
            if not self.execute_sql(sql, params):
                success = False
        return success

class DailyForecastDAO(BaseWeatherDAO):
    """
    `daily_forecast` 表的 DAO。
    """
    def __init__(self, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
        super().__init__(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, "daily_forecast")

    def insert(self, forecast_data):
        """
        插入每日天气数据。
        """
        sql = """
        INSERT INTO daily_forecast (dt, sunrise, sunset, moonrise, moonset, moon_phase, summary, temp_day, temp_min, temp_max, temp_night, temp_eve, temp_morn, feels_like_day, feels_like_night, feels_like_eve, feels_like_morn, pressure, humidity, wind_speed, wind_deg, clouds, pop, rain, uvi, weather)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success = True
        for day in forecast_data:
            params = (
                day["dt"],
                day["sunrise"],
                day["sunset"],
                day["moonrise"],
                day["moonset"],
                day["moon_phase"],
                day["summary"],
                day["temp"]["day"],
                day["temp"]["min"],
                day["temp"]["max"],
                day["temp"]["night"],
                day["temp"]["eve"],
                day["temp"]["morn"],
                day["feels_like"]["day"],
                day["feels_like"]["night"],
                day["feels_like"]["eve"],
                day["feels_like"]["morn"],
                day["pressure"],
                day["humidity"],
                day["wind_speed"],
                day["wind_deg"],
                day["clouds"],
                day["pop"],
                day.get("rain", 0),
                day["uvi"],
                day["weather"][0]["main"] if day["weather"] else None,
            )
            if not self.execute_sql(sql, params):
                success = False
        return success

class WeatherAlertsDAO(BaseWeatherDAO):
    """
    `weather_alerts` 表的 DAO。
    """
    def __init__(self, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB):
        super().__init__(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, "weather_alerts")

    def insert(self, alert_data):
        """
        插入天气警报数据。
        """
        sql = """
        INSERT INTO weather_alerts (sender_name, event, start, end, description, tags)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        success = True
        for alert in alert_data:
            params = (
                alert["sender_name"],
                alert["event"],
                alert["start"],
                alert["end"],
                alert["description"],
                ",".join(alert["tags"]) if alert["tags"] else None,
            )
            if not self.execute_sql(sql, params):
                success = False
        return success