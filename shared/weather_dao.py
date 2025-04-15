"""
shared/weather_dao.py

定义数据库访问对象 (DAO)，用于处理天气数据的 CRUD 操作。
"""

import logging
from dbutils.pooled_db import PooledDBError
import pymysql
from pymysql import MySQLError, OperationalError, ProgrammingError, InternalError

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
        from shared.db_connector import get_db_connection
        return get_db_connection(
            host=self.MYSQL_HOST, port=self.MYSQL_PORT, 
            user=self.MYSQL_USER, password=self.MYSQL_PASSWORD, 
            db=self.MYSQL_DB
        )

    def _log_db_error(self, e, operation):
        """记录详细的数据库错误日志"""
        error_details = {
            'operation': operation,
            'error_type': type(e).__name__,
            'error_code': getattr(e, 'args', (None,))[0],
            'error_msg': str(e),
            'table': self.table_name
        }
        logging.error(f"数据库操作失败: {error_details}", exc_info=True)

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
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
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
                cursor.execute(sql, params)
            conn.commit()
            logging.info("当前天气数据已写入MySQL")
            return True
            
        except OperationalError as e:
            self._log_db_error(e, "insert_current_weather")
            if conn:
                conn.rollback()
            raise ConnectionError("数据库连接错误，请检查网络或数据库状态") from e
        except ProgrammingError as e:
            self._log_db_error(e, "insert_current_weather")
            if conn:
                conn.rollback()
            raise ValueError("SQL语句或参数错误") from e
        except InternalError as e:
            self._log_db_error(e, "insert_current_weather")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库内部错误") from e
        except PooledDBError as e:
            self._log_db_error(e, "insert_current_weather")
            raise ConnectionError("连接池资源耗尽") from e
        except MySQLError as e:
            self._log_db_error(e, "insert_current_weather")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库操作失败") from e
        finally:
            if conn:
                conn.close()

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
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO minutely_forecast (dt, precipitation)
                VALUES (%s, %s)
                """
                params = [(minute["dt"], minute["precipitation"]) for minute in forecast_data]
                cursor.executemany(sql, params)
            conn.commit()
            logging.info("分钟级天气数据已写入MySQL")
            return True
            
        except OperationalError as e:
            self._log_db_error(e, "insert_minutely_forecast")
            if conn:
                conn.rollback()
            raise ConnectionError("数据库连接错误，请检查网络或数据库状态") from e
        except ProgrammingError as e:
            self._log_db_error(e, "insert_minutely_forecast")
            if conn:
                conn.rollback()
            raise ValueError("SQL语句或参数错误") from e
        except InternalError as e:
            self._log_db_error(e, "insert_minutely_forecast")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库内部错误") from e
        except PooledDBError as e:
            self._log_db_error(e, "insert_minutely_forecast")
            raise ConnectionError("连接池资源耗尽") from e
        except MySQLError as e:
            self._log_db_error(e, "insert_minutely_forecast")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库操作失败") from e
        finally:
            if conn:
                conn.close()

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
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO hourly_forecast (dt, temperature, feels_like, pressure, humidity, wind_speed, wind_deg, clouds, pop, weather)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = [(
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
                ) for hour in forecast_data]
                cursor.executemany(sql, params)
            conn.commit()
            logging.info("小时级天气数据已写入MySQL")
            return True
            
        except OperationalError as e:
            self._log_db_error(e, "insert_hourly_forecast")
            if conn:
                conn.rollback()
            raise ConnectionError("数据库连接错误，请检查网络或数据库状态") from e
        except ProgrammingError as e:
            self._log_db_error(e, "insert_hourly_forecast")
            if conn:
                conn.rollback()
            raise ValueError("SQL语句或参数错误") from e
        except InternalError as e:
            self._log_db_error(e, "insert_hourly_forecast")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库内部错误") from e
        except PooledDBError as e:
            self._log_db_error(e, "insert_hourly_forecast")
            raise ConnectionError("连接池资源耗尽") from e
        except MySQLError as e:
            self._log_db_error(e, "insert_hourly_forecast")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库操作失败") from e
        finally:
            if conn:
                conn.close()

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
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO daily_forecast (dt, sunrise, sunset, moonrise, moonset, moon_phase, summary, temp_day, temp_min, temp_max, temp_night, temp_eve, temp_morn, feels_like_day, feels_like_night, feels_like_eve, feels_like_morn, pressure, humidity, wind_speed, wind_deg, clouds, pop, rain, uvi, weather)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = [(
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
                ) for day in forecast_data]
                cursor.executemany(sql, params)
            conn.commit()
            logging.info("每日天气数据已写入MySQL")
            return True
            
        except OperationalError as e:
            self._log_db_error(e, "insert_daily_forecast")
            if conn:
                conn.rollback()
            raise ConnectionError("数据库连接错误，请检查网络或数据库状态") from e
        except ProgrammingError as e:
            self._log_db_error(e, "insert_daily_forecast")
            if conn:
                conn.rollback()
            raise ValueError("SQL语句或参数错误") from e
        except InternalError as e:
            self._log_db_error(e, "insert_daily_forecast")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库内部错误") from e
        except PooledDBError as e:
            self._log_db_error(e, "insert_daily_forecast")
            raise ConnectionError("连接池资源耗尽") from e
        except MySQLError as e:
            self._log_db_error(e, "insert_daily_forecast")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库操作失败") from e
        finally:
            if conn:
                conn.close()

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
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO weather_alerts (sender_name, event, start, end, description, tags)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = [(
                    alert["sender_name"],
                    alert["event"],
                    alert["start"],
                    alert["end"],
                    alert["description"],
                    ",".join(alert["tags"]) if alert["tags"] else None,
                ) for alert in alert_data]
                cursor.executemany(sql, params)
            conn.commit()
            logging.info("天气警报数据已写入MySQL")
            return True
            
        except OperationalError as e:
            self._log_db_error(e, "insert_weather_alerts")
            if conn:
                conn.rollback()
            raise ConnectionError("数据库连接错误，请检查网络或数据库状态") from e
        except ProgrammingError as e:
            self._log_db_error(e, "insert_weather_alerts")
            if conn:
                conn.rollback()
            raise ValueError("SQL语句或参数错误") from e
        except InternalError as e:
            self._log_db_error(e, "insert_weather_alerts")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库内部错误") from e
        except PooledDBError as e:
            self._log_db_error(e, "insert_weather_alerts")
            raise ConnectionError("连接池资源耗尽") from e
        except MySQLError as e:
            self._log_db_error(e, "insert_weather_alerts")
            if conn:
                conn.rollback()
            raise RuntimeError("数据库操作失败") from e
        finally:
            if conn:
                conn.close()

def check_pool_status():
    """
    检查连接池状态
    """
    from shared.db_connector import pool_status
    return pool_status()